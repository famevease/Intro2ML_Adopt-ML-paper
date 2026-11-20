import argparse
import os

import numpy as np
import torch
from torch.utils.data import DataLoader, Subset
import wandb

from src.calibration import calibrate_new_prototypes, compute_raw_prototypes
from src.dataset import CIFARDatasetFSCIL
from src.eval_incremental import predict_all
from src.models import ResNet20CIFAR
from src.utils import compute_fscil_metrics, seed_everything


def run_hyperparameter_sweep(args: argparse.Namespace) -> None:
    """Thực thi thực nghiệm khảo sát độ nhạy siêu tham số alpha và tau trên CIFAR-100.

    Hiện thực hóa thí nghiệm Ablation Study tại Section 6.3 (Figure 5) của bài báo
    TEEN (Wang et al., NeurIPS 2023):
    - Đóng băng hoàn toàn backbone đã huấn luyện ở Session 0 (base_model.pth).
    - Quét lưới giá trị alpha trong [0.0, 0.1, ..., 0.9] và tau trong {8, 16, 32, 64}.
    - Ghi nhận AvgAcc, BAcc, NAcc, HMean và PD tại Session 8 (100 lớp) lên W&B.

    Args:
        args (argparse.Namespace): Các tham số cấu hình dòng lệnh.

    Returns:
        None
    """
    seed_everything(args.seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    if not os.path.exists(args.ckpt_path):
        raise FileNotFoundError(
            f"Không tìm thấy checkpoint tại '{args.ckpt_path}'. "
            "Hãy kiểm tra lại đường dẫn file base_model.pth."
        )

    wandb.init(
        entity=args.wandb_entity,
        project=args.wandb_project,
        name=f"ablation-alpha-tau-seed{args.seed}",
        tags=["lab1", "ablation-study", "sweep-alpha"],
        config=vars(args),
    )

    # 1. Nạp mô hình Session 0 và khóa cứng trạng thái suy luận
    model = ResNet20CIFAR(num_classes=100, tau=16.0).to(device)
    state_dict = torch.load(args.ckpt_path, map_location=device)
    model.load_state_dict(state_dict)
    model.eval()

    # 2. Chuẩn bị sẵn toàn bộ dữ liệu các phiên 0..8 và trích xuất 60 base prototypes 1 lần
    dataset = CIFARDatasetFSCIL(root=args.data_dir, seed=args.seed)

    base_clean_idx = np.where(dataset.train_targets < 60)[0]
    base_clean_set = Subset(dataset.train_clean_set, base_clean_idx)
    base_clean_loader = DataLoader(
        base_clean_set, batch_size=args.batch_size, shuffle=False, num_workers=2
    )
    base_prototypes = compute_raw_prototypes(
        model=model,
        dataloader=base_clean_loader,
        num_classes=60,
        device=device,
    )

    # Tính trước raw prototypes cho các lớp mới (Session 1..8) vì backbone cố định
    session_raw_new_protos: dict[int, torch.Tensor] = {}
    session_test_loaders: dict[int, DataLoader] = {}

    for session in range(0, 9):
        active_classes = 60 + session * 5
        support_set, test_set = dataset.get_session_data(
            session=session, ways=5, shots=5
        )
        session_test_loaders[session] = DataLoader(
            test_set, batch_size=args.batch_size, shuffle=False, num_workers=2
        )

        if session > 0:
            start_class = 60 + (session - 1) * 5
            support_loader = DataLoader(
                support_set, batch_size=25, shuffle=False, num_workers=2
            )
            raw_all = compute_raw_prototypes(
                model=model,
                dataloader=support_loader,
                num_classes=active_classes,
                device=device,
            )
            session_raw_new_protos[session] = raw_all[start_class:active_classes]

    # Đo Session 0 một lần làm mốc tính PD (không phụ thuộc vào alpha/tau hiệu chuẩn)
    preds_s0, targets_s0 = predict_all(
        model=model,
        loader=session_test_loaders[0],
        active_classes=60,
        device=device,
    )
    metrics_s0 = compute_fscil_metrics(preds=preds_s0, targets=targets_s0)
    session0_acc = metrics_s0["avg_acc"]

    # 3. Thực thi quét lưới siêu tham số theo Section 6.3 (Figure 5)
    tau_grid = [8.0, 16.0, 32.0, 64.0]
    alpha_grid = [round(0.1 * i, 1) for i in range(0, 10)]  # 0.0, 0.1, ..., 0.9

    print("\n" + "=" * 82)
    print(
        f"{'Tau':<6} | {'Alpha':<6} | {'S8 AvgAcc (%)':<14} | {'S8 BAcc (%)':<12} | "
        f"{'S8 NAcc (%)':<12} | {'S8 HMean (%)':<13} | {'PD (%)':<7}"
    )
    print("-" * 82)

    sweep_rows = []
    best_hmean_cfg = {"hmean": -1.0, "alpha": 0.0, "tau": 16.0, "avg_acc": 0.0, "new_acc": 0.0}

    for tau in tau_grid:
        model.tau = tau

        for alpha in alpha_grid:
            # Xóa trọng số các lớp mới (60..99) trước mỗi cấu hình để cô lập hoàn toàn
            model.fc.weight.data[60:].zero_()

            # Cắm prototype đã hiệu chuẩn cho toàn bộ 8 incremental sessions
            for session in range(1, 9):
                start_class = 60 + (session - 1) * 5
                end_class = 60 + session * 5
                calibrated = calibrate_new_prototypes(
                    base_prototypes=base_prototypes,
                    new_raw_prototypes=session_raw_new_protos[session],
                    alpha=alpha,
                    tau=tau,
                )
                model.fc.weight.data[start_class:end_class] = calibrated

            # Đánh giá trên toàn bộ 100 lớp tại Session cuối cùng (Session 8)
            preds_s8, targets_s8 = predict_all(
                model=model,
                loader=session_test_loaders[8],
                active_classes=100,
                device=device,
            )
            m8 = compute_fscil_metrics(
                preds=preds_s8,
                targets=targets_s8,
                num_base_classes=60,
                session0_acc=session0_acc,
            )

            row = {
                "tau": tau,
                "alpha": alpha,
                "s8_avg_acc": m8["avg_acc"],
                "s8_base_acc": m8["base_acc"],
                "s8_new_acc": m8["new_acc"],
                "s8_hmean": m8["hmean"],
                "pd": m8["pd"],
            }
            sweep_rows.append(row)

            if m8["hmean"] > best_hmean_cfg["hmean"]:
                best_hmean_cfg = {
                    "hmean": m8["hmean"],
                    "alpha": alpha,
                    "tau": tau,
                    "avg_acc": m8["avg_acc"],
                    "new_acc": m8["new_acc"],
                }

            # Ghi log riêng cho tau=16.0 (mặc định của CIFAR-100) để W&B vẽ line chart theo alpha
            if tau == 16.0:
                wandb.log({
                    "sweep_tau16/alpha": alpha,
                    "sweep_tau16/s8_avg_acc": m8["avg_acc"],
                    "sweep_tau16/s8_base_acc": m8["base_acc"],
                    "sweep_tau16/s8_new_acc": m8["new_acc"],
                    "sweep_tau16/s8_hmean": m8["hmean"],
                    "sweep_tau16/pd": m8["pd"],
                })

            print(
                f"{tau:<6.1f} | {alpha:<6.1f} | {m8['avg_acc']:<14.2f} | "
                f"{m8['base_acc']:<12.2f} | {m8['new_acc']:<12.2f} | "
                f"{m8['hmean']:<13.2f} | {m8['pd']:<7.2f}"
            )

    print("=" * 82)
    print(
        f"Cấu hình cân bằng tốt nhất (theo HMean): tau={best_hmean_cfg['tau']}, "
        f"alpha={best_hmean_cfg['alpha']} -> AvgAcc={best_hmean_cfg['avg_acc']:.2f}%, "
        f"NAcc={best_hmean_cfg['new_acc']:.2f}%, HMean={best_hmean_cfg['hmean']:.2f}%"
    )

    # Lưu toàn bộ 40 tổ hợp (tau, alpha) vào W&B Table để vẽ biểu đồ Figure 5a & 5b
    ablation_table = wandb.Table(
        columns=[
            "tau",
            "alpha",
            "s8_avg_acc",
            "s8_base_acc",
            "s8_new_acc",
            "s8_hmean",
            "pd",
        ]
    )
    for r in sweep_rows:
        ablation_table.add_data(
            r["tau"],
            r["alpha"],
            r["s8_avg_acc"],
            r["s8_base_acc"],
            r["s8_new_acc"],
            r["s8_hmean"],
            r["pd"],
        )

    wandb.log({"ablation_alpha_tau_table": ablation_table})
    wandb.summary["best_hmean_alpha"] = best_hmean_cfg["alpha"]
    wandb.summary["best_hmean_tau"] = best_hmean_cfg["tau"]
    wandb.summary["best_hmean_value"] = best_hmean_cfg["hmean"]
    wandb.finish()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Sensitivity Sweep over alpha and tau for TEEN on CIFAR-100"
    )
    parser.add_argument("--data_dir", type=str, default="/content/data")
    parser.add_argument(
        "--ckpt_path",
        type=str,
        default="/content/drive/MyDrive/IntroML_TEEN/checkpoints/base_model.pth",
    )
    parser.add_argument("--batch_size", type=int, default=256)
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--wandb_entity", type=str, default=None)
    parser.add_argument("--wandb_project", type=str, default="Intro2ML-Group05")
    args = parser.parse_args()
    run_hyperparameter_sweep(args)
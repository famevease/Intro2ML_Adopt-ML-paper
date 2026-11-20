import argparse
import os

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Subset
import wandb

from src.calibration import calibrate_new_prototypes, compute_raw_prototypes
from src.dataset import CIFARDatasetFSCIL
from src.models import ResNet20CIFAR
from src.utils import compute_fscil_metrics, seed_everything

# Số liệu chuẩn của TEEN trên CIFAR-100 từ Table 6 (Appendix C.2, NeurIPS 2023)
PAPER_CIFAR100_TEEN = {
    0: 74.92,
    1: 72.65,
    2: 68.74,
    3: 65.01,
    4: 62.01,
    5: 59.29,
    6: 57.90,
    7: 54.76,
    8: 52.64,
}


@torch.no_grad()
def predict_all(
    model: nn.Module,
    loader: DataLoader,
    active_classes: int,
    device: torch.device,
) -> tuple[torch.Tensor, torch.Tensor]:
    """Chạy suy luận trên toàn bộ tập kiểm thử của phiên hiện tại.

    Args:
        model (nn.Module): Mô hình ResNet20CIFAR đã cập nhật ma trận trọng số W.
        loader (DataLoader): Bộ nạp dữ liệu kiểm thử tích lũy (60 + 5*session lớp).
        active_classes (int): Tổng số lớp đã xuất hiện tính đến phiên hiện tại.
        device (torch.device): Thiết bị tính toán (cuda hoặc cpu).

    Returns:
        tuple[torch.Tensor, torch.Tensor]: Bộ (preds, targets) trên CPU.
    """
    model.eval()
    all_preds, all_targets = [], []

    for images, labels in loader:
        images = images.to(device)
        logits = model(images, active_classes=active_classes)
        preds = logits.argmax(dim=1).cpu()
        all_preds.append(preds)
        all_targets.append(labels)

    return torch.cat(all_preds, dim=0), torch.cat(all_targets, dim=0)


def evaluate_incremental_fscil(args: argparse.Namespace) -> None:
    """Thực thi chuỗi đánh giá FSCIL từ Session 0 đến Session 8 trên CIFAR-100.

    Hiện thực hóa quy trình đánh giá tăng dần không huấn luyện lại của TEEN
    (Section 3.2, Section 5.1 & Section 6.1, NeurIPS 2023):
    1. Nạp checkpoint Session 0 và đóng băng hoàn toàn bộ trích xuất đặc trưng.
    2. Trích xuất 60 base prototypes làm mỏ neo ngữ nghĩa (Equation 1).
    3. Qua từng phiên 1..8 (5-way 5-shot): tính raw prototypes -> hiệu chuẩn bằng
       tổ hợp lồi (Equations 5-7) -> cắm trực tiếp vào ma trận W -> đo 5 chỉ số.

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
            "Hãy kiểm tra lại đường dẫn Google Drive của file base_model.pth."
        )

    wandb.init(
        entity=args.wandb_entity,
        project=args.wandb_project,
        name=f"incremental-teen-alpha{args.alpha}-tau{args.tau}-seed{args.seed}",
        tags=["lab1", "incremental-eval", "cifar100"],
        config=vars(args),
    )

    # 1. Nạp mô hình đã huấn luyện ở Session 0 và khóa cứng trạng thái eval()
    model = ResNet20CIFAR(num_classes=100, tau=args.tau).to(device)
    state_dict = torch.load(args.ckpt_path, map_location=device)
    model.load_state_dict(state_dict)
    model.eval()

    # 2. Khởi tạo dữ liệu CIFAR-100 theo chuẩn 60 base + 8x(5-way 5-shot)
    dataset = CIFARDatasetFSCIL(root=args.data_dir, seed=args.seed)

    # Trích xuất empirical prototypes của 60 lớp Base trên tập ảnh sạch (Equation 1)
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

    print("\n" + "=" * 86)
    print(
        f"{'Session':<9} | {'Classes':<7} | {'AvgAcc (%)':<10} | {'BAcc (%)':<9} | "
        f"{'NAcc (%)':<9} | {'HMean (%)':<9} | {'PD (%)':<7} | {'Paper (%)':<9}"
    )
    print("-" * 86)

    session0_acc = None
    session_results = []

    # 3. Vòng lặp đánh giá tuần tự từ Session 0 đến Session 8
    for session in range(0, 9):
        active_classes = 60 + session * 5
        support_set, test_set = dataset.get_session_data(
            session=session, ways=5, shots=5
        )

        if session > 0:
            start_class = 60 + (session - 1) * 5
            end_class = active_classes

            support_loader = DataLoader(
                support_set, batch_size=25, shuffle=False, num_workers=2
            )

            # Bước A (Eq. 1): Tính prototype thô từ 5 ảnh mẫu của 5 lớp mới
            raw_protos_all = compute_raw_prototypes(
                model=model,
                dataloader=support_loader,
                num_classes=end_class,
                device=device,
            )
            new_raw_prototypes = raw_protos_all[start_class:end_class]

            # Bước B (Eq. 5-7): Hiệu chuẩn prototype lớp mới bằng 60 lớp Base
            calibrated_prototypes = calibrate_new_prototypes(
                base_prototypes=base_prototypes,
                new_raw_prototypes=new_raw_prototypes,
                alpha=args.alpha,
                tau=args.tau,
            )

            # Bước C (Sec. 3.2): Cắm trực tiếp prototype đã hiệu chuẩn vào ma trận W
            model.fc.weight.data[start_class:end_class] = calibrated_prototypes

        # Đánh giá trên toàn bộ tập kiểm thử của các lớp đã học tính đến session hiện tại
        test_loader = DataLoader(
            test_set, batch_size=args.batch_size, shuffle=False, num_workers=2
        )
        preds, targets = predict_all(
            model=model,
            loader=test_loader,
            active_classes=active_classes,
            device=device,
        )

        metrics = compute_fscil_metrics(
            preds=preds,
            targets=targets,
            num_base_classes=60,
            session0_acc=session0_acc,
        )

        if session == 0:
            session0_acc = metrics["avg_acc"]

        pd_rate = metrics["pd"]
        paper_acc = PAPER_CIFAR100_TEEN[session]
        rel_dev = ((metrics["avg_acc"] - paper_acc) / paper_acc) * 100.0

        session_results.append({
            "session": session,
            "active_classes": active_classes,
            "avg_acc": metrics["avg_acc"],
            "base_acc": metrics["base_acc"],
            "new_acc": metrics["new_acc"],
            "hmean": metrics["hmean"],
            "pd": pd_rate,
            "paper_acc": paper_acc,
            "rel_dev_pct": round(rel_dev, 2),
        })

        wandb.log({
            "session": session,
            "active_classes": active_classes,
            "eval/avg_acc": metrics["avg_acc"],
            "eval/base_acc": metrics["base_acc"],
            "eval/new_acc": metrics["new_acc"],
            "eval/hmean": metrics["hmean"],
            "eval/pd": pd_rate,
            "paper/avg_acc": paper_acc,
        })

        print(
            f"Session {session:<1} | {active_classes:<7} | "
            f"{metrics['avg_acc']:<10.2f} | {metrics['base_acc']:<9.2f} | "
            f"{metrics['new_acc']:<9.2f} | {metrics['hmean']:<9.2f} | "
            f"{pd_rate:<7.2f} | {paper_acc:<9.2f}"
        )

    print("=" * 86)

    # Lưu bảng đối chiếu vào W&B Summary & W&B Table để trích xuất trực tiếp cho Slide
    final_res = session_results[-1]
    wandb.summary["final_session8_avg_acc"] = final_res["avg_acc"]
    wandb.summary["final_session8_new_acc"] = final_res["new_acc"]
    wandb.summary["final_session8_hmean"] = final_res["hmean"]
    wandb.summary["final_pd"] = final_res["pd"]

    table = wandb.Table(
        columns=[
            "session",
            "active_classes",
            "avg_acc",
            "base_acc",
            "new_acc",
            "hmean",
            "pd",
            "paper_acc",
            "rel_dev_pct",
        ]
    )
    for row in session_results:
        table.add_data(
            row["session"],
            row["active_classes"],
            row["avg_acc"],
            row["base_acc"],
            row["new_acc"],
            row["hmean"],
            row["pd"],
            row["paper_acc"],
            row["rel_dev_pct"],
        )
    wandb.log({"comparison_table": table})
    wandb.finish()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Evaluate Incremental FSCIL Sessions (0..8) with TEEN on CIFAR-100"
    )
    parser.add_argument("--data_dir", type=str, default="/content/data")
    parser.add_argument(
        "--ckpt_path",
        type=str,
        default="/content/drive/MyDrive/IntroML_TEEN/checkpoints/base_model.pth",
    )
    parser.add_argument("--batch_size", type=int, default=256)
    parser.add_argument("--alpha", type=float, default=0.1)
    parser.add_argument("--tau", type=float, default=16.0)
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--wandb_entity", type=str, default=None)
    parser.add_argument("--wandb_project", type=str, default="Intro2ML-Group05")
    args = parser.parse_args()
    evaluate_incremental_fscil(args)
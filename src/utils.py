import os
import random
from typing import Dict

import numpy as np
import torch


def seed_everything(seed: int = 42) -> None:
    """Khóa đồng bộ hạt giống ngẫu nhiên trên toàn bộ hệ thống để đảm bảo tính tái lập.

    Args:
        seed (int): Giá trị hạt giống ngẫu nhiên cố định (mặc định: 42).

    Returns:
        None
    """
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def compute_fscil_metrics(
    preds: torch.Tensor,
    targets: torch.Tensor,
    num_base_classes: int = 60,
) -> Dict[str, float]:
    """Tính bộ 4 chỉ số đánh giá tại một session FSCIL: AvgAcc, BAcc, NAcc và HMean.

    Cài đặt theo định nghĩa tại Section 4.1 và Section 6.1.2 của bài báo TEEN
    (Wang et al., NeurIPS 2023). Trên CIFAR-100, mỗi lớp có đều 100 ảnh test
    (Appendix C.1) nên độ chính xác theo mẫu trùng với trung bình theo từng lớp.

    Args:
        preds (torch.Tensor): Vector nhãn dự đoán của mô hình, shape (N,).
        targets (torch.Tensor): Vector nhãn thực tế (ground-truth), shape (N,).
        num_base_classes (int): Số lượng lớp cơ sở ở Session 0 (mặc định: 60).

    Returns:
        Dict[str, float]: Từ điển chứa các chỉ số tính theo thang phần trăm (%):
            - 'avg_acc': Độ chính xác trên toàn bộ các lớp đã gặp.
            - 'base_acc': Độ chính xác trên tập lớp cơ sở (BAcc).
            - 'new_acc': Độ chính xác trên tập lớp mới (NAcc).
            - 'h_mean': Trung bình điều hòa giữa BAcc và NAcc (HMean).
    """
    preds = preds.detach().cpu()
    targets = targets.detach().cpu()

    # 1. AvgAcc: Độ chính xác trên toàn bộ mẫu kiểm thử hiện tại
    avg_acc = (preds == targets).float().mean().item() * 100.0

    # 2. BAcc: Độ chính xác trên 60 lớp cơ sở (nhãn < num_base_classes)
    base_mask = targets < num_base_classes
    if base_mask.any():
        base_acc = (preds[base_mask] == targets[base_mask]).float().mean().item() * 100.0
    else:
        base_acc = 0.0

    # 3. NAcc: Độ chính xác trên các lớp mới (nhãn >= num_base_classes)
    new_mask = targets >= num_base_classes
    if new_mask.any():
        new_acc = (preds[new_mask] == targets[new_mask]).float().mean().item() * 100.0
        # 4. HMean: Trung bình điều hòa giữa BAcc và NAcc
        denom = base_acc + new_acc
        h_mean = (2.0 * base_acc * new_acc / denom) if denom > 0.0 else 0.0
    else:
        # Tại Session 0 chưa xuất hiện lớp mới
        new_acc = 0.0
        h_mean = 0.0

    return {
        "avg_acc": round(avg_acc, 4),
        "base_acc": round(base_acc, 4),
        "new_acc": round(new_acc, 4),
        "h_mean": round(h_mean, 4),
    }


def compute_pd(acc_session_0: float, acc_last_session: float) -> float:
    """Tính tỷ lệ suy giảm hiệu năng (Performance Dropping Rate - PD).

    Định nghĩa tại Section 6.1.2 (Wang et al., NeurIPS 2023): PD = Acc_0 - Acc_{-1}.

    Args:
        acc_session_0 (float): AvgAcc tại Session 0 (%).
        acc_last_session (float): AvgAcc tại Session cuối cùng (%).

    Returns:
        float: Độ sụt giảm độ chính xác PD (%).
    """
    return round(acc_session_0 - acc_last_session, 4)
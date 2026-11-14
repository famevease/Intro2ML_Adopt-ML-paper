import os
import random
import numpy as np
import torch


def seed_everything(seed: int = 2026) -> None:
    """Cố định toàn bộ hạt giống ngẫu nhiên để đảm bảo tính tái lập thực nghiệm.

    Args:
        seed (int): Giá trị hạt giống ngẫu nhiên. Mặc định là 2026.

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
    session0_acc: float | None = None,
) -> dict[str, float]:
    """Tính toán bộ chỉ số đánh giá chuẩn cho bài toán FSCIL.

    Args:
        preds (torch.Tensor): Nhãn dự đoán của mô hình, shape (N,).
        targets (torch.Tensor): Nhãn thực tế của tập test, shape (N,).
        num_base_classes (int): Số lượng lớp cơ sở ở Session 0. Mặc định là 60.
        session0_acc (float | None): Độ chính xác ở Session 0 để tính mức suy giảm PD.

    Returns:
        dict[str, float]: Từ điển chứa avg_acc, base_acc, new_acc, hmean và pd (%).
    """
    correct = (preds == targets).float()
    avg_acc = correct.mean().item() * 100.0

    base_mask = targets < num_base_classes
    new_mask = targets >= num_base_classes

    base_acc = correct[base_mask].mean().item() * 100.0 if base_mask.any() else 0.0
    new_acc = correct[new_mask].mean().item() * 100.0 if new_mask.any() else 0.0

    if base_acc + new_acc > 0 and new_mask.any():
        hmean = 2 * base_acc * new_acc / (base_acc + new_acc)
    else:
        hmean = 0.0

    pd = (session0_acc - avg_acc) if session0_acc is not None else 0.0

    return {
        "avg_acc": round(avg_acc, 2),
        "base_acc": round(base_acc, 2),
        "new_acc": round(new_acc, 2),
        "hmean": round(hmean, 2),
        "pd": round(pd, 2),
    }
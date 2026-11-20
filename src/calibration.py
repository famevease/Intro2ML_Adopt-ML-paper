import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader


@torch.no_grad()
def compute_raw_prototypes(
    model: nn.Module,
    dataloader: DataLoader,
    num_classes: int,
    device: torch.device,
) -> torch.Tensor:
    """Trích xuất vector prototype thô (trung bình đặc trưng) cho từng lớp.

    Hiện thực hóa Equation (1), Section 3.2 của bài báo TEEN (NeurIPS 2023):
        c_k = (1 / Num_k) * sum_{y_j == k} phi_theta(x_j)

    Args:
        model (nn.Module): Mạng ResNet20CIFAR đã đóng băng trọng số.
        dataloader (DataLoader): Bộ nạp dữ liệu chứa ảnh support và nhãn.
        num_classes (int): Tổng số lớp của không gian nhãn hiện tại (ví dụ: 60 ở Session 0,
            65 ở Session 1, ..., 100 ở Session 8).
        device (torch.device): Thiết bị tính toán (cuda hoặc cpu).

    Returns:
        torch.Tensor: Ma trận prototypes thô kích thước (num_classes, feature_dim).
            Các lớp không xuất hiện trong dataloader sẽ giữ giá trị 0.
    """
    model.eval()
    feature_dim = model.feature_dim
    prototypes = torch.zeros((num_classes, feature_dim), device=device)
    counts = torch.zeros(num_classes, device=device)

    for images, labels in dataloader:
        images, labels = images.to(device), labels.to(device)
        # Trích xuất đặc trưng 64 chiều phi_theta(x_j) không tính đạo hàm
        features = model.extract_features(images)

        for cls_id in labels.unique():
            mask = labels == cls_id
            prototypes[cls_id] += features[mask].sum(dim=0)
            counts[cls_id] += mask.sum()

    valid = counts > 0
    prototypes[valid] = prototypes[valid] / counts[valid].unsqueeze(1)
    return prototypes


def calibrate_new_prototypes(
    base_prototypes: torch.Tensor,
    new_raw_prototypes: torch.Tensor,
    alpha: float = 0.1,
    tau: float = 16.0,
) -> torch.Tensor:
    """Hiệu chuẩn prototype của các lớp mới bằng tổ hợp lồi với base prototypes.

    Hiện thực hóa thuật toán hiệu chuẩn không huấn luyện (Training-Free Calibration)
    tại Section 5.1, Equations (5), (6), (7) của bài báo TEEN (NeurIPS 2023):
        - Eq. (5): S_{b,n} = cosine_similarity(c_b, c_n) * tau
        - Eq. (6): w_{b,n} = softmax(S_{b,n} trên tập B lớp base)
        - Eq. (7): c_bar_n = (1 - alpha) * c_n + alpha * sum_{b=0}^{B-1} (w_{b,n} * c_b)

    Args:
        base_prototypes (torch.Tensor): Prototypes của B lớp cơ sở, shape (B, D).
        new_raw_prototypes (torch.Tensor): Prototypes thô của N lớp mới, shape (N, D).
        alpha (float): Hệ số cường độ hiệu chuẩn (mặc định 0.1 cho CIFAR-100).
        tau (float): Hệ số nhiệt độ khuếch đại độ sắc nét Softmax (mặc định 16.0).

    Returns:
        torch.Tensor: Ma trận prototypes của N lớp mới đã hiệu chuẩn và chuẩn hóa L2,
            kích thước (N, D).
    """
    # Chuẩn hóa L2 về độ dài đơn vị (||c||_2 = 1) để phép nhân vô hướng thành Cosine Similarity
    base_norm = F.normalize(base_prototypes, p=2, dim=1)  # shape: (B, D)
    new_norm = F.normalize(new_raw_prototypes, p=2, dim=1)  # shape: (N, D)

    # Equation (5): Ma trận độ tương đồng Cosine nhân hệ số nhiệt độ tau
    sim_matrix = torch.matmul(new_norm, base_norm.T) * tau  # shape: (N, B)

    # Equation (6): Trọng số chú ý ngữ nghĩa qua hàm Softmax trên chiều lớp base (dim=1)
    weights = F.softmax(sim_matrix, dim=1)  # shape: (N, B)

    # Equation (7): Tổ hợp lồi giữa prototype gốc của lớp mới và thành phần hiệu chuẩn base
    delta_c = torch.matmul(weights, base_norm)  # shape: (N, D)
    calibrated = (1.0 - alpha) * new_norm + alpha * delta_c

    # Chuẩn hóa L2 đầu ra để tương thích trực tiếp với Cosine Classifier
    return F.normalize(calibrated, p=2, dim=1)
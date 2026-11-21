from typing import Optional

import torch
import torch.nn as nn
import torch.nn.functional as F


class BasicBlock(nn.Module):
    """Khối dư cơ bản (Residual Block) gồm 2 tầng tích chập 3x3 cho ResNet-20 (He et al., CVPR 2016)."""

    expansion: int = 1

    def __init__(self, in_planes: int, planes: int, stride: int = 1) -> None:
        """Khởi tạo khối dư cơ bản (BasicBlock) cho kiến trúc ResNet-20 trên CIFAR-100.

        Gồm hai lớp tích chập 3x3 kèm BatchNorm2d (không bias) và kết nối tắt (shortcut)
        theo He et al. (CVPR 2016, Section 4.2), được bài báo TEEN chỉ định sử dụng cho
        CIFAR-100 tại Section 6.1.1 & Appendix C.1.

        Args:
            in_planes (int): Số kênh đặc trưng đầu vào.
            planes (int): Số kênh đặc trưng đầu ra của khối.
            stride (int): Bước nhảy của lớp tích chập đầu tiên (mặc định: 1).

        Returns:
            None
        """
        super().__init__()
        self.conv1 = nn.Conv2d(
            in_planes, planes, kernel_size=3, stride=stride, padding=1, bias=False
        )
        self.bn1 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(
            planes, planes, kernel_size=3, stride=1, padding=1, bias=False
        )
        self.bn2 = nn.BatchNorm2d(planes)

        # Đường cộng tắt (Skip connection): dùng Conv 1x1 nếu đổi số kênh hoặc giảm kích thước ảnh
        self.shortcut = nn.Sequential()
        if stride != 1 or in_planes != self.expansion * planes:
            self.shortcut = nn.Sequential(
                nn.Conv2d(
                    in_planes,
                    self.expansion * planes,
                    kernel_size=1,
                    stride=stride,
                    bias=False,
                ),
                nn.BatchNorm2d(self.expansion * planes),
            )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Thực hiện lan truyền thuận qua hai lớp tích chập và cộng nhánh kết nối tắt.

        Args:
            x (torch.Tensor): Tensor đặc trưng đầu vào có kích thước (B, in_planes, H, W).

        Returns:
            torch.Tensor: Tensor đặc trưng đầu ra sau hàm kích hoạt ReLU có kích thước
                (B, planes, H', W').
        """
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += self.shortcut(x)
        return F.relu(out)


class ResNet20CIFAR(nn.Module):
    """Mạng ResNet-20 cho ảnh 32x32 của CIFAR-100 kết hợp Cosine Classifier.

    Hiện thực hóa thiết lập kiến trúc tại Section 6.1.1 & Appendix C.1 (Wang et al., NeurIPS 2023):
    - Backbone ResNet-20 xuất vector đặc trưng d = 64 chiều.
    - Lớp fc không dùng bias đóng vai trò bảng lưu 100 vector prototype (60 base + 40 new).
    - Logits = CosineSimilarity(feature, prototype) * tau (với tau = 16.0).
    """

    def __init__(self, num_classes: int = 100, tau: float = 16.0) -> None:
        """Khởi tạo mạng ResNet-20 (d=64) kèm Cosine Classifier cho CIFAR-100.

        Xây dựng theo kiến trúc chuẩn cho ảnh 32x32 (He et al., CVPR 2016, Section 4.2)
        và thiết lập của TEEN trên CIFAR-100 (Section 6.1.1 & Appendix C.1): không dùng
        MaxPool ở tầng đầu, gồm 3 cụm tầng (16 -> 32 -> 64 kênh) và lớp phân loại Cosine
        không bias.

        Args:
            num_classes (int): Tổng số lớp tối đa của bộ phân loại (mặc định: 100).
            tau (float): Hệ số nhiệt độ phóng đại độ tương đồng Cosine (mặc định: 16.0).

        Returns:
            None
        """
        super().__init__()
        self.in_planes = 16
        self.tau = tau
        self.feature_dim = 64

        # Tầng đầu giữ nguyên kích thước 32x32 (khác với ResNet-18)
        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(16)

        # 3 cụm khối dư: 1 + 2*(3+3+3) + 1(fc) = 20 tầng có trọng số
        self.layer1 = self._make_layer(16, num_blocks=3, stride=1)  # Output: (B, 16, 32, 32)
        self.layer2 = self._make_layer(32, num_blocks=3, stride=2)  # Output: (B, 32, 16, 16)
        self.layer3 = self._make_layer(64, num_blocks=3, stride=2)  # Output: (B, 64, 8, 8)
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))                 # Output: (B, 64, 1, 1)

        # Bảng lưu trữ prototypes: shape (100, 64), không dùng bias
        self.fc = nn.Linear(self.feature_dim, num_classes, bias=False)

    def _make_layer(self, planes: int, num_blocks: int, stride: int) -> nn.Sequential:
        """Xây dựng một cụm tầng (stage) gồm các khối BasicBlock nối tiếp nhau.

        Args:
            planes (int): Số kênh đặc trưng đầu ra của cụm tầng.
            num_blocks (int): Số lượng khối BasicBlock trong cụm (mặc định: 3 cho ResNet-20).
            stride (int): Bước nhảy áp dụng cho khối đầu tiên của cụm để giảm kích thước không gian.

        Returns:
            nn.Sequential: Chuỗi các khối BasicBlock đã được ghép nối tuần tự.
        """
        strides = [stride] + [1] * (num_blocks - 1)
        layers = []
        for s in strides:
            layers.append(BasicBlock(self.in_planes, planes, s))
            self.in_planes = planes * BasicBlock.expansion
        return nn.Sequential(*layers)

    def extract_features(self, x: torch.Tensor) -> torch.Tensor:
        """Trích xuất vector đặc trưng thô 64 chiều phi_theta(x) từ ảnh đầu vào.

        Args:
            x (torch.Tensor): Batch ảnh đầu vào, shape (Batch, 3, 32, 32).

        Returns:
            torch.Tensor: Vector đặc trưng chưa chuẩn hóa L2, shape (Batch, 64).
        """
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.layer1(out)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.avgpool(out)
        return torch.flatten(out, 1)  # Duỗi (B, 64, 1, 1) -> (B, 64)

    def forward(
        self, x: torch.Tensor, active_classes: Optional[int] = None
    ) -> torch.Tensor:
        """Tính logits phân loại dựa trên Cosine Similarity nhân hệ số nhiệt độ tau.

        Args:
            x (torch.Tensor): Batch ảnh đầu vào, shape (Batch, 3, 32, 32).
            active_classes (Optional[int]): Số lớp đang xét ở session hiện tại
                (ví dụ: 60 ở Session 0, 65 ở Session 1, ..., 100 ở Session 8).

        Returns:
            torch.Tensor: Ma trận logits O * tau, shape (Batch, active_classes).
        """
        # Chuẩn hóa L2 vector đặc trưng và vector prototype về độ dài 1
        features = F.normalize(self.extract_features(x), p=2, dim=1)
        weights = (
            self.fc.weight
            if active_classes is None
            else self.fc.weight[:active_classes]
        )
        norm_weights = F.normalize(weights, p=2, dim=1)

        # Phép nhân hai vector đã chuẩn hóa L2 chính là Cosine Similarity, sau đó nhân tau
        logits = F.linear(features, norm_weights) * self.tau
        return logits
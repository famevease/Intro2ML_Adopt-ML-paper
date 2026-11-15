import torch
import torch.nn as nn
import torch.nn.functional as F


class BasicBlock(nn.Module):
    """Khối dư cơ bản (Residual Block) cho kiến trúc ResNet-20 trên CIFAR-100."""

    expansion = 1

    def __init__(self, in_planes: int, planes: int, stride: int = 1) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(
            in_planes, planes, kernel_size=3, stride=stride, padding=1, bias=False
        )
        self.bn1 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(
            planes, planes, kernel_size=3, stride=1, padding=1, bias=False
        )
        self.bn2 = nn.BatchNorm2d(planes)

        self.shortcut = nn.Sequential()
        if stride != 1 or in_planes != self.expansion * planes:
            self.shortcut = nn.Sequential(
                nn.Conv2d(
                    in_planes, self.expansion * planes, kernel_size=1, stride=stride, bias=False
                ),
                nn.BatchNorm2d(self.expansion * planes),
            )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += self.shortcut(x)
        return F.relu(out)


class ResNet20CIFAR(nn.Module):
    """Mạng ResNet-20 chuẩn cho CIFAR-100 kết hợp lớp phân loại Cosine Similarity.

    Attributes:
        tau (float): Hệ số nhiệt độ nhân với Cosine Similarity trước Cross-Entropy.
        fc (nn.Linear): Lớp trọng số lưu trữ các class prototypes (không dùng bias).
    """

    def __init__(self, num_classes: int = 100, tau: float = 16.0) -> None:
        super().__init__()
        self.in_planes = 16
        self.tau = tau
        self.feature_dim = 64

        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(16)
        self.layer1 = self._make_layer(16, num_blocks=3, stride=1)
        self.layer2 = self._make_layer(32, num_blocks=3, stride=2)
        self.layer3 = self._make_layer(64, num_blocks=3, stride=2)
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))

        # Lớp phân loại không bias đóng vai trò lưu trữ vector prototypes
        self.fc = nn.Linear(self.feature_dim, num_classes, bias=False)

    def _make_layer(self, planes: int, num_blocks: int, stride: int) -> nn.Sequential:
        strides = [stride] + [1] * (num_blocks - 1)
        layers = []
        for s in strides:
            layers.append(BasicBlock(self.in_planes, planes, s))
            self.in_planes = planes * BasicBlock.expansion
        return nn.Sequential(*layers)

    def extract_features(self, x: torch.Tensor) -> torch.Tensor:
        """Trích xuất vector đặc trưng 64 chiều từ ảnh đầu vào."""
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.layer1(out)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.avgpool(out)
        return torch.flatten(out, 1)

    def forward(self, x: torch.Tensor, active_classes: int | None = None) -> torch.Tensor:
        """Tính logits dựa trên độ tương đồng Cosine nhân với hệ số nhiệt độ tau."""
        features = F.normalize(self.extract_features(x), p=2, dim=1)
        weights = self.fc.weight if active_classes is None else self.fc.weight[:active_classes]
        norm_weights = F.normalize(weights, p=2, dim=1)
        logits = F.linear(features, norm_weights) * self.tau
        return logits
import numpy as np
import torch
from torch.utils.data import Dataset, Subset
from torchvision import datasets, transforms


class CIFARDatasetFSCIL:
    """Quản lý và chia tập dữ liệu CIFAR-100 theo chuẩn FSCIL (60 base + 8x5 incremental).

    Attributes:
        root (str): Thư mục lưu trữ dữ liệu CIFAR-100.
        seed (int): Hạt giống ngẫu nhiên dùng để bốc 5 mẫu/lớp ở các incremental session.
    """

    def __init__(self, root: str = "./data", seed: int = 2026) -> None:
        self.root = root
        self.seed = seed

        # Chuẩn hóa theo mean và std tiêu chuẩn của CIFAR-100
        self.mean = (0.5071, 0.4867, 0.4408)
        self.std = (0.2675, 0.2565, 0.2761)

        self.train_transform = transforms.Compose([
            transforms.RandomCrop(32, padding=4),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize(self.mean, self.std),
        ])

        self.test_transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(self.mean, self.std),
        ])

        # Tải bộ dữ liệu gốc (train có augmentation, train_raw không augmentation để rút trích prototype)
        self.train_aug_set = datasets.CIFAR100(
            root=self.root, train=True, download=True, transform=self.train_transform
        )
        self.train_clean_set = datasets.CIFAR100(
            root=self.root, train=True, download=False, transform=self.test_transform
        )
        self.test_set = datasets.CIFAR100(
            root=self.root, train=False, download=True, transform=self.test_transform
        )

        self.train_targets = np.array(self.train_clean_set.targets)
        self.test_targets = np.array(self.test_set.targets)

    def get_session_data(
        self, session: int, ways: int = 5, shots: int = 5
    ) -> tuple[Dataset, Dataset]:
        """Lấy tập dữ liệu huấn luyện (support) và kiểm thử (query) cho từng session.

        Args:
            session (int): Chỉ số session từ 0 (Base) đến 8 (Incremental cuối).
            ways (int): Số lớp mới mỗi incremental session. Mặc định là 5.
            shots (int): Số ảnh mẫu mỗi lớp mới. Mặc định là 5.

        Returns:
            tuple[Dataset, Dataset]: (train_subset, test_subset) tương ứng của session.
        """
        if session == 0:
            # Session 0: Toàn bộ 500 ảnh train và 100 ảnh test của 60 lớp đầu (0..59)
            train_idx = np.where(self.train_targets < 60)[0]
            test_idx = np.where(self.test_targets < 60)[0]
            return Subset(self.train_aug_set, train_idx), Subset(self.test_set, test_idx)

        # Incremental Session (1..8): Mỗi session thêm 5 lớp mới, mỗi lớp 5 ảnh
        start_class = 60 + (session - 1) * ways
        end_class = start_class + ways
        rng = np.random.default_rng(self.seed + session)

        support_indices = []
        for cls_id in range(start_class, end_class):
            cls_indices = np.where(self.train_targets == cls_id)[0]
            chosen = rng.choice(cls_indices, size=shots, replace=False)
            support_indices.extend(chosen.tolist())

        # Tập test đánh giá trên TOÀN BỘ các lớp đã gặp từ Session 0 đến hiện tại
        test_idx = np.where(self.test_targets < end_class)[0]

        return Subset(self.train_clean_set, support_indices), Subset(self.test_set, test_idx)
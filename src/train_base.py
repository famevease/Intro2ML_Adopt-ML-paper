import argparse
import os

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import wandb

from src.dataset import CIFARDatasetFSCIL
from src.models import ResNet20CIFAR
from src.utils import seed_everything


def evaluate_base(
    model: nn.Module,
    loader: DataLoader,
    device: torch.device,
    num_classes: int = 60,
) -> float:
    """Đánh giá độ chính xác Top-1 trên tập kiểm thử của 60 lớp Base (Session 0).

    Args:
        model (nn.Module): Mô hình ResNet20CIFAR đang huấn luyện.
        loader (DataLoader): Bộ nạp dữ liệu kiểm thử của 60 lớp Base (6.000 ảnh).
        device (torch.device): Thiết bị tính toán (cuda hoặc cpu).
        num_classes (int): Số lượng lớp cơ sở (mặc định: 60).

    Returns:
        float: Độ chính xác Top-1 tính theo thang phần trăm (%).
    """
    model.eval()
    correct, total = 0, 0
    with torch.no_grad():
        for images, labels in loader:
            images, labels = images.to(device), labels.to(device)
            logits = model(images, active_classes=num_classes)
            preds = logits.argmax(dim=1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)
    return (correct / total) * 100.0


def train_base_session(args: argparse.Namespace) -> None:
    """Huấn luyện mạng ResNet-20 trên 60 lớp Base của CIFAR-100 (Session 0).

    Cài đặt theo Section 6.1.1 & Appendix C.1 của bài báo TEEN (NeurIPS 2023):
    - Optimizer SGD (lr=0.1, momentum=0.9, weight_decay=5e-4) + CosineAnnealingLR.
    - Hàm mất mát Cross-Entropy trên logits đã nhân nhiệt độ tau=16.0.
    - Lưu checkpoint tốt nhất sang Google Drive và ghi log real-time lên W&B.

    Args:
        args (argparse.Namespace): Các tham số dòng lệnh cấu hình thực nghiệm.

    Returns:
        None
    """
    seed_everything(args.seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    wandb.init(
        entity=args.wandb_entity,
        project=args.wandb_project,
        name=f"base-session-resnet20-seed{args.seed}",
        tags=["lab1", "base-session"],
        config=vars(args),
    )

    dataset = CIFARDatasetFSCIL(root=args.data_dir, seed=args.seed)
    train_set, test_set = dataset.get_session_data(session=0)

    train_loader = DataLoader(
        train_set,
        batch_size=args.batch_size,
        shuffle=True,
        num_workers=2,
        pin_memory=True,
    )
    test_loader = DataLoader(
        test_set,
        batch_size=args.batch_size,
        shuffle=False,
        num_workers=2,
        pin_memory=True,
    )

    model = ResNet20CIFAR(num_classes=100, tau=args.tau).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(
        model.parameters(), lr=args.lr, momentum=0.9, weight_decay=5e-4
    )
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer, T_max=args.epochs
    )

    os.makedirs(args.save_dir, exist_ok=True)
    best_acc = 0.0
    best_path = os.path.join(args.save_dir, "base_model.pth")

    for epoch in range(1, args.epochs + 1):
        model.train()
        running_loss, correct, total = 0.0, 0, 0

        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)

            # 4 bước chuẩn của vòng lặp huấn luyện PyTorch
            optimizer.zero_grad()
            logits = model(images, active_classes=60)
            loss = criterion(logits, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * labels.size(0)
            correct += (logits.argmax(dim=1) == labels).sum().item()
            total += labels.size(0)

        scheduler.step()
        train_loss = running_loss / total
        train_acc = (correct / total) * 100.0
        test_acc = evaluate_base(model, test_loader, device, num_classes=60)

        if test_acc > best_acc:
            best_acc = test_acc
            torch.save(model.state_dict(), best_path)

        wandb.log({
            "epoch": epoch,
            "train/loss": train_loss,
            "train/acc": train_acc,
            "val/base_acc": test_acc,
            "lr": scheduler.get_last_lr()[0],
        })

        if epoch % 10 == 0 or epoch == 1:
            print(
                f"Epoch [{epoch:03d}/{args.epochs}] "
                f"Loss: {train_loss:.4f} | Train Acc: {train_acc:.2f}% | Test Acc: {test_acc:.2f}%"
            )

    wandb.summary["best_base_acc"] = round(best_acc, 4)
    wandb.finish()
    print(f"Hoàn tất Session 0! Best Base Acc: {best_acc:.2f}% | Lưu tại: {best_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Train Base Session (Session 0) for TEEN on CIFAR-100"
    )
    parser.add_argument("--data_dir", type=str, default="/content/data")
    parser.add_argument(
        "--save_dir",
        type=str,
        default="/content/drive/MyDrive/IntroML_TEEN/checkpoints",
    )
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--batch_size", type=int, default=256)
    parser.add_argument("--lr", type=float, default=0.1)
    parser.add_argument("--tau", type=float, default=16.0)
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--wandb_entity", type=str, default=None)
    parser.add_argument("--wandb_project", type=str, default="Intro2ML-Group05")
    args = parser.parse_args()
    train_base_session(args) 
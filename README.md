# Few-Shot Class-Incremental Learning via Training-Free Prototype Calibration (TEEN) — Clean-Room Reproduction

Kho mã nguồn tái lập thực nghiệm độc lập (*clean-room implementation*) cho đồ án môn **Nhập môn Học máy (Introduction to Machine Learning)** — **Nhóm 05** (Nguyễn Hoàng Long & Trần Gia Hiên).

- **Bài báo mục tiêu (IEEE):** Q.-W. Wang, D.-W. Zhou, Y.-K. Zhang, D.-C. Zhan, and H.-J. Ye, "Few-Shot Class-Incremental Learning via Training-Free Prototype Calibration," in *Advances in Neural Information Processing Systems (NeurIPS)*, vol. 36, 2023.
- **Dự án Weights & Biases công khai:** [https://wandb.ai/tghien/Intro2ML-Group05](https://wandb.ai/tghien/Intro2ML-Group05)
- **Mã nguồn gốc của tác giả (chỉ dùng để đối chiếu phân kỳ):** [https://github.com/wangkiw/TEEN](https://github.com/wangkiw/TEEN)

---

## 1. Tuyên bố Phạm vi Thực nghiệm (Core Scope Declaration)

Theo quy định của Lab 1 (*Reproduction*), nhóm lựa chọn phạm vi **Core Scope** nhằm kiểm chứng sâu bản chất toán học của cơ chế hiệu chuẩn prototype không huấn luyện lại (*training-free calibration*):

1. **Tái lập trọn vẹn trên chuẩn CIFAR-100 (Section 6.1.1 & Appendix C.1):**
   - Kiến trúc **ResNet-20** ($d = 64$) kết hợp **Cosine Classifier** không bias ($\tau = 16.0$).
   - Giao thức FSCIL gồm **Session 0 (Base Session)** với 60 lớp cơ sở (500 ảnh train/lớp, 100 ảnh test/lớp) và **8 Incremental Sessions (Session 1–8)** theo chuẩn **5-way 5-shot** (mỗi phiên thêm 5 lớp mới $\times$ 5 ảnh mẫu, đánh giá tích lũy trên toàn bộ $60 + 5s$ lớp đã gặp).
   - Hiệu chuẩn prototype lớp mới bằng tổ hợp lồi với siêu tham số mặc định của CIFAR-100: $\alpha = 0.1, \tau = 16.0$ (Equations 1, 5, 6, 7).
2. **Thực nghiệm mở rộng — Khảo sát độ nhạy siêu tham số (Section 6.3, Figure 5):**
   - Quét lưới 40 tổ hợp $\alpha \in \{0.0, 0.1, 0.2, \dots, 0.9\}$ (gồm mốc đối chứng $\alpha = 0.0$ không hiệu chuẩn) và $\tau \in \{8, 16, 32, 64\}$ để đánh giá sự đánh đổi giữa độ chính xác lớp cơ sở (`BAcc`) và lớp mới (`NAcc`, `HMean`).

---

## 2. Cấu trúc Kho lưu trữ (Repository Structure)

```text
├── README.md                    # Tài liệu dự án, Core Scope, Mapping Table & Deviation Analysis
├── requirements.txt             # Danh sách thư viện chuẩn (Python >= 3.9, PyTorch, W&B)
├── .gitignore                   # Bỏ qua checkpoints nặng, dữ liệu cục bộ, cache
├── notebooks/
│   └── reproduction_demo.ipynb  # Notebook Google Colab chạy kiểm thử pipeline từ đầu đến cuối
├── slides/
│   ├── final_submission.pptx    # Slide Deck chính thức (M2 + Lab 1, 28 slides, < 20 MB)
│   └── assets/                  # 100% sơ đồ lý thuyết tự vẽ (.png/.svg)
└── src/
    ├── __init__.py
    ├── utils.py                 # Cố định hạt giống ngẫu nhiên (seed=2026) & bộ 5 thước đo FSCIL
    ├── dataset.py               # Tải và chia CIFAR-100 (60 Base + 8x 5-way 5-shot)
    ├── models.py                # ResNet-20 cho CIFAR-100 (He et al., CVPR 2016) + Cosine Classifier
    ├── calibration.py           # Tự cài đặt Equations (1), (5), (6), (7) của TEEN từ đầu
    ├── train_base.py            # Huấn luyện Session 0 (100 epochs, SGD + CosineAnnealingLR) & log W&B
    ├── eval_incremental.py      # Đóng băng backbone, đánh giá Session 0..8 & log W&B
    └── sweep_alpha.py           # Quét lưới siêu tham số (alpha, tau) tái hiện Figure 5 & log W&B

```
## 3. Hướng dẫn Cài đặt & Tái lập Thực nghiệm

### 3.1. Môi trường yêu cầu

- Python $\ge 3.9$, GPU CUDA (khuyến nghị Google Colab T4).
- Không sử dụng thư viện ngoài đặc thù; toàn bộ phụ thuộc tiêu chuẩn (`torch`, `torchvision`, `numpy`, `wandb`, `matplotlib`) nằm trong `requirements.txt`.

```bash
git clone https://github.com/famevease/Intro2ML_Adopt-ML-paper.git
cd Intro2ML_Adopt-ML-paper
pip install -r requirements.txt
wandb login
```

### 3.2. Thực thi tuần tự các bước thực nghiệm

Tất cả lượt chạy đều cố định hạt giống `--seed 2026` (`random`, `numpy`, `torch`, `cudnn.deterministic = True`) để đảm bảo tính lặp lại (*repeatability*):

```bash
# Bước 1: Huấn luyện Base Session (Session 0 — 60 lớp cơ sở, 100 epochs)
python -m src.train_base \
    --data_dir /content/data \
    --save_dir ./checkpoints \
    --epochs 100 --batch_size 256 --lr 0.1 --tau 16.0 --seed 2026

# Bước 2: Đánh giá 8 Incremental Sessions (Session 0..8, alpha=0.1, tau=16.0)
python -m src.eval_incremental \
    --data_dir /content/data \
    --ckpt_path ./checkpoints/base_model.pth \
    --alpha 0.1 --tau 16.0 --seed 2026

# Bước 3: Quét độ nhạy siêu tham số (40 tổ hợp alpha x tau)
python -m src.sweep_alpha \
    --data_dir /content/data \
    --ckpt_path ./checkpoints/base_model.pth \
    --seed 2026

```

---

## 4. Bảng Ánh xạ Thực nghiệm (W&B Mapping Table)

| Thực nghiệm | Script / Notebook | Liên kết W&B Run (Public) | Tóm tắt kết quả chứng minh |
| --- | --- | --- | --- |
| **Base Session (Session 0)** | `src/train_base.py` | [base-session-resnet20-seed2026](https://wandb.ai/tghien/Intro2ML-Group05/runs/7p556r1c) | Huấn luyện ResNet-20 hội tụ ổn định sau 100 epochs trên 60 lớp cơ sở, đạt `Best Base Acc = 71.73%` (trọng số SGD) và `70.67%` sau khi đồng nhất thành 60 empirical prototypes. |
| **Incremental FSCIL (Session 0–8)** | `src/eval_incremental.py` | [incremental-teen-alpha0.1-tau16.0-seed2026](https://wandb.ai/tghien/Intro2ML-Group05/runs/mq51zgks) | Đánh giá tăng dần không huấn luyện lại ($\alpha=0.1, \tau=16.0$): đạt `Session 8 AvgAcc = 45.07%`, giữ vững `BAcc = 67.15%` (chỉ giảm 3.52% qua 8 phiên), `NAcc = 11.95%`, `HMean = 20.29%`, `PD = 25.60%`. |
| **Sensitivity Sweep ($\alpha, \tau$)** | `src/sweep_alpha.py` | [ablation-alpha-tau-seed2026](https://wandb.ai/tghien/Intro2ML-Group05/runs/phq5eqnt) | Quét 40 tổ hợp $\alpha \in [0.0, 0.9]$ và $\tau \in \{8, 16, 32, 64\}$ tại Session 8 (đối chiếu Section 6.3, Figure 5) — `tau=16.0, alpha=0.7 -> AvgAcc=43.72%, NAcc=14.68%, HMean=23.81%`. |

---

## 5. Đối chiếu Kết quả & Phân tích Sai lệch (Comparison & Deviation Analysis)

### 5.1. Bảng so sánh 3 chiều qua 9 phiên trên CIFAR-100

| Session | Số lớp | Paper gốc (Table 6, RTX 3090) | Repo gốc `wangkiw/TEEN` (Colab T4, 600ep) | Clean-room Nhóm 05 (`mq51zgks`, Colab T4) | Chênh lệch vs. Paper (%) | Sai lệch tương đối (%) | Rebuild BAcc (%) | Rebuild NAcc (%) | Rebuild HMean (%) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 60 | 74.92% | `[ĐIỀN TỪ LOG]` | **70.67%** | -4.25 | -5.67% | 70.67 | — | — |
| 1 | 65 | 72.65% | `[ĐIỀN TỪ LOG]` | **66.15%** | -6.50 | -8.95% | 69.92 | 21.00 | 32.30 |
| 2 | 70 | 68.74% | `[ĐIỀN TỪ LOG]` | **62.09%** | -6.65 | -9.67% | 69.48 | 17.70 | 28.21 |
| 3 | 75 | 65.01% | `[ĐIỀN TỪ LOG]` | **58.00%** | -7.01 | -10.78% | 69.15 | 13.40 | 22.45 |
| 4 | 80 | 62.01% | `[ĐIỀN TỪ LOG]` | **54.60%** | -7.41 | -11.95% | 68.83 | 11.90 | 20.29 |
| 5 | 85 | 59.29% | `[ĐIỀN TỪ LOG]` | **51.89%** | -7.40 | -12.48% | 68.35 | 12.40 | 20.99 |
| 6 | 90 | 57.90% | `[ĐIỀN TỪ LOG]` | **49.66%** | -8.24 | -14.23% | 68.02 | 12.93 | 21.73 |
| 7 | 95 | 54.76% | `[ĐIỀN TỪ LOG]` | **47.28%** | -7.48 | -13.66% | 67.82 | 12.09 | 20.52 |
| 8 | 100 | **52.64%** | `[ĐIỀN TỪ LOG]` | **45.07%** | **-7.57** | **-14.38%** | **67.15** | **11.95** | **20.29** |
| **PD ($\downarrow$)** | — | **22.28%** | `[ĐIỀN TỪ LOG]` | **25.60%** | **+3.32** | **+14.90%** | — | — | — |

### 5.2. Phân tích nguyên nhân phân kỳ giữa Clean-room và Mã nguồn gốc (`wangkiw/TEEN`)

Qua đối chiếu trực tiếp với kho mã nguồn công khai `wangkiw/TEEN` (chạy tách biệt chỉ để kiểm chứng), nhóm xác định chính xác **4 nguyên nhân kỹ thuật** gây ra độ lệch `-4.25%` ngay từ Session 0 và `-7.57%` tại Session 8:

1. **Số vòng lặp huấn luyện Base Session (`600` vs. `100` epochs):** Bài báo gốc (Section 6.1.1 & Appendix C.1) không công bố số epochs cho CIFAR-100; kiểm tra `scripts/cifar.sh` của tác giả cho thấy họ huấn luyện tới **600 epochs** (`-tmax 600`), trong khi bản *clean-room* của nhóm dùng **100 epochs** theo thông lệ chuẩn.
2. **Chiến lược Data Augmentation ẩn (`AutoAugment` vs. cơ bản):** Trong `dataloader/cifar100/cifar.py`, tác giả tích hợp ngầm `CIFAR10Policy` (`AutoAugment`) mà không đề cập trong văn bản bài báo; bản *clean-room* của nhóm chỉ sử dụng `RandomCrop(32, padding=4)` và `RandomHorizontalFlip()`.
3. **Thứ tự chia lớp & biến thiên chọn mẫu 5-shot (*Shot Variance*):** Mã nguồn gốc nạp bộ tệp chỉ số cố định (`data/index_list/cifar100/session_1..9.txt`) kế thừa từ TOPIC/CEC/FACT với `seed=1`, trong khi bản *clean-room* sử dụng thứ tự nhãn `0..99` mặc định của `torchvision` và bốc mẫu ngẫu nhiên theo `seed=2026`.
4. **Môi trường phần cứng & thư viện:** Bài báo thực nghiệm trên GPU NVIDIA RTX 3090 với PyTorch 1.4 / NumPy 1.x, trong khi nhóm thực thi trên Google Colab Tesla T4 với PyTorch 2.x / Python 3.13 / NumPy 2.x.

Dù có độ lệch nền từ Session 0, bản tái lập của nhóm vẫn tái hiện nhất quán hai tính chất cốt lõi của TEEN: (1) triệt tiêu hiện tượng quên thảm khốc khi `BAcc` chỉ giảm `3.52%` xuyên suốt 8 phiên mở rộng, và (2) tốc độ suy giảm hiệu năng `PD = 25.60%` nằm cùng nhóm với `Decoupled-DeepEMD` (`25.34%`) và vượt trội các baseline như `Decoupled-Cosine` (`26.87%`) hay `TOPIC` (`34.73%`) trong Table 6.

Bên cạnh đó, mức `NAcc = 11.95%` (và `HMean = 20.29%`) của nhóm tại Session 8 thấp hơn `-13.18` điểm phần trăm so với mức `NAcc = 25.13%` (`HMean = 37.11%`) được báo cáo tại Appendix C.2, Table 8 của bài báo . Kết quả này phản ánh rõ hiện tượng thiên vị lớp cơ sở (*Base-Class Dominance*, Section 4.1): khi không gian đặc trưng nền 100 epochs (không dùng `AutoAugment`) có độ phân tách thấp hơn, cường độ hiệu chuẩn mặc định $\alpha = 0.1$ chưa đủ mạnh để kéo các mẫu lớp mới thoát khỏi lực hút của 60 lớp cơ sở. Xu hướng đánh đổi giữa `BAcc` và `NAcc`/`HMean` khi tăng dần $\alpha$ được kiểm chứng trực tiếp tại lượt chạy quét siêu tham số `phq5eqnt`.

---

## 6. Cam kết Liêm chính Học thuật (Academic Integrity)

Toàn bộ mã nguồn trong thư mục `src/` được nhóm tự lập trình từ đầu (*clean-room implementation*) dựa trên mô tả toán học và thiết lập thực nghiệm của bài báo TEEN (NeurIPS 2023) và kiến trúc ResNet-20 (He et al., CVPR 2016). Kho mã nguồn gốc `wangkiw/TEEN` chỉ được thực thi tách biệt nhằm đối chiếu kết quả và định lượng nguyên nhân phân kỳ.

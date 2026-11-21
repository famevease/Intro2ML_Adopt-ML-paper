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
## 5. Đối chiếu Thực nghiệm & Phân tích Sai lệch (Deviation Analysis)

### 5.1. Bảng đối chiếu 3 chiều trên CIFAR-100 ($\alpha = 0.1, \tau = 16.0$)

Bảng dưới đây đối chiếu trực tiếp kết quả công bố tại **Table 6 & Table 8 (Appendix C.2)** của bài báo, kết quả thực thi nguyên bản kho mã nguồn chính thức `wangkiw/TEEN` trên hạ tầng Google Colab (NVIDIA L4), và kết quả tái lập độc lập (*clean-room*) của Nhóm 05 (`mq51zgks`):

| Phiên (Session) | Số lớp | Paper gốc (Table 6, RTX 3090) | Repo gốc `wangkiw/TEEN` (Colab L4) | Clean-Room Nhóm 05 (`mq51zgks`, T4) | Chênh lệch (Clean-Room vs. Paper) | Sai lệch tương đối |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Session 0 (Base)** | 60 | `74.92%` | **`76.63%`** | **`70.67%`** | `-4.25` pp | `-5.67%` |
| **Session 1** | 65 | `72.65%` | **`72.29%`** (`BAcc 75.70%`, `NAcc 31.40%`) | **`66.15%`** (`BAcc 69.92%`, `NAcc 21.00%`) | `-6.50` pp | `-8.95%` |
| **Session 2** | 70 | `68.74%` | **`67.99%`** (`BAcc 74.80%`, `NAcc 27.10%`) | **`62.09%`** (`BAcc 69.48%`, `NAcc 17.70%`) | `-6.65` pp | `-9.67%` |
| **Session 3** | 75 | `65.01%` | **`64.00%`** (`BAcc 73.78%`, `NAcc 24.87%`) | **`58.00%`** (`BAcc 69.15%`, `NAcc 13.40%`) | `-7.01` pp | `-10.78%` |
| **Session 4** | 80 | `62.01%` | **`60.73%`** (`BAcc 73.10%`, `NAcc 23.60%`) | **`54.60%`** (`BAcc 68.83%`, `NAcc 11.90%`) | `-7.41` pp | `-11.95%` |
| **Session 5** | 85 | `59.29%` | **`57.86%`** (`BAcc 71.85%`, `NAcc 24.28%`) | **`51.89%`** (`BAcc 68.35%`, `NAcc 12.40%`) | `-7.40` pp | `-12.48%` |
| **Session 6** | 90 | `57.90%` | **`55.67%`** (`BAcc 71.13%`, `NAcc 24.73%`) | **`49.66%`** (`BAcc 68.02%`, `NAcc 12.93%`) | `-8.24` pp | `-14.23%` |
| **Session 7** | 95 | `54.76%` | **`53.13%`** (`BAcc 70.83%`, `NAcc 22.77%`) | **`47.28%`** (`BAcc 67.82%`, `NAcc 12.09%`) | `-7.48` pp | `-13.66%` |
| **Session 8 (Final)** | 100 | `52.64%` | **`51.11%`** (`BAcc 70.25%`, `NAcc 22.40%`) | **`45.07%`** (`BAcc 67.15%`, `NAcc 11.95%`) | **`-7.57` pp** | **`-14.38%`** |
| **PD ($\downarrow$)** | — | **`22.28%`** | **`25.52%`** | **`25.60%`** | `+3.32` pp | `+14.90%` |
| **Session 8 HMean** | 100 | **`37.11%`** *(Table 8)* | **`33.97%`** | **`20.29%`** | `-16.82` pp | `-45.32%` |

*(Ghi chú: Ở Session 0, độ chính xác phân loại tuyến tính SGD của bản clean-room đạt `71.73%` và đạt `70.67%` sau khi đồng nhất 60 trọng số thành 60 Empirical Base Prototypes theo Section 3.2; đối với `wangkiw/TEEN` trên Colab L4, hai mốc tương ứng là `78.37%` và `76.63%`).*

### 5.2. Phân tích định lượng nguyên nhân phân kỳ (2 tầng nguyên nhân)

Việc thực thi độc lập kho gốc `wangkiw/TEEN` trên cùng hạ tầng Colab cho phép tách bạch chính xác tổng độ lệch **`-7.57` điểm phần trăm** (`52.64%` vs. `45.07%`) tại Session 8 thành hai lớp nguyên nhân có kiểm chứng:

1. **Sai số do phần cứng & phiên bản thư viện (`Paper` vs. `wangkiw/TEEN` trên Colab L4: `-1.53` pp):**
   Khi chạy nguyên bản mã nguồn tác giả trên GPU L4 với PyTorch 2.x, độ chính xác cuối đạt **`51.11%`** (so với `52.64%` trong Table 6 trên RTX 3090 với PyTorch 1.4), và các chỉ số phân rã `NAcc = 22.40%`, `HMean = 33.97%` bám sát Table 8 (`25.13%` và `37.11%`). Điều này chứng minh khác biệt phần cứng GPU và seed khởi tạo chỉ gây biến thiên nhỏ quanh mức `1.5` điểm phần trăm.
2. **Tác động của 3 chi tiết cài đặt không nêu trong văn bản bài báo (`wangkiw/TEEN` vs. `Clean-Room Nhóm 05`: `-6.04` pp — chiếm ~80% tổng độ lệch):**
   * **Số vòng lặp huấn luyện Base Session (`600` vs. `100` epochs):** Section 6.1.1 & Appendix C.1 chỉ nêu 400 epochs cho CUB200 và không công bố số epochs cho CIFAR-100; tệp `scripts/cifar.sh` của tác giả huấn luyện tới **600 epochs** (`-tmax 600`), trong khi bản *clean-room* chạy **100 epochs** theo thông lệ chuẩn.
   * **Chiến lược Data Augmentation ẩn (`AutoAugment` vs. cơ bản):** Tệp `dataloader/cifar100/cifar.py` tích hợp ngầm `CIFAR10Policy` (AutoAugment) mà không đề cập trong bài báo; bản *clean-room* chỉ dùng `RandomCrop(32, padding=4)` và `RandomHorizontalFlip()`.
   * **Thứ tự chia lớp & biến thiên chọn mẫu 5-shot (*Shot Variance*):** Mã nguồn gốc nạp bộ tệp chỉ số cố định (`data/index_list/cifar100/session_1..9.txt`) kế thừa từ TOPIC/CEC/FACT với `seed=1`, trong khi bản *clean-room* dùng thứ tự nhãn `0..99` mặc định của `torchvision` và bốc mẫu ngẫu nhiên theo `seed=2026`.

Dù tồn tại khoảng cách nền từ Session 0, bản tái lập *clean-room* của nhóm vẫn tái hiện nhất quán hai đặc tính cốt lõi của TEEN: (1) triệt tiêu hiện tượng quên thảm khốc khi `BAcc` chỉ giảm `3.52` pp xuyên suốt 8 phiên mở rộng, và (2) tốc độ suy giảm hiệu năng `PD = 25.60%` nằm cùng nhóm với Decoupled-DeepEMD (`25.34%`) và vượt trội Decoupled-Cosine (`26.87%`) hay TOPIC (`34.73%`) trong Table 6. Bên cạnh đó, mức `NAcc = 11.95%` tại Session 8 phản ánh rõ hiện tượng thiên vị lớp cơ sở (*Base-Class Dominance*, Section 4.1): khi không gian đặc trưng nền 100 epochs (không dùng AutoAugment) có độ phân tách thấp hơn, cường độ hiệu chuẩn mặc định $\alpha = 0.1$ chưa đủ mạnh để kéo các mẫu lớp mới thoát khỏi lực hút của 60 lớp cơ sở — điều này được kiểm chứng trực tiếp tại lượt chạy quét siêu tham số `phq5eqnt` (đỉnh `HMean = 23.81%` tại $\tau = 16.0, \alpha = 0.7$).

---

## 6. Cam kết Liêm chính Học thuật (Academic Integrity)

Toàn bộ mã nguồn trong thư mục `src/` được nhóm tự lập trình từ đầu (*clean-room implementation*) dựa trên mô tả toán học và thiết lập thực nghiệm của bài báo TEEN (NeurIPS 2023) và kiến trúc ResNet-20 (He et al., CVPR 2016). Kho mã nguồn gốc `wangkiw/TEEN` chỉ được thực thi tách biệt nhằm đối chiếu kết quả và định lượng nguyên nhân phân kỳ.

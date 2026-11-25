# MASTERPLAN & EXECUTION PLAN — GIAI ĐOẠN 2: CRITIQUE (M3), EMPIRICS (LAB 2) & POSTER WORKSHOP

* **Môn học:** Nhập môn Học máy (*Introduction to Machine Learning*)
* **Bài báo mục tiêu:** *Few-Shot Class-Incremental Learning via Training-Free Prototype Calibration* (TEEN, NeurIPS 2023)
* **Nhóm thực hiện:** Nhóm 05
  * **Trần Gia Hiên (Hiên):** Nhóm trưởng — Lead Lý thuyết Phản biện (M3), nhánh *Adaptive Gate Baseline*, Thiết kế Poster A2, Quản trị Repo & Audit
  * **Nguyễn Hoàng Long (Long):** Kỹ thuật trưởng — Lead Mã nguồn & Thực nghiệm Lab 2 (OOD Stress Test, Trade-off & $K$-shot Sweep), Log W&B & Xuất biểu đồ
* **Kho lưu trữ & Theo dõi:**
  * **Weights & Biases (Public):** [https://wandb.ai/tghien/Intro2ML-Group05](https://wandb.ai/tghien/Intro2ML-Group05) *(dùng chung project với Lab 1, gắn tag riêng `lab2`)*
  * **Checkpoint kế thừa từ Lab 1:** `base_model.pth` từ run [`7p556r1c`](https://wandb.ai/tghien/Intro2ML-Group05/runs/7p556r1c) (`seed = 2026`, ResNet-20 trên 60 lớp Base CIFAR-100, centroid acc `70.67%`)
* **Mốc thời gian (10 ngày):**
  * **Khởi động Giai đoạn 2:** `25/11/2026`
  * **Đóng gói hoàn chỉnh (Audit Gate — trước hạn 24h):** `04/12/2026`
  * **Hạn nộp chính thức trên Moodle:** `05/12/2026`
  * **Buổi vấn đáp cuối kỳ (Poster Workshop):** Sau ngày `05/12/2026` vài ngày

---

## I. MỤC TIÊU & QUY CHUẨN BẮT BUỘC ("LUẬT THÉP" GÓI NỘP 2)

### 1. Trọng số đánh giá liên quan
* **Poster (M3 Critique + Lab 2 Empirics): `50%` tổng điểm môn học.**
* **Chất lượng kho mã nguồn, kỷ luật theo dõi W&B & định dạng sản phẩm: `5%` tổng điểm.**
* **Hình thức bảo vệ:** Thi vấn đáp trực tiếp tại **Poster Workshop** — đứng cạnh poster A2, thuyết trình và trả lời câu hỏi của giám khảo.

### 2. Quy chuẩn kỹ thuật của Poster & Thực nghiệm
1. **Định dạng Poster:**
   * **Đúng 1 file `.pptx` duy nhất chứa đúng 1 slide**, kích thước **khổ dọc A2 (Portrait A2: `42.0 cm × 59.4 cm` / `16.54 in × 23.39 in`)**.
   * **Ngôn ngữ trên Poster:** **Tiếng Anh** (đồng bộ với Slide Deck Gói 1 và thuật ngữ bài báo NeurIPS).
   * **Công cụ:** Dựng layout trực tiếp trên PowerPoint; sơ đồ minh họa lý thuyết tự vẽ (Figma/Draw.io/PowerPoint) và biểu đồ thực nghiệm xuất từ `matplotlib` độ phân giải cao (≥ 300 DPI) lưu trong `poster/assets/`. Tuyệt đối không cắt dán hình từ bài báo gốc.
2. **Cấu trúc ghép cặp bắt buộc:**
   * Mốc 3 (*Phản biện lý thuyết*) và Lab 2 (*Thực nghiệm kiểm chứng*) tách bạch về vai trò nhưng **đặt cạnh nhau theo từng cặp Vấn đề 1–1** trên poster: mỗi hạn chế lý thuyết đi liền với bằng chứng đo đạc thực tế của chính hạn chế đó.
   * Đáp ứng đủ tối thiểu: **3 Điểm mạnh** (có bằng chứng từ Reading / Lab 1), **2 Hạn chế lý thuyết** (có thực nghiệm kiểm chứng), và **2 Hướng phát triển tương lai**.
3. **Kỷ luật mã nguồn & W&B:**
   * Tự viết mới hoàn toàn các script Lab 2 trong `src/`, cố định `seed = 2026`, đầy đủ docstrings chuẩn PEP8.
   * Mọi lượt chạy Lab 2 phải log công khai lên `Intro2ML-Group05` với **`tags=["lab2", ...]`**.
   * Mọi con số và biểu đồ trên Poster phải ghi rõ **W&B Run ID / Link** để truy vết trực tiếp.
   * Commit Git đều đặn theo từng đầu việc ("commit early and often"), cập nhật đầy đủ bảng ánh xạ trong `README.md`.

---

## II. TRỤC NỘI DUNG PHẢN BIỆN & THỰC NGHIỆM (2 CẶP CỐT LÕI)

```text
┌───────────────────────────────────────────────────────────────────────────────┐
│                    M3 (THEORY CRITIQUE)  <── 1:1 PAIR ──>  LAB 2 (EMPIRICS)    │
├───────────────────────────────────────────────────────────────────────────────┤
│ 3 Strengths (Backed by Lab 1: 7p556r1c, mq51zgks, phq5eqnt)                   │
├───────────────────────────────────────────────────────────────────────────────┤
│ Limitation 1: Semantic Overlap Assumption    │ Exp 1A: SVHN OOD (32x32 RGB)   │
│ & Softmax Sum-to-One Forcing (No Rejection)  │ Exp 1B: CIFAR-100 Sim-Split    │
├──────────────────────────────────────────────┼────────────────────────────────┤
│ Limitation 2: Base-New Trade-off Paradox     │ Exp 2A: FNR/FPR/TBR/TNR &      │
│ (R->W vs W->R) & Shot-Count Blindness (K)    │         R->W vs W->R Anatomy   │
│                                              │ Exp 2B: K-Shot Sweep (1..50)   │
│                                              │ Exp 2C: Adaptive Gate Baseline │
├──────────────────────────────────────────────┴────────────────────────────────┤
│ 2 Future Directions: (1) Similarity-Gated Adaptive alpha_n                    │
│                      (2) Margin-Preserving / Inter-Session Calibration        │
└───────────────────────────────────────────────────────────────────────────────┘
```

### 1. Ba Điểm mạnh (Strengths — dẫn chứng từ Reading & Lab 1)
1. **Zero Catastrophic Forgetting via Frozen Manifold:** Đóng băng $\phi_\theta$ sau Session 0 giúp bảo toàn gần như nguyên vẹn tri thức cũ — run [`mq51zgks`](https://wandb.ai/tghien/Intro2ML-Group05/runs/mq51zgks) ghi nhận `BAcc` chỉ giảm `3.52` pp (`70.67% → 67.15%`) xuyên suốt 8 phiên mở rộng.
2. **Training-Free & Ultra-Low Incremental Latency:** Hiệu chuẩn đóng-form không lan truyền ngược ($\mathcal{O}(B \cdot d)$ phép toán vector mỗi lớp mới); toàn bộ 8 incremental sessions trên CIFAR-100 hoàn tất trong `~17s` (run `mq51zgks`).
3. **Effective Same-Domain Variance Reduction (James-Stein Shrinkage):** Khi lớp mới cùng miền ngữ nghĩa, tổ hợp lồi cải thiện rõ rệt phân lớp mới và cân bằng Base–New — run [`phq5eqnt`](https://wandb.ai/tghien/Intro2ML-Group05/runs/phq5eqnt) cho thấy tăng $\alpha$ từ `0.0 → 0.7` (tại $\tau = 16$) nâng `NAcc` từ `11.40% → 14.68%` (`+3.28` pp) và `HMean` từ `19.50% → 23.81%`.

### 2. Hai Cặp Hạn chế Lý thuyết (M3) ↔ Thực nghiệm Kiểm chứng (Lab 2)

#### Cặp 1: Giả định Semantic Overlap & Thiếu cơ chế từ chối OOD
* **Phản biện lý thuyết (M3):**
  * **Giả định ngầm:** Eq. (5)–(7) mặc định mọi lớp mới $\mathbf{c}_n$ đều biểu diễn được trong bao lồi của $B$ base prototypes ($\Delta \mathbf{c}_n = \sum_{b=0}^{B-1} w_{b,n}\mathbf{c}_b$).
  * **Thiếu sót toán học:** Softmax (Eq. 6) ép $\sum_{b=0}^{B-1} w_{b,n} = 1$ ngay cả khi mọi độ tương đồng cosine $\cos(\mathbf{c}_n, \mathbf{c}_b)$ đều rất nhỏ hoặc âm; phép chuẩn hóa L2 sau tổ hợp lồi tiếp tục khuếch đại độ lệch góc khi $\|\Delta \mathbf{c}_n\|_2$ nhỏ. *(Ghi chú đọc kỹ văn bản: bài báo không có Theorem/Lemma hình thức nào, đồng thời Eq. (7) trang 7 còn in sót chỉ số $b=0$ khi viết $\sum_{b=1}^{B-1} w_{b,n}c_b$).*
* **Thực nghiệm kiểm chứng (Lab 2 — `src/stress_test_ood.py`, tái sử dụng `base_model.pth`):**
  * **Exp 1A — Cross-Domain OOD Sessions (SVHN):** Dùng checkpoint CIFAR-100 Base (`60` lớp vật thể/tự nhiên), cho các phiên incremental học **10 lớp chữ số đường phố SVHN** (native `32×32` RGB, chia 2 sessions 5-way 5-shot hoặc 5 sessions 2-way 5-shot, lặp nhiều seed support để ổn định). So sánh $\alpha = 0.0$ (Uncalibrated NCM) vs $\alpha \in \{0.1, 0.3, 0.5, 0.7, 0.9\}$.
  * **Exp 1B — Controlled Semantic-Distance Split ngay trong CIFAR-100:** Tính điểm tương đồng cực đại $s_n^{\max} = \max_b \cos(\mathbf{c}_n, \mathbf{c}_b)$ cho 40 lớp mới của CIFAR-100, sắp xếp/nhóm thành các phân đoạn từ *High Semantic Overlap* → *Low Semantic Overlap*, đo độ chênh $\Delta\text{NAcc}(\alpha) = \text{NAcc}(\alpha) - \text{NAcc}(0)$ theo từng mức độ tương đồng.
  * **Giả thuyết kiểm chứng:** Khi độ tương đồng ngữ nghĩa giảm thấp hoặc chuyển sang OOD (SVHN), đường cong hiệu năng của TEEN ($\alpha > 0$) rơi xuống **dưới mức đối chứng $\alpha = 0.0$** (*negative calibration / semantic distortion*).

#### Cặp 2: Nghịch lý Đánh đổi Base–New (`R→W` vs `W→R`) & Mù với cỡ mẫu $K$-shot
* **Phản biện lý thuyết (M3):**
  * **Nghịch lý hình học (Section 4.1 vs Section 5.2):** Section 4.1 chẩn đoán lớp mới hay bị nhận nhầm *vào chính lớp base giống nhất* (TBR cao), nhưng Eq. (7) lại **kéo** prototype lớp mới tiến *gần hơn* tới cụm base giống nhất đó mà không có chứng minh nào cho thấy biên Cosine mới giữ nguyên được tính phân tách cho lớp Base. Thực tế, Table 1 & Fig. 3b của bài báo cho thấy `FNR` tăng mạnh (`13.78% → 18.75%` ở S8) và lỗi `R→W` xảy ra chủ yếu ở Base Class — tức là **đánh đổi trực tiếp Base Accuracy lấy Novel Accuracy**, không phải cải thiện miễn phí.
  * **Mù với cỡ mẫu $K$ ($\alpha$ cố định toàn cục):** Theo thống kê mẫu, phương sai ước lượng thô giảm theo $\text{Cov}(\mathbf{c}_n) = \frac{1}{K}\Sigma_n$. Khi $K$ tăng từ $5 \to 20, 50$, $\mathbf{c}_n$ đã tiến gần tâm thật, nhưng $\alpha$ cố định vẫn ép kéo về base prior $\Delta\mathbf{c}_n$, đưa thêm **chệch hệ thống (bias)** vào ước lượng.
* **Thực nghiệm kiểm chứng (Lab 2 — `src/analyze_tradeoff_shots.py` & `src/adaptive_calibration.py`):**
  * **Exp 2A — Giải phẫu `FNR/FPR`, `TBR/TNR` và `R→W` vs `W→R`:** Bổ sung hàm đo đúng Eq. (2), Eq. (3) và tỷ lệ dịch chuyển dự đoán (`UC`, `W→R` trên New, `R→W` trên Base) trên CIFAR-100 khi quét $\alpha \in \{0.0, 0.1, \dots, 0.9\}$. Vẽ đường cong đánh đổi `Base R→W Loss` vs `Novel W→R Gain`.
  * **Exp 2B — Khảo sát độ nhạy cỡ mẫu $K$-shot ($K \in \{1, 3, 5, 10, 20, 50\}$):** So sánh $\alpha = 0.0$ vs $\alpha \in \{0.1, 0.5, 0.7\}$ khi số ảnh support mỗi lớp mới tăng dần. Chỉ ra điểm giao cắt (crossover point) nơi hiệu chuẩn cố định bắt đầu gây hại cho cả `NAcc` và `AvgAcc`.
  * **Exp 2C — Replacement Baseline (*Similarity-Gated Adaptive $\alpha_n$*):** Cài đặt một biến thể đơn giản không cần train thêm:
    $$\alpha_n = \alpha_0 \cdot \text{clip}\!\left(\frac{s_n^{\max} - \gamma}{1 - \gamma},\, 0,\, 1\right) \cdot \sqrt{\frac{5}{K}}$$
    (với $s_n^{\max} = \max_b \cos(\mathbf{c}_n, \mathbf{c}_b)$ và ngưỡng $\gamma$, hoặc cổng theo entropy của $w_{b,n}$). Chạy đối chiếu trên cả CIFAR-100 và SVHN OOD để chứng minh khả năng triệt tiêu negative transfer của Hướng phát triển 1.

### 3. Hai Hướng phát triển Tương lai (Future Directions)
1. **Similarity-Gated & Sample-Aware Adaptive Calibration ($\alpha_n$):** Tự động điều tiết cường độ kéo theo độ tin cậy ngữ nghĩa ($s_n^{\max}$, entropy của $w_{b,n}$) và cỡ mẫu $K$, cho phép phương pháp tự tắt hiệu chuẩn khi gặp lớp OOD hoặc dữ liệu nhiều shot (được minh họa trực tiếp qua Exp 2C).
2. **Margin-Preserving & Inter-Session Calibration:** Tách thành phần trực giao với vector nối tâm Base gần nhất để giảm `R→W` trên các lớp Base, đồng thời mở rộng tập mỏ neo hiệu chuẩn sang cả các prototype lớp mới đã tích lũy ổn định ở các phiên trước.

---

## III. MA TRẬN PHÂN CÔNG CHÉO CÁNH (HIÊN & LONG)

| Hạng mục | Long (Lead Code & Stress Testing) | Hiên (Nhóm trưởng — M3, Adaptive Baseline & Poster) | Kiểm duyệt chéo |
| :--- | :--- | :--- | :--- |
| **Lý thuyết Phản biện (M3)** | Rà soát công thức toán, kiểm tra lại lỗi Eq. (7) & tính chính xác lập luận hình học. | Viết hoàn chỉnh khung 3 Điểm mạnh, 2 Hạn chế lý thuyết, 2 Hướng phát triển. | Thống nhất thuật ngữ Tiếng Anh dùng trên Poster. |
| **Mã nguồn & W&B (Lab 2)** | Viết `src/stress_test_ood.py` (Exp 1A, 1B) & `src/analyze_tradeoff_shots.py` (Exp 2A, 2B); chạy Colab, log W&B tag `lab2`. | Viết & chạy `src/adaptive_calibration.py` (Exp 2C: Adaptive Gate baseline trên CIFAR-100 + SVHN OOD), log W&B tag `lab2`. | Cả hai kiểm tra `seed=2026`, docstrings PEP8, link W&B public. |
| **Trực quan & Poster A2** | Xuất biểu đồ `matplotlib` 300 DPI cho Exp 1A, 1B, 2A, 2B (gắn Run ID lên chú thích). | Xuất biểu đồ Exp 2C; tự vẽ sơ đồ hình học 2D minh họa OOD & `R→W`; dựng **Poster A2 dọc `.pptx`** (Tiếng Anh). | Kiểm tra bố cục 1-1: M3 bên cạnh Lab 2, không sai số liệu. |
| **Repo & Tài liệu** | Kiểm tra lại lệnh CLI tái lập cho script của mình. | Cập nhật `README.md` (mục Lab 2 + Mapping Table + CLI); chạy Audit Gate ngày `04/12`. | Kiểm tra public link trên trình duyệt ẩn danh trước khi nộp. |

---

## IV. KẾ HOẠCH HÀNH ĐỘNG 10 NGÀY (25/11 – 05/12/2026)

```text
25/11 ── Chặng 1: Chốt M3 & Code Lab 2 (4 ngày) ────────────── 28/11
29/11 ── Chặng 2: Chạy W&B, Vẽ Sơ đồ & Dựng Poster A2 (4 ngày) 02/12
03/12 ── Chặng 3: Rà soát, README & Audit Nộp Bài (2 ngày) ─── 04/12 ── [05/12 DEADLINE]
```

### Chặng 1: Chốt Khung Phản biện M3 & Viết Mã nguồn Lab 2 (`25/11 – 28/11`)
* **Ngày 25/11 (Thứ Tư) — Khởi động & Chốt thiết kế:**
  * [x] *Chung:* Thống nhất 2 cặp M3–Lab 2, xác nhận lại vị trí lưu `base_model.pth` (`7p556r1c`) trên Google Drive/Colab.
  * [ ] *Hiên:* Tạo nhánh/cấu trúc `poster/assets/` trong repo; bắt đầu phác thảo nội dung Tiếng Anh cho 3 Strengths, 2 Limitations, 2 Future Directions.
  * [ ] *Long:* Kiểm tra lại `src/utils.py` và `src/eval_incremental.py` để tái sử dụng chuẩn xác trong script Lab 2.
* **Ngày 26/11 (Thứ Năm) — Viết Script Thực nghiệm 1 (OOD & Semantic Split):**
  * [ ] *Long:* Viết `src/stress_test_ood.py` hỗ trợ nạp `base_model.pth`, chạy incremental với **SVHN** (`torchvision.datasets.SVHN`, 32×32) và **CIFAR-100 Semantic-Distance Split**, log W&B `tags=["lab2", "ood"]`. Commit lên GitHub.
  * [ ] *Hiên:* Hoàn thành bản nháp văn bản M3 (đối chiếu kỹ từng phương trình Eq. 2–7 trong bài báo để bảo đảm không sai ký hiệu).
* **Ngày 27/11 (Thứ Sáu) — Viết Script Thực nghiệm 2 (Trade-off & $K$-shot):**
  * [ ] *Long:* Viết `src/analyze_tradeoff_shots.py` tính đầy đủ `FNR`, `FPR`, `TBR`, `TNR`, `UC`, `W→R`, `R→W` theo $\alpha$, và quét $K \in \{1, 3, 5, 10, 20, 50\}$, log W&B `tags=["lab2", "tradeoff-kshot"]`. Commit lên GitHub.
  * [ ] *Hiên:* Thiết kế khung lưới (wireframe) Poster A2 dọc trên PowerPoint (`42.0 cm × 59.4 cm` Portrait), chia sẵn các ô 1-1 cho Cặp 1 và Cặp 2.
* **Ngày 28/11 (Thứ Bảy) — Viết Adaptive Gate Baseline & Checkpoint Chặng 1:**
  * [ ] *Hiên:* Viết `src/adaptive_calibration.py` cài đặt *Similarity-Gated Adaptive $\alpha_n$* (Exp 2C), tích hợp kiểm thử trên cả CIFAR-100 và SVHN OOD, log W&B `tags=["lab2", "adaptive-gate"]`. Commit lên GitHub.
  * [ ] *Chung (Họp Checkpoint 1 — 30 phút):* Chạy thử toàn bộ 3 script trên Colab GPU để đảm bảo không lỗi đường dẫn/dataset trước khi quét chính thức.

### Chặng 2: Chạy Thực nghiệm Chính thức, Xuất Biểu đồ & Dựng Poster (`29/11 – 02/12`)
* **Ngày 29/11 (Chủ Nhật) — Chạy W&B Thực nghiệm 1 & 2:**
  * [ ] *Long:* Chạy chính thức `src/stress_test_ood.py` (Exp 1A, 1B) và `src/analyze_tradeoff_shots.py` (Exp 2A, 2B) với `seed=2026` (và có thể thêm 3 seeds cho SVHN 5-shot để vẽ error bar). Kiểm tra số liệu lưu sạch trên W&B.
  * [ ] *Hiên:* Chạy chính thức `src/adaptive_calibration.py` (Exp 2C) với `seed=2026` trên cả CIFAR-100 và SVHN OOD; ghi nhận bảng so sánh với TEEN cố định và $\alpha=0.0$.
* **Ngày 30/11 (Thứ Hai) — Xuất Bộ Biểu đồ & Tự vẽ Sơ đồ Lý thuyết:**
  * [ ] *Long:* Viết script/notebook vẽ 4 biểu đồ chuẩn xuất bản (300 DPI, font chữ to rõ để đọc được trên A2, nền trắng, chú thích rõ Run ID W&B) lưu vào `poster/assets/`.
  * [ ] *Hiên:* Tự vẽ 2 sơ đồ minh họa hình học (1: *OOD Vector Distortion under Sum-to-One Softmax*; 2: *Base–New Boundary Encroachment `R→W` vs `W→R`*) bằng Figma/Draw.io/PowerPoint lưu vào `poster/assets/`.
* **Ngày 01/12 (Thứ Ba) — Dựng Poster A2 Dọc Bản Nháp Hoàn chỉnh (v1):**
  * [ ] *Hiên:* Lắp ráp toàn bộ nội dung M3, bảng số liệu, sơ đồ tự vẽ và biểu đồ Lab 2 vào `poster/poster_Group05_TEEN.pptx` (đúng 1 slide A2 Portrait, Tiếng Anh), gắn đầy đủ Run ID / Link W&B và QR Code dẫn tới Repo + W&B.
  * [ ] *Long:* Cung cấp bảng số liệu tóm tắt chính xác đến 2 chữ số thập phân cho từng run Lab 2 và rà soát đối chiếu số liệu trên bản nháp poster.
* **Ngày 02/12 (Thứ Tư) — Checkpoint Chặng 2 (Review Thẩm mỹ & Độ đọc A2):**
  * [ ] *Chung (Họp Checkpoint 2 — 45 phút):* Xuất thử Poster sang PDF và zoom đúng tỷ lệ A2 (hoặc in nháp/đọc trên màn hình lớn ở khoảng cách 1m) để kiểm tra cỡ chữ (tiêu đề ≥ 36–48pt, nội dung ≥ 18–24pt, chú thích ≥ 14pt), tránh chữ quá nhỏ hoặc nhồi nhét quá dày.

### Chặng 3: Tinh chỉnh, Cập nhật README, Audit Gate & Nộp Bài (`03/12 – 05/12`)
* **Ngày 03/12 (Thứ Năm) — Tinh chỉnh Poster & Cập nhật `README.md`:**
  * [ ] *Hiên:* Chỉnh sửa bố cục, khoảng thở (whitespace), căn gióng và rút gọn text trên Poster sau feedback ngày 02/12. Cập nhật `README.md` (thêm phần Lab 2, bảng W&B Mapping Table cho các run Lab 2, hướng dẫn CLI chạy lại từng script).
  * [ ] *Long:* Kiểm tra lại toàn bộ docstrings, `requirements.txt` (nếu có thêm thư viện nào như `seaborn` thì cập nhật, ưu tiên chỉ dùng các thư viện đã có), và xóa file rác/tạm khỏi repo.
* **Ngày 04/12 (Thứ Sáu) — AUDIT GATE & NỘP TRƯỚC HẠN 24 GIỜ:**
  * [ ] *Chung:* Thực hiện đầy đủ Bảng kiểm tra chất lượng (Mục V bên dưới).
  * [ ] *Hiên:* Nộp file `poster/poster_Group05_TEEN.pptx` và link GitHub repo công khai lên Moodle trong ngày `04/12`, chụp ảnh màn hình xác nhận nộp thành công.
* **Ngày 05/12 (Thứ Bảy) — Hạn chót Moodle (Ngày dự phòng & Chuẩn bị Vấn đáp):**
  * [ ] *Chung:* Dự phòng xử lý sự cố kỹ thuật (nếu có). Bắt đầu soạn kịch bản thuyết trình 3–5 phút đứng cạnh Poster và danh sách câu hỏi phản biện giả định cho buổi **Poster Workshop** sau 05/12.

---

## V. BẢNG KIỂM TRA CHẤT LƯỢNG TRƯỚC KHI NỘP (AUDIT GATE — `04/12/2026`)

* [ ] **Định dạng file Poster:** Đúng **1 file `.pptx`** duy nhất, chứa **đúng 1 slide**.
* [ ] **Kích thước chuẩn A2 dọc:** Kiểm tra *Slide Size → Custom* đúng Portrait `42.0 cm × 59.4 cm` (`16.54 in × 23.39 in`).
* [ ] **Đủ tiêu chuẩn M3:** Có ít nhất **3 Điểm mạnh** (dẫn chứng cụ thể), **2 Hạn chế lý thuyết** (lập luận chặt chẽ), và **2 Hướng phát triển tương lai**.
* [ ] **Liên kết 1-1 M3 ↔ Lab 2:** Mỗi hạn chế lý thuyết nằm ngay cạnh biểu đồ/bảng thực nghiệm chứng minh cho chính điểm yếu đó.
* [ ] **Truy vết W&B 100%:** Mọi số liệu Lab 1 & Lab 2 trên poster đều có Run ID / Link dẫn trực tiếp về project công khai `Intro2ML-Group05`; các run Lab 2 có tag riêng (`lab2`).
* [ ] **Tính liêm chính & Thẩm mỹ:** 100% sơ đồ và biểu đồ do nhóm tự vẽ/tự chạy (không cắt dán hình paper), chữ to rõ đọc được ở khoảng cách trình bày poster.
* [ ] **GitHub Repository Public:** Kiểm tra ở trình duyệt ẩn danh thấy repo public, `README.md` có đầy đủ Mapping Table Lab 1 + Lab 2 và lệnh CLI chạy lại được với `seed=2026`.

---

## VI. CHUẨN BỊ CHO POSTER WORKSHOP (SAU `05/12/2026`)

Sau khi nộp bài trên Moodle, hai bạn dành 1–2 buổi luyện tập trả lời 5 câu hỏi "tủ" mà giám khảo thường xoáy sâu:
1. *Tại sao trong Lab 1 bản clean-room chỉ đạt `45.07%` so với `52.64%` của paper, và điều đó có làm thay đổi kết luận ở Lab 2 không?* (Dẫn chứng 2 tầng sai lệch `7p556r1c` vs `wangkiw/TEEN` và chỉ ra `PD = 25.60%` vs `25.52%` hoàn toàn tương đồng).
2. *Tại sao Section 4.1 nói lớp mới bị hút nhầm vào lớp base giống nhất, nhưng Section 5.1 lại kéo prototype lớp mới tiến về chính lớp base đó?* (Giải thích trực giác James-Stein vs đánh đổi `R→W` trên Base như đã đo trong Exp 2A).
3. *Nếu dùng `SVHN` làm OOD cho backbone train trên CIFAR-100, tại sao TEEN tệ hơn cả `alpha = 0.0`?* (Chỉ vào cơ chế Softmax $\sum w_{b,n}=1$ + L2 normalization kéo vector chữ số về cụm vật thể CIFAR-100).
4. *Vì sao khi $K$ tăng lên ($K=20, 50$), hiệu chuẩn cố định của TEEN lại trở nên bất lợi?* (Liên hệ $\text{Cov}(\mathbf{c}_n) = \frac{1}{K}\Sigma_n$ vs Bias-Variance Tradeoff).
5. *Baseline Adaptive Gate (Exp 2C) của nhóm giải quyết vấn đề gì và giới hạn mới của chính nó là gì?* (Chặn được OOD/high-$K$ nhờ cổng tương đồng, nhưng vẫn phụ thuộc vào ngưỡng chọn hoặc chất lượng không gian cosine của backbone Session 0).

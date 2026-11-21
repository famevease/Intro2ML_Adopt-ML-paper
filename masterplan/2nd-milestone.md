# MASTERPLAN & DETAILED EXECUTION PLAN: DỰ ÁN HỌC MÁY (FSCIL - TEEN)

* **Môn học:** Nhập môn Học máy (Introduction to Machine Learning)
* **Chủ đề lớn:** Never-Ending Learning / Continual Learning
* **Bài báo mục tiêu:** *Few-Shot Class-Incremental Learning via Training-Free Prototype Calibration* (TEEN)
* **Hội nghị & Thời gian:** NeurIPS 2023 (Kỷ yếu xuất bản 12/2023, CORE A*)
* **Tác giả:** Qi-Wei Wang, Da-Wei Zhou, Yi-Kai Zhang, De-Chuan Zhan, Han-Jia Ye (Đại học Nam Kinh / LAMDA)
* **Nhóm thực hiện:** Nhóm 05 (Team 05)
  * **Nguyễn Hoàng Long (Long):** Kỹ thuật trưởng (Lead Code, Pipeline Tái lập & Thực nghiệm Lab 1)
  * **Trần Gia Hiên (Hiên):** Trưởng nhóm Nội dung (Lead Slide Deck, Lý thuyết M2, Quản trị Repo & Phân tích)
* **Hạn nộp Gói 1 (Slide Deck + Lab 1):** 21/11 *(Mục tiêu đóng gói hoàn chỉnh: 20/11)*

---

## I. TỔNG QUAN DỰ ÁN & TIÊU CHÍ ĐÁNH GIÁ BẮT BUỘC

### 1. Phân bổ trọng số điểm môn học
* **Gói nộp 1 (45% tổng điểm) — Deadline 21/11:**
  * **Milestone 2 (M2 - Reading):** Đọc hiểu sâu sắc, phân tích bối cảnh, động lực, phương pháp tiền nhiệm, sơ đồ tự vẽ, cơ chế toán học.
  * **Lab 1 (Reproduction):** Tái lập thực nghiệm từ mô tả bài báo, ghi log công khai trên Weights & Biases (W&B), phân tích sai lệch (Deviation Analysis).
  * *Sản phẩm nộp:* **1 file PowerPoint duy nhất (`.pptx`) từ 20 đến 40 slide** kèm Speaker Notes dưới mỗi slide và **Link GitHub Repository công khai**.
* **Gói nộp 2 (50% tổng điểm) — Cuối kỳ:**
  * **Milestone 3 (M3 - Critique):** Phân tích 3 thế mạnh, 2 giới hạn lý thuyết cốt tử, 2 hướng phát triển.
  * **Lab 2 (Empirical Stress Testing):** Thực nghiệm chứng minh điểm yếu (Semantic Independence Failure / OOD).
  * *Sản phẩm nộp:* **1 file Poster duy nhất khổ A2 dọc (`.pptx`)** và tham gia Poster Workshop (Vấn đáp).
* **Kỷ luật học thuật & Chất lượng Repo (5% tổng điểm):**
  * Lịch sử commit đều đặn ("early and often"), code chuẩn PEP8 có docstrings, cố định random seed, nhật ký theo dõi W&B sạch sẽ.

### 2. Quy chuẩn kỹ thuật bắt buộc ("Luật thép")
1. **Quy chuẩn Slide Deck:**
   * Định dạng: File `.pptx`, dung lượng **$< 20\text{ MB}$**, tỷ lệ màn hình **16:9**.
   * Độ dài: Nghiêm ngặt từ **20 đến 40 slide** (ít hơn hoặc nhiều hơn đều bị trừ điểm nặng).
   * Speaker Notes: **100% slide phải có Speaker Notes**, độ dài mỗi slide $\le 500$ từ. Người chấm đọc Slide + Notes để chấm điểm mà không cần mở file PDF của paper.
   * Trích dẫn khoa học: Chuẩn IEEE dạng số `[1]`, `[2]` đặt trực tiếp ở chân trang (footnote) của từng slide trích dẫn. **Không tạo slide tài liệu tham khảo riêng ở cuối**.
   * Hình ảnh & Sơ đồ: **100% sơ đồ kiến trúc, luồng thuật toán phải tự vẽ** (bằng Figma, Draw.io, Canva). Tuyệt đối không chụp màn hình hay cắt dán hình từ paper (vi phạm tính liêm chính học thuật sẽ bị 0 điểm).
2. **Quy chuẩn Mã nguồn & Thực nghiệm:**
   * Ngôn ngữ: Python $\ge 3.9$, PyTorch, NumPy, Scikit-Learn.
   * Tính độc lập: Tự viết lại mã nguồn dựa trên mô tả văn bản và công thức toán của bài báo. Code của tác giả chỉ dùng để đối chiếu và xác định sai lệch, không copy nguyên xi.
   * Experiment Tracking: Mọi lần chạy thực nghiệm đều phải ghi nhận công khai lên **Weights & Biases (W&B)**.
   * Tính tái lập: Cố định seed ngẫu nhiên (`random`, `numpy`, `torch`).

---

## II. MA TRẬN PHÂN CHIA TRÁCH NHIỆM (LONG & HIÊN)

Mô hình làm việc: **Chéo cánh (Cross-functional)** nhằm đảm bảo cả hai thành viên đều nắm vững lý thuyết và thực nghiệm để sẵn sàng vấn đáp.

```text
       ┌─────────────────────────────────────────────────────────────┐
       │                       MASTER WORKFLOW                       │
       └──────────────────────────────┬──────────────────────────────┘
                                      │
              ┌───────────────────────┴───────────────────────┐
              ▼                                               ▼
       [LONG: LEAD CODE]                             [HIÊN: LEAD SLIDE]
  • Bóc tách toán -> Mã giả                     • Khởi tạo Git Repo & Project W&B
  • Viết src/ & module calibration.py           • Dựng Template Slide Deck 16:9
  • Huấn luyện Base Session CIFAR-100           • Tự vẽ Diagrams (slides/assets/)
  • Chạy 8 Incremental Sessions                 • Soạn lý thuyết M2 (Slide 1 - 16)
  • Trích xuất Metrics & Log W&B                • Chạy Sensitivity Sweep (alpha, tau)
              │                                               │
              └───────────────────────┬───────────────────────┘
                                      │
                                      ▼
                        [HỘI TỤ & ĐÓNG GÓI CHUNG]
                 • Bảng phân tích sai lệch (Deviation Table)
                 • Hoàn thiện Speaker Notes (< 500 từ/slide)
                 • Cập nhật Mapping Table trong README.md
                 • Kiểm tra kỹ thuật (.pptx < 20MB, 20-40 slide)
```

| Hạng mục | Long (Lead Code & Tái lập) | Hiên (Lead Slide & Lý thuyết) | Phối hợp / Kiểm duyệt |
| :--- | :--- | :--- | :--- |
| **Lý thuyết & Bối cảnh** | Đọc sâu Section 3 & 4 (Thuật toán chi tiết, phân chia dataset CIFAR-100). | Đọc sâu Section 1 & 2 (Bối cảnh FSCIL, các phương pháp tiền nhiệm và hạn chế). | Cùng thống nhất bảng ký hiệu toán học chung cho slide và code. |
| **Slide Deck (45% điểm)** | Cung cấp số liệu đo được, biểu đồ W&B, soạn Notes phần Thực nghiệm & Sai lệch kỹ thuật. | Thiết kế template chuẩn 16:9, tự vẽ 100% sơ đồ vào `slides/assets/`, soạn Notes phần Lý thuyết. | Rà soát chéo: đảm bảo 100% slide có notes ($\le 500$ từ) và footnote IEEE chuẩn. |
| **Mã nguồn (Lab 1)** | Tự viết module `src/calibration.py`, script train Base session và 8 Incremental sessions trên CIFAR-100. | Chạy thử nghiệm mở rộng: Quét độ nhạy siêu tham số $\alpha \in \{0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9\}$ (với $\alpha = 0.0$ làm mốc đối chứng khi không hiệu chỉnh) và $\tau \in \{8, 16, 32, 64\}$ trên W&B. | Đảm bảo code chạy độc lập, cố định seed, không phụ thuộc code tác giả. |
| **Repo & Báo cáo** | Viết docstrings cho từng hàm, kiểm tra pipeline chạy thông qua `requirements.txt`. | Khởi tạo repo, viết file `README.md` hoàn chỉnh (Mapping Table & Deviation Table). | Kiểm tra tính public của link W&B và link GitHub. |

---

## III. CƠ SỞ KỸ THUẬT BÀI BÁO TEEN (NEURIPS 2023)

### 1. Định nghĩa bài toán FSCIL trên CIFAR-100
* **Base Session (Session 0):** Tập dữ liệu lớn $\mathcal{D}_0$ gồm 60 lớp (nhiều mẫu/lớp). Huấn luyện mạng trích xuất đặc trưng (Backbone ResNet-18/20) để học không gian biểu diễn cơ bản.
* **Incremental Sessions (Session 1 đến 8):** Gồm 8 task liên tiếp, mỗi task đến 5 lớp mới, mỗi lớp chỉ có đúng 5 ảnh mẫu (**5-way 5-shot**).
* **Thách thức:** Cập nhật tham số bằng Gradient Descent sẽ gây hiện tượng **Overfitting** vào 5 mẫu mới và **Catastrophic Forgetting** trên 60 lớp cũ.

### 2. Cơ chế cốt lõi của TEEN (Training-Free Prototype Calibration)
1. **Đóng băng Backbone:** Sau Session 0, đóng băng hoàn toàn mạng trích xuất đặc trưng $f_\theta(\cdot)$. Không dùng thêm bất kỳ bước tối ưu Gradient Descent nào ở các session sau.
2. **Tính Prototype thô (Raw Prototype):** Với lớp mới $n$, trích xuất đặc trưng của 5 ảnh mẫu và lấy trung bình:
   $$\mathbf{c}_n = \frac{1}{5} \sum_{i=1}^5 f_\theta(\mathbf{x}_i^{(n)})$$
3. **Ước lượng Tương quan Ngữ nghĩa (Semantic Similarity):** Đo độ tương đồng Cosine giữa vector tâm lớp mới $\mathbf{c}_n$ với toàn bộ $B$ prototype các lớp base $\mathbf{c}_b$ ($b = 0, \dots, B-1$), nhân với hệ số phóng đại $\tau$ rồi chuẩn hóa qua Softmax theo đúng Equations (5) & (6) của bài báo:
   $$S_{b,n} = \frac{\mathbf{c}_b \cdot \mathbf{c}_n}{\Vert{}\mathbf{c}_b\Vert{}_2 \Vert{}\mathbf{c}_n\Vert{}_2} \cdot \tau, \qquad w_{b,n} = \frac{\exp(S_{b,n})}{\sum_{i=0}^{B-1} \exp(S_{i,n})}$$
   *(Giải thích: Vì $\tau = 16 > 1$, phép nhân $\tau$ giúp phóng đại sự chênh lệch độ tương đồng Cosine trước khi qua Softmax để dồn trọng số vào các lớp base giống nhất; nếu chia cho $16$ sẽ làm phân phối bị san phẳng).*
4. **Hiệu chỉnh Prototype bằng Tổ hợp Lồi (Convex Combination):** Kéo vector tâm lớp mới về phía các lớp base tương đồng để triệt tiêu sai lệch do lấy mẫu ít:
   $$\bar{\mathbf{c}}_n = (1 - \alpha)\mathbf{c}_n + \alpha \sum_{b=0}^{B-1} w_{b,n} \mathbf{c}_b$$
5. **Phân loại (Inference):** Dùng bộ phân loại Nearest Prototype Classifier (khoảng cách Cosine hoặc Euclidean) trên toàn bộ các lớp đã học.

---

## IV. CẤU TRÚC 28 SLIDE POWERPOINT CHI TIẾT (M2 & LAB 1)

Tổng cộng: **28 slide** (thỏa mãn quy chuẩn 20–40 slide).

### PHẦN 1: TỔNG QUAN & BỐI CẢNH (Slide 1 – 4)
* **Slide 1: Tiêu đề & Thông tin Nhóm**
  * *Visual:* Tên bài báo, hội nghị NeurIPS 2023, danh sách tác giả LAMDA, tên thành viên Long & Hiên, link Repo GitHub.
  * *Notes:* Giới thiệu tổng quan đề án, tuyên bố mục tiêu mốc M2 và Lab 1.
* **Slide 2: Bài toán Class-Incremental Learning & Hiện tượng Catastrophic Forgetting**
  * *Visual:* Sơ đồ luồng thời gian: Dữ liệu đến theo đợt $\to$ Mô hình quên kiến thức cũ.
  * *Notes:* Phân tích hiện tượng quên thảm khốc theo góc nhìn dịch chuyển phân phối dữ liệu. Footnote: `[1]` Trích dẫn công trình CIL nền tảng.
* **Slide 3: Thách thức Few-Shot (FSCIL) & Ví dụ Thực tế**
  * *Visual:* Minh họa đối lập: 60 lớp cũ (dữ liệu dồi dào) vs Lớp mới chỉ có 5 bức ảnh mẫu (5-shot). Ví dụ thực tế: Hệ thống nhận diện khuôn mặt điểm danh sinh viên mới.
  * *Notes:* Giải thích tại sao FSCIL là bài toán sống còn trong thực tế khi chi phí thu thập nhãn quá đắt đỏ.
* **Slide 4: Nghịch lý Tối ưu trong FSCIL (Optimization Dilemma)**
  * *Visual:* Đồ thị nghịch lý: Cập nhật Gradient $\to$ Overfitting & Forgetting; Không cập nhật $\to$ Không học được lớp mới.
  * *Notes:* Liên hệ trực tiếp với **Lecture 11 (Overfitting)** và **Lecture 8 (Bias-Variance Tradeoff)**: Khi $N=5$, phương sai bùng nổ nếu tối ưu đạo hàm.

### PHẦN 2: PHÂN TÍCH TIỀN NHIỆM & KHOẢNG TRỐNG (Slide 5 – 8)
* **Slide 5: Tiền nhiệm 1 - Replay Buffer & Knowledge Distillation (iCaRL)**
  * *Visual:* Sơ đồ bộ nhớ đệm lưu ảnh cũ và hàm mất mát chưng cất tri thức.
  * *Notes:* Phân tích nguyên lý và hạn chế: Lưu trữ ảnh vi phạm quyền riêng tư, chưng cất tri thức kém hiệu quả khi lớp mới quá ít ảnh. Footnote: `[2]` Rebuffi et al., CVPR 2017.
* **Slide 6: Tiền nhiệm 2 - Meta-Learning & Đồ thị tri thức (TOPIC, CEC)**
  * *Visual:* Sơ đồ mạng nơ-ron đồ thị (GNN) điều chỉnh trọng số.
  * *Notes:* Hạn chế: Kiến trúc cồng kềnh, chi phí tính toán đạo hàm cấp hai cực lớn, dễ mất ổn định khi số session tăng. Footnote: `[3]` Zhang et al., CVPR 2021.
* **Slide 7: Tiền nhiệm 3 - Nearest Class Mean (NCM) thuần túy**
  * *Visual:* Vector prototype thô bị lệch xa so với tâm phân phối thực tế của lớp.
  * *Notes:* Phân tích lý thuyết: Ước lượng mẫu $N=5$ có sai số phương sai cực lớn, dẫn đến hiện tượng ranh giới phân loại đè lên các lớp cũ tương tự.
* **Slide 8: Khoảng trống Nghiên cứu (The Missing Gap)**
  * *Visual:* Bảng so sánh hạn chế của các tiền nhiệm và khoảng trống: Chưa phương pháp nào tận dụng thông tin ngữ nghĩa sẵn có của Base session một cách trực tiếp mà không cần huấn luyện thêm.
  * *Notes:* Định vị đóng góp của TEEN: Lấp đầy khoảng trống bằng phương pháp Training-free.

### PHẦN 3: TÍNH MỚI & ĐÓNG GÓP CỦA TEEN (Slide 9 – 10)
* **Slide 9: Triết lý Cốt lõi: Training-Free Paradigm**
  * *Visual:* Biểu tượng "Khóa" (Lock) trên backbone sau session 0; khẩu hiệu "Zero Gradient Update".
  * *Notes:* Nhấn mạnh tính đột phá: Biến bài toán học tăng dần từ tối ưu hóa tham số phức tạp thành bài toán hiệu chỉnh hình học vector. Liên hệ **Lecture 17 (Occam's Razor)**.
* **Slide 10: Ba Đóng góp Cốt lõi của Bài báo**
  * *Visual:* 3 khối đóng góp: (1) Khám phá hiện tượng mẫu mới bị nhận nhầm vào lớp base tương đồng, (2) Đề xuất giải pháp hiệu chuẩn training-free, (3) Đạt SOTA trên 3 bộ benchmark chuẩn.
  * *Notes:* Chi tiết hóa từng đóng góp khoa học và giá trị thực tiễn.

### PHẦN 4: PHƯƠNG PHÁP & CƠ CHẾ TOÁN HỌC (Slide 11 – 16)
* **Slide 11: Hệ thống Ký hiệu & Phát biểu Bài toán Hình thức**
  * *Visual:* Bảng tra cứu ký hiệu toán học nhất quán: $\mathcal{D}_0, \mathcal{D}_t, \mathbf{c}, \bar{\mathbf{c}}, \alpha, \tau, f_\theta$.
  * *Notes:* Định nghĩa toán học không gian đặc trưng $\mathbb{R}^d$ và giao thức chia task.
* **Slide 12: Kiến trúc Tổng thể Phương pháp (Overall Pipeline)**
  * *Visual:* **Sơ đồ vector tự vẽ**: Ảnh $\to$ Frozen Backbone $\to$ Raw Prototype $\to$ Semantic Attention Module $\to$ Calibrated Prototype $\to$ Classifier.
  * *Notes:* Đi bộ cùng người đọc qua từng khối xử lý trong không gian vector.
* **Slide 13: Cơ chế Toán học 1 - Ước lượng Prototype Thô & Độ lệch Mẫu**
  * *Visual:* Công thức trung bình cộng mẫu và hình học 2D biểu diễn độ lệch do lấy mẫu ngẫu nhiên (Sampling Bias).
  * *Notes:* Giải thích cặn kẽ tại sao $\mathbf{c}_n$ bị lệch khỏi tâm phân phối khi cỡ mẫu $N=5$.
* **Slide 14: Cơ chế Toán học 2 - Khai phá Tương quan Ngữ nghĩa (Semantic Similarity)**
  * *Visual:* Vòng tròn đo khoảng cách Cosine và công thức phân phối trọng số Softmax với nhiệt độ $\tau$.
  * *Notes:* Phân tích ý nghĩa hình học: Không gian Base class đã học được các thuộc tính thị giác khái quát, cho phép chiếu lớp mới lên tổ hợp các lớp cũ tương đồng.
* **Slide 15: Cơ chế Toán học 3 - Hiệu chỉnh bằng Tổ hợp Lồi (Convex Combination)**
  * *Visual:* Đồ thị vector 2D minh họa phép kéo: $\bar{\mathbf{c}}_n = (1 - \alpha)\mathbf{c}_n + \alpha \sum_{b=0}^{B-1} w_{b,n} \mathbf{c}_b$.
  * *Notes:* Phân tích vai trò của siêu tham số $\alpha \in [0, 1]$. Liên hệ với kỹ thuật co mẫu (Shrinkage estimation) và **Lecture 12 (Regularization)**.
* **Slide 16: Phân tích Độ phức tạp Tính toán (Complexity Story)**
  * *Visual:* Bảng so sánh Big-O về thời gian huấn luyện và bộ nhớ inference giữa TEEN và tiền nhiệm.
  * *Notes:* Chứng minh độ phức tạp huấn luyện ở các session sau là $\mathcal{O}(1)$ về mặt cập nhật mạng và $\mathcal{O}(C_{base} \cdot d)$ về phép toán vector.

### PHẦN 5: THIẾT LẬP THỰC NGHIỆM TÁI LẬP (Slide 17 – 19)
* **Slide 17: Benchmark CIFAR-100 & Giao thức Chia Task**
  * *Visual:* Sơ đồ phân bổ dữ liệu: 60 lớp base (500 ảnh train/lớp) + 8 sessions (mỗi session 5 lớp, 5 ảnh/lớp).
  * *Notes:* Mô tả môi trường thực nghiệm, siêu tham số huấn luyện Base (SGD, Cosine Annealing, 100 epochs, seed cố định).
* **Slide 18: Tuyên bố Lựa chọn Phạm vi (Core Scope Declaration)**
  * *Visual:* Khung tuyên bố Core Scope: Tái lập hoàn chỉnh CIFAR-100 (Session 0–8) + 1 thực nghiệm Sensitivity Sweep với $\alpha$.
  * *Notes:* Biện minh lý do chọn Core Scope: Tập trung kiểm chứng sâu cơ chế hiệu chỉnh prototype và đánh giá tính nhạy cảm của tổ hợp lồi.
* **Slide 19: Kiến trúc Repo GitHub & Tích hợp Weights & Biases (W&B)**
  * *Visual:* Cấu trúc thư mục mã nguồn và giao diện Dashboard W&B theo dõi các run.
  * *Notes:* Trình bày kỷ luật thực nghiệm: 100% metrics được log tự động lên W&B, đảm bảo tính minh bạch và truy vết số liệu.

### PHẦN 6: KẾT QUẢ TÁI LẬP (LAB 1) (Slide 20 – 23)
* **Slide 20: Kết quả Huấn luyện Base Session (Session 0)**
  * *Visual:* Biểu đồ Learning Curves (Loss `train_loss.png` & Accuracy `val_base_acc.png` qua 100 epochs) trích xuất trực tiếp từ W&B.
  * *Notes:* Báo cáo kết quả Session 0: Top-1 Test Accuracy đạt $71.73\%$ ở Epoch 100 (Loss $0.1603$, Train Acc $95.83\%$), chuyển đổi sang NCM centroid đạt $70.67\%$ (so với công bố paper Table 6 là $74.92\%$). Kèm link run W&B.
* **Slide 21: Kết quả Chuỗi 8 Incremental Sessions**
  * *Visual:* Đồ thị đường cong hiệu năng tích lũy từ Session 1 đến 8 (`eval_avg_acc.png`, `eval_base_acc.png`, `eval_newacc.png`, `eval_hmean.png`).
  * *Notes:* Nhận xét xu hướng: Độ chính xác trung bình giảm êm dịu từ $70.67\% \to 45.07\%$, Base Acc giữ vững $67.15\%$ (không bị catastrophic forgetting), Novel Acc duy trì ổn định $12\% \sim 21\%$.
* **Slide 22: Bảng Đối chiếu Toàn diện (Comparison Table)**
  * *Visual:* Biểu đồ suy giảm hiệu năng `eval_pd.png` bên trái kết hợp Bảng số liệu chi tiết 9 session bên phải.
  * *Notes:* Trình bày chi tiết từng con số: Session 8 đạt AvgAcc $45.07\%$, BaseAcc $67.15\%$, NovelAcc $11.95\%$, PD $25.60\%$.
* **Slide 23: Thực nghiệm Mở rộng - Quét Độ nhạy $\alpha$ và $\tau$ (Sensitivity Sweep)**
  * *Visual:* Biểu đồ đường quét độ nhạy `sweep_alpha_tau_fig5.png` và biểu đồ đánh đổi `sweep_tradeoff_tau16.png`.
  * *Notes:* Phân tích kết quả: Khi $\alpha = 0.0$ (không hiệu chỉnh), AvgAcc đạt $45.03\%$; đạt vùng đỉnh tại $\alpha \in [0.1, 0.2]$ ($45.07\% \sim 45.12\%$); NAcc tăng $+3.28\%$ từ $11.40\%$ lên $14.68\%$ ở $\alpha=0.7$; đỉnh HMean $23.81\%$ tại $\alpha=0.7, \tau=16$. Kèm link W&B run `phq5eqnt`.

### PHẦN 7: PHÂN TÍCH SAI LỆCH & ĐỐI CHIẾU MÃ NGUỒN (Slide 24 – 26)
* **Slide 24: Phân tích Sai lệch Kỹ thuật (Deviation Analysis)**
  * *Visual:* Biểu đồ phân rã nguyên nhân gây sai lệch giữa Rebuild và Paper.
  * *Notes:* Giải thích 3 nguồn sai lệch chính: (1) Biến thiên ngẫu nhiên khi bốc 5 ảnh mẫu (shot variance), (2) Khác biệt thư viện tối ưu và phần cứng GPU, (3) Chi tiết data augmentation lúc train base.
* **Slide 25: Đối chiếu với Mã nguồn Gốc của Tác giả (Original Code Divergence)**
  * *Visual:* Sơ đồ luồng đối chiếu code nhóm tự viết vs code repo tác giả.
  * *Notes:* Nêu rõ tính độc lập: Nhóm tự cấu trúc module `calibration.py` rõ ràng theo công thức toán, không phụ thuộc vào các script lồng ghép phức tạp của tác giả.
* **Slide 26: Bản đồ Truy vết Liêm chính (Artifact Mapping)**
  * *Visual:* Bảng ánh xạ: Tên hình ảnh/bảng trên slide $\leftrightarrow$ Script thực thi $\leftrightarrow$ Run ID trên W&B $\leftrightarrow$ Commit Hash trên Git.
  * *Notes:* Khẳng định 100% kết quả là thực nghiệm thật, có thể tái lập lại bằng 1 lệnh duy nhất trong terminal.

### PHẦN 8: TỔNG KẾT & CẦU NỐI M3 / LAB 2 (Slide 27 – 28)
* **Slide 27: Đánh giá Tổng kết Giai đoạn 1**
  * *Visual:* Tóm tắt 3 kết luận chính: Nắm vững lý thuyết, tái lập thành công pipeline TEEN với sai lệch cực nhỏ, làm chủ không gian prototype.
  * *Notes:* Đánh giá tổng quan: TEEN là một giải pháp baseline xuất sắc nhưng dựa trên những giả định lý thuyết cần được kiểm chứng nghiêm ngặt.
* **Slide 28: Cầu nối sang Milestone 3 & Lab 2 (Preview Phản biện)**
  * *Visual:* Minh họa trực quan tình huống sụp đổ: Lớp mới hoàn toàn trực giao / khác biệt ngữ nghĩa với các lớp base (Semantic Independence Failure).
  * *Notes:* Đặt vấn đề cho Poster A2 cuối kỳ: Khi các lớp mới không có tương quan ngữ nghĩa, việc kéo prototype cũ sẽ làm sai lệch không gian biểu diễn như thế nào?

---

## V. KẾ HOẠCH HÀNH ĐỘNG CHI TIẾT TỪNG NGÀY (31/10 – 21/11)

Lộ trình 21 ngày được chia thành 3 giai đoạn nhịp nhàng, tối ưu hóa thời gian cho nhóm 2 người:

```text
31/10 ─── Giai đoạn 1: Khởi động & Khung sườn ─── 06/11
07/11 ─── Giai đoạn 2: Hiện thực Code & Slide  ─── 14/11
15/11 ─── Giai đoạn 3: Phân tích & Đóng gói     ─── 20/11 ─── [21/11 NỘP]
```

### Giai đoạn 1: Đồng bộ hóa & Khởi tạo Khung sườn (31/10 – 06/11)
* **Ngày 31/10 (Thứ 7): Họp khởi động & Thiết lập công cụ**
  - [x] *Chung:* Họp 1 giờ qua Google Meet, thống nhất bài báo TEEN và tuyên bố Core Scope trên CIFAR-100.
  - [x] *Hiên:* Tạo GitHub repo công khai. Tạo project chung trên Weights & Biases (W&B), gửi invite cho Long.
  - [x] *Long:* Thiết lập môi trường ảo Python 3.9+, cài đặt PyTorch và kiểm tra GPU trên Google Colab.
* **Ngày 01/11 (Chủ nhật): Cấu trúc Repo & Template PowerPoint**
  - [x] *Hiên:* Commit cấu trúc thư mục ban đầu (`src/`, `slides/`, `slides/assets/`, `notebooks/`). Dựng template PowerPoint chuẩn 16:9, chèn sẵn ô Speaker Notes và vị trí footnote IEEE.
  - [x] *Long:* Tải mã nguồn gốc của tác giả TEEN về máy, đọc script huấn luyện để ghi nhận các siêu tham số mặc định.
* **Ngày 02/11 (Thứ 2): Dàn ý chi tiết & Bóc tách mã giả**
  - [x] *Hiên:* Soạn dàn ý chi tiết 28 slide vào file `slides/notes.md`.
  - [x] *Long:* Bóc tách công thức Section 3 ra mã giả (pseudocode), xác định danh sách các hàm cần tự viết trong `src/calibration.py`.
* **Ngày 03/11 (Thứ 3): Xử lý Dữ liệu CIFAR-100**
  - [x] *Hiên:* Soạn nội dung và Speaker Notes cho Slide 1 – 4 (Bối cảnh FSCIL, ví dụ thực tế).
  - [x] *Long:* Viết file `src/dataset.py` để tự động tải và chia CIFAR-100 thành 60 lớp base và 8 incremental tasks (5-way 5-shot). Chạy thử repo tác giả để lấy số liệu đối chiếu ban đầu.
* **Ngày 04/11 (Thứ 4): Sơ đồ đầu tiên & Backbone Model**
  - [x] *Hiên:* Tự vẽ sơ đồ 1: Bài toán FSCIL & Hiện tượng Catastrophic Forgetting (vẽ trực tiếp trong slide PowerPoint).
  - [x] *Long:* Viết `src/models.py` dựng mạng ResNet-18/20 chuẩn cho CIFAR-100.
* **Ngày 05/11 (Thứ 5): Soạn Tiền nhiệm & Script Train Base**
  - [x] *Hiên:* Soạn Slide 5 – 8 (Phân tích hạn chế của tiền nhiệm) kèm Speaker Notes chi tiết.
  - [x] *Long:* Viết script huấn luyện Base session `src/train_base.py`, tích hợp ghi log loss và accuracy thời gian thực lên W&B.
* **Ngày 06/11 (Thứ 6): Họp Checkpoint Tuần 1**
  - [x] *Chung:* Rà soát chéo: Repo đã có code tải data sạch; Slide deck đã lên khung xong 8 slide đầu.
### Giai đoạn 2: Hiện thực hóa Thuật toán & Soạn thảo Trọng tâm (07/11 – 14/11)
* **Ngày 07/11 (Thứ 7): Huấn luyện Base Session & Vẽ Sơ đồ TEEN**
  - [x] *Long:* Chạy huấn luyện Base session trên 60 lớp CIFAR-100 (100 epochs, mất ~20 phút trên Colab GPU). Lưu checkpoint weights vào `checkpoints/base_model.pth`. Log W&B đầy đủ.
  - [x] *Hiên:* Dùng Figma/Draw.io vẽ sơ đồ kiến trúc tổng thể TEEN (`slides/assets/teen_pipeline.png`) và sơ đồ kéo vector bằng tổ hợp lồi (`slides/assets/convex_calibration.png`).
* **Ngày 08/11 (Chủ nhật): Tự viết Module Hiệu chuẩn Prototype**
  - [x] *Long:* Tự viết file `src/calibration.py` hoàn chỉnh từ công thức toán học (hàm tính raw prototype, cosine similarity, softmax weights, convex update). Viết docstrings đầy đủ.
  - [x] *Hiên:* Soạn Slide 9 – 12 (Tính mới của TEEN, Overall pipeline, ký hiệu toán học).
* **Ngày 09/11 (Thứ 2): Chạy Incremental Sessions 1 đến 8**
  - [x] *Long:* Viết `src/eval_incremental.py`: Đóng băng backbone, forward 5 ảnh/lớp, gọi hàm hiệu chuẩn từ `calibration.py`, đo Top-1 Accuracy trên toàn bộ các lớp đã học. Chạy xong 8 sessions, log W&B.
  - [x] *Hiên:* Soạn Slide 13 – 16 (Cơ chế toán học, công thức hiệu chuẩn, độ phức tạp $O(1)$) kèm Speaker Notes phân tích cặn kẽ.
* **Ngày 10/11 (Thứ 3): Bàn giao Code & Chuẩn bị Sweep**
  - [x] *Long:* Kiểm tra lại code, đẩy lên nhánh `main`, bàn giao script cho Hiên chạy sweep.
  - [x] *Hiên:* Soạn Slide 17 – 19 (Benchmark CIFAR-100, tuyên bố Core Scope, tích hợp W&B).
* **Ngày 11/11 (Thứ 4): Thực thi Sensitivity Sweep**
  - [x] *Hiên:* Chạy script quét độ nhạy `src/sweep_alpha.py` với $\alpha \in \{0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9\}$ (kèm mốc đối chứng $\alpha = 0.0$ khi không hiệu chỉnh) và $\tau \in \{8, 16, 32, 64\}$, ghi nhận toàn bộ run vào project W&B chung. Xuất biểu đồ kết quả.
  - [x] *Long:* Lập bảng đối chiếu (Comparison Table) giữa số liệu nhóm đo được và số liệu Table 1 trong bài báo gốc.
* **Ngày 12/11 (Thứ 5): Phân tích Sai lệch (Deviation Analysis)**
  - [x] *Long:* So sánh output của code tự viết với output khi chạy code tác giả. Xác định rõ nguyên nhân gây sai lệch.
  - [x] *Hiên:* Đưa biểu đồ Base session và Incremental sessions từ W&B vào Slide 20 – 22.
* **Ngày 13/11 (Thứ 6): Lắp ráp Số liệu & Phân tích vào Slide**
  - [ ] *Hiên:* Đưa biểu đồ Sensitivity Sweep vào Slide 23. Soạn khung Slide 24 – 26 (Phân tích sai lệch, đối chiếu code tác giả).
  - [x] *Long:* Viết bản nháp Speaker Notes cho phần Thực nghiệm và Sai lệch kỹ thuật để Hiên đưa vào slide.
* **Ngày 14/11 (Thứ 7): Họp Checkpoint Tuần 2**
  - [x] *Chung:* Kiểm tra tiến độ: Toàn bộ thực nghiệm Lab 1 đã hoàn thành; slide deck đã có 26 slide hoàn chỉnh; các run W&B hiển thị công khai.

### Giai đoạn 3: Ghép nối, Hoàn thiện Speaker Notes & Đóng gói (15/11 – 20/11)
* **Ngày 15/11 (Chủ nhật): Hoàn thiện Slide 27 - 28 & Cầu nối Lab 2**
  - [ ] *Hiên:* Soạn Slide 27 (Tổng kết) và Slide 28 (Giới thiệu giả định Semantic Overlap để làm bàn đạp cho Milestone 3 & Lab 2 cuối kỳ).
  - [x] *Long:* Rà soát lại toàn bộ code trong repo, đảm bảo mọi hàm đều có docstrings chuẩn và file `requirements.txt` sạch sẽ.
* **Ngày 16/11 (Thứ 2): Tổng rà soát Speaker Notes toàn bộ 28 Slide**
  - [ ] *Hiên:* Đọc từng slide kèm Speaker Notes, biên tập câu chữ mạch lạc, bảo đảm văn phong tự nhiên.
  - [x] *Long:* Kiểm tra tính chính xác của các công thức toán và số liệu thực nghiệm trong Notes, bảo đảm không có slide nào vượt quá 500 từ.
* **Ngày 17/11 (Thứ 3): Kiểm tra Chuẩn Trích dẫn IEEE & Định dạng**
  - [ ] *Hiên:* Rà soát từng slide để bảo đảm có footnote trích dẫn chuẩn IEEE `[X]` ở chân trang. Bảo đảm không có slide references thừa ở cuối.
  - [x] *Long:* Đóng gói Jupyter Notebook hoàn chỉnh `notebooks/reproduction_pipeline.ipynb` cho phép chạy từ đầu đến cuối một cách thông suốt.
* **Ngày 18/11 (Thứ 4): Hoàn thiện README.md của Repository**
  - [ ] *Hiên & Long:* Cập nhật file `README.md` chính thức trên GitHub:
    - [ ] Thông tin nhóm và Citation IEEE của bài báo.
    - [ ] Tuyên bố phạm vi Core Scope.
    - [ ] Bảng Mapping Table đầy đủ (Tên thực nghiệm - Script - Link W&B Run - Kết quả tóm tắt).
    - [ ] Bảng Deviation Table đối chiếu kết quả.
    - [ ] Hướng dẫn chạy mã nguồn chi tiết.
* **Ngày 19/11 (Thứ 5): Kiểm tra Kỹ thuật Nghiêm ngặt (Audit Gate)**
  - [ ] *Chung:*
    - [ ] Đếm lại tổng số slide: Đúng **28 slide** (nằm gọn trong 20 – 40).
    - [ ] Kiểm tra dung lượng file `.pptx`: Phải **dưới 20 MB** (nén ảnh nếu cần).
    - [ ] Kiểm tra link repo trên trình duyệt ẩn danh: Bảo đảm Repo là **Public**.
    - [ ] Kiểm tra link W&B: Bảo đảm Project là **Public**.
* **Ngày 20/11 (Thứ 6): ĐÓNG GÓI VÀ NỘP BÀI (TRƯỚC HẠN 24 GIỜ)**
  - [ ] *Hiên:* Xuất bản file PowerPoint cuối cùng `slides/final_submission_TEEN.pptx`.
  - [ ] *Chung:* Tiến hành nộp file `.pptx` và link GitHub repo lên hệ thống Moodle. Chụp màn hình xác nhận đã nộp thành công.
* **Ngày 21/11 (Thứ 7): Hạn chót Moodle (Buffer Time)**
  - [ ] *Chung:* Ngày dự phòng cho các sự cố kỹ thuật hoặc nghẽn mạng của hệ thống. Nhóm hoàn thành đúng hạn và chuẩn bị cho giai đoạn 2.

---

## VI. CẤU TRÚC KHO LƯU TRỮ (GITHUB REPOSITORY ARCHITECTURE)

```text
├── README.md                  <- Tổng quan dự án, Scope, Mapping Table, Deviation Analysis
├── requirements.txt           <- Danh sách thư viện (torch>=2.0.0, wandb, scikit-learn, etc.)
├── .gitignore                 <- Bỏ qua checkpoints nặng, cache, __pycache__, logs cục bộ
├── slides/
│   ├── final_submission.pptx  <- File thuyết trình chính thức (< 20MB, có Speaker Notes)
│   ├── presentation_v1.pptx   <- Bản nháp slide giai đoạn 1 (minh chứng tiến độ)
│   ├── notes.md               <- Kịch bản nháp Speaker Notes từng slide
│   └── assets/                <- 100% sơ đồ vector tự vẽ (.png, .svg, .drawio)
├── src/
│   ├── __init__.py
│   ├── dataset.py             <- Data loader CIFAR-100 chia base & incremental sessions
│   ├── models.py              <- Backbone ResNet (đóng băng sau session 0)
│   ├── calibration.py         <- Thuật toán hiệu chỉnh prototype cốt lõi tự viết
│   ├── train_base.py          <- Huấn luyện session 0 (60 classes) & log W&B
│   ├── eval_incremental.py    <- Chạy 8 session FSCIL & log W&B
│   ├── sweep_alpha.py         <- Script quét độ nhạy siêu tham số alpha
│   └── utils.py               <- Hàm hỗ trợ, cố định seeds, tính toán metrics
└── notebooks/
    └── reproduction_demo.ipynb<- Notebook Google Colab chạy kiểm thử pipeline từ đầu đến cuối
```

### Quy ước Commit Git ("Commit early and often")
* Không đẩy 1 commit khổng lồ vào ngày cuối.
* Tuân thủ định dạng commit:
  * `feat: implement raw prototype extraction in calibration.py`
  * `train: complete base session training on cifar100 and log to wandb`
  * `docs: add speaker notes for methodology slides 11-16`
  * `assets: add self-drawn fscil framework diagram`
  * `exp: add sensitivity sweep script for alpha calibration`
  * `fix: resolve seed inconsistency in incremental class splitting`

---

## VII. MẪU MAPPING TABLE VÀ DEVIATION TABLE (TRONG README & SLIDE)

### 1. Bảng Ánh xạ Thực nghiệm (Mapping Table)

| Thực nghiệm | Script / Notebook | Link Run W&B | Số liệu tóm tắt | Ghi chú kỹ thuật |
| :--- | :--- | :--- | :--- | :--- |
| **Base Session (60 classes)** | `src/train_base.py` | [base-session-resnet20-seed2026 (7p556r1c)](https://wandb.ai/tghien/Intro2ML-Group05/runs/7p556r1c) | Test Acc: $71.73\%$ (Centroid: $70.67\%$) | ResNet-20, SGD, 100 epochs, Cosine, seed = 2026 |
| **Incremental FSCIL (Sessions 1-8)** | `src/eval_incremental.py` | [incremental-teen-alpha0.1-tau16.0-seed2026 (mq51zgks)](https://wandb.ai/tghien/Intro2ML-Group05/runs/mq51zgks) | S8 AvgAcc: $45.07\%$ | $\alpha = 0.1, \tau = 16$, BaseAcc: $67.15\%$, NovelAcc: $11.95\%$, PD: $25.60\%$ |
| **Sensitivity Sweep ($\alpha \in [0.0, 0.9]$, $\tau \in \{8, 16, 32, 64\}$)** | `src/sweep_alpha.py` | [ablation-alpha-tau-seed2026 (phq5eqnt)](https://wandb.ai/tghien/Intro2ML-Group05/runs/phq5eqnt) | Plateau at $\alpha \in [0.1, 0.2]$ ($45.12\%$) | Quét $\alpha \in [0.0, 0.9]$ và $\tau \in \{8, 16, 32, 64\}$, NAcc gain $+3.28\%$, Best HMean $23.81\%$ |

### 2. Bảng Phân tích Sai lệch (Deviation Analysis Table)

| Session | Kết quả Bài báo (Paper) | Kết quả Nhóm đo (Rebuild) | Sai lệch tương đối (Relative Deviation) | Nguyên nhân phân tích sai lệch |
| :---: | :---: | :---: | :---: | :--- |
| **0 (Base)** | $74.92\%$ | $70.67\%$ | $-5.67\%$ | Base manifold initialization offset (linear test acc: $71.73\% \to$ NCM centroid: $70.67\%$). |
| **Session 1** | $72.65\%$ | $66.15\%$ | $-8.95\%$ | Biến thiên lấy mẫu ngẫu nhiên của 5 bức ảnh mẫu (shot variance). |
| **Session 2** | $68.74\%$ | $62.09\%$ | $-9.67\%$ | Sai lệch góc Cosine nhẹ giữa các prototype lớp mới và mỏ neo base. |
| **Session 4** | $62.01\%$ | $54.60\%$ | $-11.95\%$ | Tác động tích lũy từ Session 0 và biến thiên mẫu CIFAR-100. |
| **Session 8** | $52.64\%$ | $45.07\%$ | $-14.38\%$ | Lệch Session 0 base ($4.25\%$) + noise mẫu few-shot ($2.50\%$) + phần cứng/CUDA ($0.82\%$). |

---

## VIII. BẢNG KIỂM TRA CHẤT LƯỢNG TRƯỚC KHI NỘP (SUBMISSION CHECKLIST)

Trước khi nộp bài trên Moodle vào ngày 20/11, Long và Hiên phải cùng nhau đánh dấu vào từng ô dưới đây:

* [ ] **Định dạng file:** Đúng file PowerPoint `.pptx`.
* [ ] **Dung lượng file:** Dung lượng file `.pptx` $\le 20\text{ MB}$.
* [ ] **Số lượng Slide:** Đúng **28 slide** (nằm nghiêm ngặt trong khoảng 20 đến 40 slide).
* [ ] **Speaker Notes:** 100% slide đều có nội dung Notes bên dưới, không slide nào bị bỏ trống, không slide nào vượt quá 500 từ.
* [ ] **Trích dẫn IEEE:** Các phát biểu và số liệu trích dẫn đều có footnote chuẩn IEEE dạng `[1]`, `[2]` ở chân slide tương ứng; không có slide references thừa ở cuối.
* [ ] **Sơ đồ minh họa:** Toàn bộ sơ đồ luồng phương pháp và bài toán đều là hình ảnh tự vẽ của nhóm lưu tại `slides/assets/`, không dùng hình chụp cắt từ bài báo.
* [ ] **Weights & Biases:** Dự án W&B đã bật chế độ Public; tất cả các biểu đồ trên slide đều dẫn đường link trỏ về run cụ thể.
* [ ] **GitHub Repository:** Repo đã bật chế độ Public; file `README.md` hiển thị đầy đủ thông tin nhóm, Mapping Table, Deviation Analysis và hướng dẫn cài đặt chạy code.
* [ ] **Tính liêm chính học thuật:** Toàn bộ code tái lập trong `src/` được tự viết lại dựa trên mô tả lý thuyết, có cố định hạt giống ngẫu nhiên (`seed`).
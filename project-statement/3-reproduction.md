---
title: "Tái lập thực nghiệm"
short_title: "Tái lập thực nghiệm"
label: intro-ml-lab1-reproduction
description: "Lab tái lập: xây dựng lại các thực nghiệm của bài báo, theo dõi từng lượt chạy và báo cáo mức độ tương đồng giữa kết quả tái lập với kết quả đã công bố."
---

## Mục tiêu

Tái lập thực nghiệm là bài kiểm tra tính trung thực của cả học kỳ. Nhóm xây dựng lại các thực nghiệm của bài báo dựa trên những gì bài báo mô tả, chạy thực nghiệm thực tế và so sánh kết quả đo đạc được với các số liệu đã công bố. Mục tiêu không nhất thiết phải đạt được các con số trùng khớp hoàn hảo. Điều quan trọng cốt lõi là phải chỉ ra chính xác kết quả tái lập cách biệt bao xa và lý giải nguyên nhân tại sao. Việc phân tích sai lệch đó là nơi thể hiện sự hiểu biết sâu sắc về phương pháp, và nó cung cấp nội dung cho phần kết quả trong slide deck nộp cùng [2-paper-reading.md](2-paper-reading.md).

## Lựa chọn phạm vi thực nghiệm

```{important}
Nhóm chọn **một trong hai phạm vi (scope)** dưới đây và nêu rõ lựa chọn cùng lý do giải thích trong slide deck:

- **Phạm vi toàn diện (Full scope):** Tái lập toàn bộ các thực nghiệm chính được báo cáo trong bài báo, trên cùng tập dữ liệu hoặc tập dữ liệu tương đương.
- **Phạm vi cốt lõi (Core scope):** Tái lập tối thiểu hai thực nghiệm quan trọng nhất, bao gồm cả thực nghiệm so sánh chính (headline comparison) của bài báo; phần còn lại được thay thế bằng một phân tích bổ sung do chính nhóm tự thiết kế, chẳng hạn như khảo sát độ nhạy (sensitivity sweep) đối với các cấu hình mà bài báo đã thay đổi.
```

Việc lựa chọn phạm vi là quyết định chuyên môn do chính nhóm chịu trách nhiệm. Một bài báo có khối lượng thực nghiệm quá lớn và nặng nề về mặt tính toán hoàn toàn hợp lý để chọn phạm vi cốt lõi, và phần phân tích bổ sung khi đó sẽ gánh vác vai trò tương đương cho các thực nghiệm đã được lược bớt.

## Quy tắc lập trình và cài đặt

- Hãy tự cài đặt lại **dựa hoàn toàn trên mô tả của bài báo**. Nếu bài báo có công bố mã nguồn mở kèm theo, mã nguồn đó chỉ phục vụ cho việc kiểm chứng và đối chiếu: nhóm có thể đọc, chạy thử và so sánh kết quả đầu ra, nhưng tuyệt đối không được sao chép mã nguồn gốc vào mã của nhóm, và không được nộp mã đó như thể là sản phẩm tự làm.
- Sử dụng Python 3.9 trở lên, cùng các thư viện khoa học tiêu chuẩn: `numpy`, `scipy`, `scikit-learn`, cùng `torch`, `tensorflow` hoặc `jax` nếu bài báo yêu cầu học sâu (deep learning). Bất kỳ thư viện đặc thù nào khác đều phải được giải thích rõ trong file README.
- Cố định hạt giống ngẫu nhiên (random seeds), ghi chép tài liệu rõ ràng và đảm bảo các lượt chạy có tính lặp lại (repeatable). Một lượt chạy thực nghiệm mà không ai có thể tái hiện lại được thì coi như không tồn tại.
- Mọi hàm quan trọng đều phải có docstring mô tả mục đích, tham số đầu vào và giá trị trả về. File README phải giải thích rõ ràng cách thiết lập môi trường và chạy toàn bộ mã nguồn.

## Chạy và theo dõi thực nghiệm

```{note}
Thực nghiệm có thể chạy trên **bất kỳ nền tảng nào do nhóm tự chọn**: máy chủ đám mây (cloud), dịch vụ notebook trực tuyến (Google Colab, Kaggle...) hoặc phần cứng riêng của nhóm. Môn học không bắt buộc một nền tảng cụ thể nào và không yêu cầu lưu trữ bản sao notebook trực tuyến. Yêu cầu bắt buộc là các lượt chạy phải có thật, hoàn tất và được ghi chép đầy đủ, đồng thời **kho mã nguồn được theo dõi (tracked repository)** phải lưu trữ trọn vẹn mọi thứ.
```

- Mọi thực nghiệm phải được ghi nhận trong một dự án công khai trên **Weights & Biases**, nền tảng theo dõi thực nghiệm tại <https://wandb.ai>. Nền tảng này lưu trữ cấu hình, các chỉ số đánh giá (metrics) và đồ thị của từng lượt chạy, giúp slide deck có thể dẫn chứng số liệu của nhóm theo từng lượt chạy cụ thể thay vì chỉ là các con số khẳng định suông. Từ đây về sau, nền tảng này được gọi tắt là W&B.
- File README của kho mã nguồn phải có bảng ánh xạ (mapping table): với mỗi thực nghiệm, nêu rõ notebook hoặc script đã tạo ra nó, liên kết W&B tương ứng của lượt chạy, và một dòng tóm tắt lượt chạy đó chứng minh điều gì.
- Ưu tiên sử dụng các tập dữ liệu đã có sẵn công khai trên Hugging Face hoặc Kaggle hơn là tự lưu trữ các bản sao riêng lẻ. Mã nguồn tiền xử lý dữ liệu phải nằm cùng thư mục với mã thực nghiệm, để quy trình chạy có thể diễn ra trọn vẹn từ đầu đến cuối tại một nơi duy nhất.

## Yêu cầu đối với nội dung kết quả

- **Bảng đối chiếu kết quả (Comparison table):** Đối với mỗi thực nghiệm trong phạm vi đã chọn: ghi rõ số liệu bài báo công bố, số liệu nhóm đo đạc được, và độ lệch tương đối giữa hai kết quả.
- **Phân tích sai lệch (Deviation analysis):** Mọi khoảng cách đáng chú ý đều phải được giải thích cặn kẽ: các cấu hình mà bài báo không nêu rõ, sự khác biệt về thư viện và phiên bản giữa môi trường của bài báo và của nhóm, tác động của khởi tạo ngẫu nhiên, cũng như những giới hạn về mặt phần cứng. Đây chính là phần thể hiện sự khác biệt giữa việc chỉ đơn thuần "bấm nút chạy" và việc thực sự hiểu bản chất thuật toán.
- **So sánh với mã nguồn gốc:** Khi bài báo có cung cấp mã nguồn, nhóm hãy chạy mã đó, so sánh kết quả đầu ra với bản tự cài đặt của nhóm và chỉ ra chính xác vị trí mà hai quy trình có sự phân kỳ.

## Nơi lưu trữ và bàn giao kết quả

Kết quả tái lập thực nghiệm được thể hiện ở hai nơi: Phần kết quả trong slide deck nộp chung của [2-paper-reading.md](2-paper-reading.md) trình bày bảng đối chiếu kết quả và phân tích sai lệch, với mỗi con số của nhóm đều dẫn liên kết tới lượt chạy tương ứng trên W&B. Kho mã nguồn được theo dõi lưu trữ toàn bộ mã nguồn cài đặt, các file notebook và lịch sử commit/nhánh đã tạo ra chúng. Hãy commit sớm và thường xuyên: lịch sử commit là minh chứng công khai ghi nhận toàn bộ quá trình thực hiện công việc của nhóm.

---
title: "Kiểm chứng thực nghiệm"
short_title: "Thực nghiệm kiểm chứng"
label: intro-ml-lab2-empirics
description: "Lab thực nghiệm: thiết kế các thực nghiệm nhằm chứng minh các điểm yếu phát hiện được ở Mốc 3, và đúc kết toàn bộ nội dung phản biện vào một poster duy nhất."
---

## Mục tiêu

Một điểm yếu lý thuyết nếu chỉ dừng lại ở lý lẽ thì chưa đủ thuyết phục. Bài lab này sẽ biến điều đó thành hiện thực hiển hiện. Nhóm sẽ thiết kế và thực hiện các thực nghiệm nhằm biến các điểm yếu đã phát hiện ở [4-critique.md](4-critique.md) từ những lập luận trên giấy thành các số liệu thực tế đo đạc được, sau đó cô đọng toàn bộ nội dung phản biện (cả lý thuyết lẫn thực nghiệm) vào một poster duy nhất để chấm điểm tại buổi poster workshop.

## Thiết kế các thực nghiệm kiểm chứng

Hãy lựa chọn các nhóm thực nghiệm phù hợp với các điểm yếu đã xác định. Danh mục gợi ý dưới đây gồm các dạng thực nghiệm thường mang lại hiệu quả rõ nét nhất:

- **Dữ liệu vi phạm giả định (Assumption-violating data):** Tự tạo hoặc lựa chọn dữ liệu đầu vào vi phạm các giả định mà bài phản biện đã chỉ ra, rồi đo lường chất lượng của phương pháp suy giảm ra sao khi giả định không còn được thỏa mãn. Một đường cong thể hiện sự suy giảm hiệu năng đặt ngay cạnh giả định tương ứng sẽ có sức nặng hơn nhiều trang văn bản.
- **Thiết lập đối kháng và ngoài phân phối (Adversarial and out-of-distribution settings):** Đẩy phương pháp vượt ra khỏi các điều kiện dữ liệu mà bài báo gốc đã đánh giá, và chỉ ra vị trí mà hành vi của phương pháp bắt đầu thay đổi bất thường.
- **Phân rã thành phần (Component ablations):** Loại bỏ hoặc làm suy yếu các thành phần mà lý thuyết cho là nguồn gốc mang lại các đặc tính vượt trội của phương pháp, sau đó quan sát xem những đặc tính nào còn tồn tại.
- **Thay thế bằng giải pháp cơ sở (Replacement baselines):** Thay thế một thành phần được ca ngợi bằng một giải pháp thay thế đơn giản hơn và kiểm tra xem khẳng định của lý thuyết về tính tất yếu của thành phần đó có còn đứng vững hay không.
- **Thực nghiệm về độ mở rộng quy mô (Scaling runs):** Đối chiếu các tuyên bố về độ phức tạp thuật toán với thời gian chạy thực tế trên đồng hồ (wall-clock reality) ở các kích thước dữ liệu mà lý thuyết đã đề cập.
- **Khảo sát độ nhạy (Sensitivity sweeps):** Thay đổi từng núm xoay cấu hình (hyperparameter) tại một thời điểm để phơi bày mức độ nhạy cảm/mong manh của phương pháp trước một yếu tố mà bài báo đã vô tình hoặc hữu ý bỏ qua.

Các quy tắc lập trình và theo dõi thực nghiệm của [3-reproduction.md](3-reproduction.md) được áp dụng trọn vẹn tại đây: tự cài đặt lại từ mô tả, cố định và ghi rõ hạt giống ngẫu nhiên, chạy trên nền tảng do nhóm lựa chọn, và mọi lượt chạy đều phải được theo dõi. Hãy dùng chung dự án W&B công khai nhưng gắn thẻ (tag) các lượt chạy của bài lab này riêng biệt, giúp dễ dàng phân biệt hai bài lab trong nháy mắt.

## Yêu cầu đối với Poster

```{important}
- Poster là **một file `pptx` duy nhất chứa đúng một slide** theo định dạng **khổ dọc A2 (portrait A2)**.
- Poster trực quan hóa các vấn đề mà nhóm đã tìm ra. Phần phân tích lý thuyết nằm ngay cạnh phần kiểm chứng thực nghiệm tương ứng và được liên kết chặt chẽ với nhau: mỗi điểm yếu lý thuyết đi kèm với bằng chứng đo đạc thực tế, theo từng vấn đề một.
- Các số liệu thực nghiệm của nhóm phải dẫn nguồn trực tiếp đến các lượt chạy tương ứng trên W&B. Những khẳng định không thể truy vết đến bằng chứng cụ thể sẽ bị coi là thiếu căn cứ.
- Poster được nộp qua **Moodle**, kèm theo đường dẫn kho mã nguồn hiện có của nhóm.
- Tại buổi workshop (kỳ thi vấn đáp cuối kỳ), nhóm sẽ đứng cạnh poster, thuyết trình trực tiếp từ poster đó và trả lời các câu hỏi của ban giám khảo.
```

Giới hạn trong một trang duy nhất chính là yêu cầu về tính kỷ luật và cô đọng. Mọi thành quả làm việc trong cả học kỳ phải được chắt lọc trên một trang A2 khổ dọc, vì vậy poster chỉ chứa những vấn đề quan trọng nhất cùng bằng chứng chứng minh rõ ràng, hoàn toàn không có chỗ cho những chi tiết trang trí thừa thãi. Slide deck trước đó đã kể câu chuyện toàn diện; poster chính là bản lập luận đúc kết tinh hoa nhất, và buổi workshop là nơi nhóm tự tin bảo vệ công trình của mình trước hội đồng.

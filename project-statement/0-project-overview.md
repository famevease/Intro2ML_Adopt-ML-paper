---
title: "Đồ án môn học: Tổng quan"
short_title: "Tổng quan đồ án"
label: intro-ml-project-index
description: "Tổng quan về đồ án môn học: mỗi nhóm chọn một bài báo khoa học đã xuất bản về học máy và đồng hành cùng bài báo đó qua các giai đoạn chọn đề tài, đọc hiểu, tái lập thực nghiệm, phản biện lý thuyết và kiểm thử thực nghiệm (stress testing)."
---

Đồ án môn học của **Nhập môn Học máy (Introduction to Machine Learning)** yêu cầu mỗi nhóm sinh viên chọn **một bài báo khoa học đã xuất bản về học máy** và nghiên cứu chuyên sâu trong suốt học kỳ. Nhóm sẽ đọc kỹ bài báo cho đến khi có thể diễn giải lại bằng chính lời văn của mình, tái lập lại các thực nghiệm để đánh giá mức độ tin cậy và chuẩn xác của việc tái hiện, đặt câu hỏi phản biện về các phần lý thuyết chưa chặt chẽ, đồng thời chứng minh các điểm yếu phát hiện được thông qua các thực nghiệm do nhóm tự thiết kế. Tiến trình đồ án gồm ba mốc đánh giá (milestone) và hai bài thực hành (lab), mỗi phần đều có trang hướng dẫn riêng, và môn học sẽ kết thúc với buổi vấn đáp / bảo vệ cuối kỳ.

## Buổi vấn đáp cuối kỳ

```{note}
Đồ án kết thúc bằng một buổi thi vấn đáp cuối kỳ dưới hình thức **poster workshop**, thay vì một buổi thuyết trình seminar hay phiên hỏi đáp trực tiếp thông thường. Mỗi nhóm sẽ treo poster của mình, trình bày kết quả công việc của cả học kỳ trực tiếp từ poster đó và trả lời các câu hỏi của giám khảo ngay bên cạnh công trình được tóm lược trên poster.
```

## Lộ trình thực hiện

Các mốc kiểm tra (checkpoint) diễn ra theo thứ tự dưới đây, mỗi mốc đều có một trang tài liệu chi tiết. Các mốc milestone xây dựng nền tảng kiến thức, và các bài lab chuyển hóa kiến thức đó thành các thực nghiệm thực tế:

1. **[1-paper-selection.md](1-paper-selection.md)**: Nhóm đăng ký và xác nhận bài báo của mình bằng cách gửi biểu mẫu lựa chọn (selection form) được công bố trên Moodle.
2. **[2-paper-reading.md](2-paper-reading.md)**: Nhóm đọc hiểu sâu sắc bài báo và nộp nội dung diễn giải lại dưới dạng một slide deck (bộ slide thuyết trình).
3. **[3-reproduction.md](3-reproduction.md)**: Nhóm chạy lại các thực nghiệm trong bài báo và đo lường mức độ tương đồng giữa kết quả tái lập của nhóm với các số liệu đã công bố.
4. **[4-critique.md](4-critique.md)**: Nhóm phản biện lý thuyết của bài báo, từ các giả định đặt ra cho đến phân tích độ phức tạp thuật toán.
5. **[5-empirics.md](5-empirics.md)**: Nhóm chứng minh các điểm yếu đã phát hiện bằng thực nghiệm và đúc kết toàn bộ nội dung phản biện vào một poster duy nhất.

Các mốc kiểm tra được ghép cặp theo sản phẩm bàn giao (deliverable): mốc đọc hiểu (reading milestone) và lab tái lập (reproduction lab) được nộp cùng nhau dưới dạng một slide deck, còn mốc phản biện (critique milestone) và lab thực nghiệm kiểm chứng (empirical-demonstration lab) được nộp cùng nhau dưới dạng một poster.

## Quy định & Tổ chức thực hiện

- Đồ án được thực hiện theo **nhóm**. Biểu mẫu đăng ký sẽ ghi nhận đầy đủ các thành viên, và bài báo đã được xác nhận sẽ gắn liền với nhóm trong suốt học kỳ.
- Mỗi nhóm duy trì **một kho mã nguồn công khai (public code repository)** trong toàn bộ học kỳ. Mã nguồn, notebook và tài liệu phải được tích lũy liên tục từ tuần đầu tiên, và lịch sử commit sẽ phản ánh tiến độ làm việc. Mọi thông tin, số liệu báo cáo trong slide deck và poster đều phải có nguồn gốc truy vết rõ ràng từ kho mã nguồn này.
- Các bài nộp được gửi qua **Moodle**: biểu mẫu đăng ký ở mốc đầu tiên, file slide deck kèm đường dẫn kho mã nguồn tại mốc nộp slide, và file poster tại mốc nộp poster. Hạn nộp tuân theo các thông báo trên Moodle của môn học.
- Các lượt chạy thực nghiệm phải được theo dõi (track) từng lượt trên một dự án công khai tại [Weights & Biases](https://wandb.ai) để mọi số liệu báo cáo trong slide hay poster đều dẫn liên kết trực tiếp tới lượt chạy tương ứng. Quy tắc theo dõi thực nghiệm được quy định cụ thể tại [3-reproduction.md](3-reproduction.md) và áp dụng cho cả hai bài lab.

## Tiêu chí đánh giá

| Phần | Trọng số |
|---|---|
| Biểu mẫu chọn đề tài (Selection form) | Điều kiện tiên quyết (pass/fail), không tính điểm |
| **Slide deck** (kết hợp mốc Đọc hiểu và Lab Tái lập thực nghiệm) | **45%** |
| **Poster** (kết hợp mốc Phản biện lý thuyết và Lab Thực nghiệm chứng minh) | **50%** |
| Chất lượng kho lưu trữ mã nguồn, kỷ luật theo dõi W&B và định dạng sản phẩm | **5%** |
| **Tổng cộng** | **100%** |

Biểu mẫu lựa chọn không có điểm số riêng nhưng là điều kiện tiên quyết (gate) của học kỳ: nhóm chưa đăng ký bài báo sẽ không được chấm điểm sản phẩm về sau. Hai phần được chấm điểm chính tuân theo các mục ở bảng trên. Mục cuối cùng đánh giá tính kỷ luật và tính chuyên nghiệp trong quy trình làm việc xung quanh các sản phẩm bàn giao chứ không chỉ riêng bản thân sản phẩm; do đó, hãy giữ cho kho mã nguồn luôn rõ ràng, dễ đọc, các thực nghiệm được theo dõi đầy đủ và định dạng của cả hai sản phẩm bàn giao luôn chuẩn chỉ, chỉn chu.

Một slide deck xuất sắc cần diễn giải lại bài báo một cách chuẩn xác bằng chính ngôn ngữ của nhóm, trực quan hóa phương pháp một cách trung thực và đối chiếu rõ ràng kết quả tái lập với kết quả bài báo gốc kèm giải thích cho từng sai lệch, đến mức giám khảo có thể hiểu được bài báo làm gì mà không cần mở bài báo gốc ra. Một slide deck diễn giải đúng nhưng trực quan hóa nghèo nàn, hoặc báo cáo sai lệch mà không giải thích nguyên nhân, sẽ bị xem là sản phẩm chưa hoàn thiện. Một poster xuất sắc cần nêu bật được một điểm yếu thực sự, lập luận chặt chẽ về mặt lý thuyết và kiểm chứng bằng thực nghiệm được thiết kế riêng cho điểm yếu đó. Một poster chỉ khẳng định điểm yếu mà không có cơ sở lý thuyết, hoặc đưa ra các thực nghiệm không ăn nhập với điểm yếu được nêu, sẽ biến nỗ lực cả học kỳ thành những ý kiến chủ quan thiếu căn cứ.

## Tính liêm chính học thuật và việc sử dụng AI

Hãy tự cài đặt lại (reimplement) phương pháp được đề xuất từ phần mô tả trong bài báo. Nếu bài báo có công bố mã nguồn mở kèm theo, mã nguồn đó chỉ được dùng cho mục đích đối chiếu và kiểm chứng. Mọi hành vi sao chép văn bản, hình vẽ từ bài báo, sao chép mã nguồn gốc của tác giả, hoặc sao chép bài làm của nhóm khác đều sẽ nhận điểm 0 cho toàn bộ đồ án.

Như thường lệ, các công cụ AI **không bị cấm**: hãy sử dụng chúng một cách thông thái và có trách nhiệm. AI có thể hỗ trợ việc viết tài liệu và lập trình, nhưng từng thành viên phải nắm vững và chịu trách nhiệm về toàn bộ sản phẩm bàn giao tại buổi poster workshop, đồng thời có khả năng giải thích bất kỳ phần nào của công việc tại đó. Giảng viên phụ trách lab có quyền tiến hành các bài đánh giá bổ sung đối với một số nhóm nếu sản phẩm của nhóm cho thấy điều đó là cần thiết.

Định dạng chi tiết của các sản phẩm nộp và các quy định cụ thể được trình bày tại các trang tương ứng: biểu mẫu chọn đề tài tại [1-paper-selection.md](1-paper-selection.md), slide deck tại [2-paper-reading.md](2-paper-reading.md), và poster tại [5-empirics.md](5-empirics.md).

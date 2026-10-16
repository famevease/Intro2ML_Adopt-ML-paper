---
title: "Đọc hiểu bài báo"
short_title: "Đọc hiểu bài báo"
label: intro-ml-m2-reading
description: "Mốc đọc hiểu: tiếp thu sâu sắc bài báo và nộp nội dung diễn giải lại dưới dạng slide deck, kết hợp với câu chuyện tái lập thực nghiệm của Lab 1."
---

## Mục tiêu

Đọc một bài báo khoa học không chỉ dừng lại ở việc đọc hiểu từng câu chữ. Khi kết thúc mốc này, nhóm phải nắm vững kiến thức thực tế đến mức có thể tự tin bảo vệ mà không cần mở file PDF: bài báo giải quyết bài toán gì, lấp đầy khoảng trống nghiên cứu nào, phương pháp đề xuất có điểm gì thực sự mới, phương pháp hoạt động chi tiết ra sao theo từng thành phần, và các tác giả đánh giá nó như thế nào. Mốc này dùng chung sản phẩm bàn giao với [3-reproduction.md](3-reproduction.md): cả hai nộp cùng nhau dưới dạng **một slide deck duy nhất**, trong đó mốc đọc hiểu cung cấp phần diễn giải nội dung lý thuyết và bài lab cung cấp các thực nghiệm đang chạy thực tế.

## Hướng dẫn đọc hiểu

Hãy tiếp cận và phân tích bài báo theo thứ tự dưới đây. Mọi nội dung đều phải được diễn giải lại bằng chính lời văn của nhóm, và phần trình bày phải thuyết phục được người nghe ngay cả khi họ chưa từng đọc qua bài báo đó. Việc trích nguyên văn các câu từ bài báo sẽ không được tính là câu trả lời. Trọng tâm cốt lõi của mốc này chính là sự chuyển hóa kiến thức.

### Bối cảnh và động lực nghiên cứu

- Bài toán mà bài báo giải quyết, được phát biểu một cách rõ ràng, kèm theo một ví dụ cụ thể do chính nhóm tự đưa ra nhằm minh họa lý do bài toán này có ý nghĩa quan trọng trong thực tế.
- Ít nhất hai phương pháp tiền nhiệm mà bài báo kế thừa hoặc phát triển dựa trên đó. Với mỗi phương pháp, hãy nêu rõ: ý tưởng cốt lõi, hạn chế còn tồn tại và hệ quả thực tiễn của hạn chế đó. Một hạn chế nếu không nêu được hệ quả của nó thì chỉ là ghi chú sơ sài, không phải là một phân tích.

### Các đóng góp khoa học

Liệt kê các đóng góp theo đúng thuật ngữ của bài báo, sau đó phân loại lại theo từng nhóm: đóng góp về mặt lý thuyết, đóng góp về mặt kỹ thuật, và đóng góp về mặt thực nghiệm. Tính mới mẻ (novelty) được đánh giá dựa trên sự so sánh với các phương pháp tiền nhiệm ở trên: hãy chỉ rõ đối với từng đóng góp, điều gì trước đây chưa làm được hoặc chưa từng được thử nghiệm.

### Phương pháp đề xuất

Đây là phần trọng tâm kỹ thuật cốt lõi của slide deck. Việc diễn giải lại phương pháp cần bao quát qua 5 tầng nội dung:

- **Ký hiệu và bài toán hình thức (Formal problem):** Diễn đạt lại toàn bộ ký hiệu mà bài báo sử dụng theo một hệ thống ký hiệu nhất quán do nhóm tự quy ước, và phát biểu lại bài toán mà phương pháp giải quyết một cách chặt chẽ, hình thức ở những phần bài báo diễn đạt hình thức.
- **Quy trình tổng thể (Overall pipeline):** Trực quan hóa toàn bộ phương pháp từ đầu đến cuối thông qua một sơ đồ do nhóm tự vẽ và dẫn dắt người đọc theo luồng dữ liệu từ đầu vào đến đầu ra.
- **Chi tiết từng thành phần:** Mỗi thành phần cần trả lời được ba câu hỏi: nó làm nhiệm vụ gì, tại sao phương pháp lại cần nó, và nó hoạt động chính xác như thế nào. Các công thức then chốt phải đi kèm với giải thích chi tiết cho từng biến số, và không nội dung nào trên slide được phép xuất hiện mà thiếu phần giải thích ý nghĩa trong mục ghi chú của người thuyết trình (speaker notes).
- **Các đặc tính lý thuyết:** Diễn giải lại từng bổ đề (lemma), định lý (theorem) hoặc phác thảo chứng minh (proof sketch) mà bài báo khẳng định, đồng thời giải thích ý nghĩa trực quan của chúng. Không bắt buộc phải tái hiện toàn bộ chứng minh toán học, nhưng nhóm bắt buộc phải hiểu rõ những đặc tính đó mang lại điều gì và đâu là giới hạn áp dụng của chúng.
- **Độ phức tạp:** Phân tích độ phức tạp về mặt thời gian và không gian tính toán của phương pháp, đồng thời so sánh với các phương pháp tiền nhiệm đã nêu.

## Sản phẩm bàn giao kết hợp: Slide Deck

Mốc đọc hiểu bài báo và [3-reproduction.md](3-reproduction.md) được nộp chung thành **một slide deck duy nhất**.

- Một file `pptx` có độ dài từ **20 đến 40 slide**, tính toàn bộ: nội dung chính, các slide phụ lục (nếu có), và không có gì khác. Số lượng slide ít hơn thường đồng nghĩa với việc nhóm bỏ qua khâu phân tích; nhiều slide hơn thường là dấu hiệu nhóm chỉ sao chép lại bài báo theo từng phần.
- Slide deck là một sản phẩm trực quan. Nó mô tả lại bài báo bằng hình ảnh trực quan: các đóng góp, tính mới, khoảng trống nghiên cứu cần lấp đầy, phương pháp đề xuất, cùng phương pháp luận về tập dữ liệu, thước đo đánh giá và giao thức thực nghiệm — tất cả đều được thể hiện qua hình vẽ tự thiết kế, sơ đồ và bảng biểu thay vì các đoạn văn bản dài.
- Mỗi slide phải có **speaker notes không quá 500 từ**. Phần ghi chú này chứa đựng những phân tích bằng lời, lập luận và các mối liên kết chặt chẽ mà hình ảnh trực quan không thể chứa hết. Giám khảo sẽ đọc slide dựa trên nội dung ghi chú này. Đồ án không có buổi thuyết trình miệng riêng cho phần này, do đó slide deck kèm theo speaker notes chính là sản phẩm bàn giao hoàn chỉnh.
- Trích dẫn tài liệu theo **chuẩn IEEE, đánh số thứ tự, đặt ở cuối mỗi slide có nội dung trích dẫn**. **Không tạo một slide danh mục tài liệu tham khảo riêng biệt**: mỗi luận điểm phải đứng ngay cạnh nguồn trích dẫn tương ứng trên cùng một trang slide.
- Toàn bộ hình vẽ phải do chính nhóm tự thực hiện. Hãy vẽ lại hoặc tự tái tạo lại bất kỳ nội dung nào xuất hiện trong bài báo. Việc dán trực tiếp hình ảnh gốc từ bài báo sẽ bị tính là hành vi sao chép theo quy định liêm chính học thuật.
- Slide deck kết thúc bằng câu chuyện tái lập thực nghiệm: bảng đối chiếu kết quả của nhóm với kết quả của bài báo gốc, mỗi số liệu của nhóm đều phải trích dẫn kèm liên kết tới lượt chạy tương ứng trên W&B, theo hướng dẫn tại [3-reproduction.md](3-reproduction.md).

```{important}
Slide deck được nộp qua **Moodle dưới dạng một file `pptx` duy nhất có dung lượng dưới 20 MB**, bao gồm đầy đủ speaker notes. Bài nộp phải đính kèm **đường dẫn đến kho mã nguồn công khai được theo dõi (public tracked repository) của nhóm**. Một file slide vượt quá dung lượng cho phép hoặc thiếu đường dẫn kho mã nguồn sẽ khiến bài nộp bị coi là chưa hoàn tất cho đến khi được sửa lại.
```

## Cách thức đánh giá slide deck

Hội đồng chấm thi sẽ mở slide deck, đọc từng slide đối chiếu với phần speaker notes tương ứng, và kiểm tra tính xác thực của nội dung diễn giải so với bài báo gốc tại những điểm nhóm đưa ra khẳng định. Một slide deck chỉ thuật lại bài báo một cách đơn thuần sẽ nhận điểm rất thấp. Một slide deck chứng minh được nhóm đã hiểu sâu sắc, tự vẽ lại quy trình và chạy kiểm thử thực nghiệm thực tế sẽ đạt yêu cầu của mốc này. Những slide chỉ sao chép mã nguồn thô sẽ vi phạm yêu cầu trực quan hóa, và slide không có speaker notes sẽ bị tính là bỏ trống.

---
title: "Phân tích phản biện"
short_title: "Phản biện lý thuyết"
label: intro-ml-m3-analysis
description: "Mốc phản biện: đặt câu hỏi và mổ xẻ phần lý thuyết nền tảng của bài báo. Việc chứng minh các điểm yếu phát hiện được bằng thực nghiệm là nội dung của Lab 2."
---

## Mục tiêu

Sau khi đọc hiểu và tái lập thực nghiệm, nhóm đã nắm vững cách phương pháp hoạt động và kết quả thực nghiệm chỉ ra điều gì. Giờ là lúc nhóm phân định rõ ràng giữa các tuyên bố của tác giả với bằng chứng thực tế. Mốc này **chỉ tập trung phản biện phần lý thuyết**: các giả định nền tảng của phương pháp, tính chặt chẽ của các khẳng định toán học, cách thức xây dựng bài toán và tính thực tế trong phân tích độ phức tạp. Khi phần phản biện tìm ra điểm yếu, việc chứng minh điểm yếu đó bằng thực nghiệm thuộc về nội dung của [5-empirics.md](5-empirics.md) chứ không nằm ở đây, nhờ đó hai nửa của poster cuối kỳ có thể tách biệt một cách rành mạch và rõ ràng.

## Những nội dung cần soi xét kỹ lưỡng

### Các giả định ngầm (Hidden assumptions)

Mọi phương pháp đều đặt ra một số giả định về thế giới thực mà nó vận hành. Hãy tìm ra chúng: hình dạng phân phối dữ liệu mà lý thuyết kỳ vọng, giả định về tính độc lập hoặc cấu trúc giữa các đặc trưng hay các nút mạng, tính sẵn có của toàn bộ dữ liệu hoặc nhãn tại thời điểm huấn luyện, tính trơn (smoothness) mà quá trình tối ưu hóa ngầm đòi hỏi, mô hình tính toán trừu tượng che giấu đi chi phí thực tế mà phần cứng phải gánh chịu. Với mỗi giả định, hãy đặt câu hỏi: dữ liệu thực tế có thường xuyên thỏa mãn nó hay không, và điều gì sẽ xảy ra khi giả định đó bị vi phạm?

### Tính chặt chẽ của các khẳng định

- Lấy các bổ đề (lemmas), định lý (theorems) và các đặc tính đã nêu từ [2-paper-reading.md](2-paper-reading.md) để đối chiếu với phần chứng minh của chúng. Chúng có thực sự đúng như những gì được viết hay không? Các kết luận có bị ràng buộc bởi các giả thuyết mà bài báo chỉ nhắc đến thoáng qua một lần trong một ghi chú nhỏ (remark) hay không?
- Phân biệt rạch ròi giữa các khẳng định được thực nghiệm chứng minh một cách xác thực với các khẳng định chỉ đơn thuần xuất hiện bên cạnh thực nghiệm. Một bảng so sánh kết quả thực nghiệm ấn tượng không đồng nghĩa với việc chứng minh cho mọi câu từ được viết trong phần mở đầu.

### Cách thức xây dựng bài toán và hàm mục tiêu

- Hàm mục tiêu có thực sự nắm bắt được mục tiêu mà bài báo quảng bá hay không? Các phương pháp chỉ tối ưu hóa những gì được hình thức hóa thành toán học, và việc hình thức hóa đó có thể đi chệch khỏi ý đồ ban đầu. Hãy tìm kiếm các lối tắt: các đại lượng xấp xỉ thay thế cho mục tiêu thực sự, các số hạng điều chuẩn (regularizers) có tác dụng phụ mà lý thuyết bỏ qua, hay các hàm mất mát (loss functions) chấp nhận các nghiệm suy biến (degenerate solutions).

### Độ phức tạp và tính tổng quát

- Phân tích độ phức tạp được trình bày ở [2-paper-reading.md](2-paper-reading.md) tuyên bố tốc độ tăng trưởng dựa trên các giả định nhất định. Hãy đặt dấu hỏi cho chúng: tốc độ tăng trưởng được tuyên bố đó có thực sự cạnh tranh trong các trường hợp mà thực nghiệm diễn ra, hay chỉ vượt trội trong những điều kiện lý tưởng có lợi cho phương pháp?
- Đặt câu hỏi về khả năng tổng quát hóa mà bài báo quảng bá: phương pháp có thể mở rộng xa đến đâu ngoài các thiết lập thực nghiệm đã được đánh giá, và lý thuyết có cơ sở nào hỗ trợ cho sự mở rộng đó hay không?

## Cấu trúc của bài phân tích phản biện

Nội dung phân tích đóng vai trò là chất liệu cho hai sản phẩm bàn giao. Các luận điểm lý thuyết sẽ được đưa vào phần lý thuyết của poster ở [5-empirics.md](5-empirics.md), và nội dung phải đáp ứng ba tiêu chuẩn tối thiểu:

- Tối thiểu **ba điểm mạnh (strengths)** của phương pháp, mỗi điểm mạnh đều phải được lập luận bằng chứng cứ rút ra từ quá trình đọc hiểu hoặc tái lập thực nghiệm thay vì chỉ khẳng định suông.
- Tối thiểu **hai hạn chế (limitations)** mà bài báo chưa giải quyết được, mỗi hạn chế đều phải được lập luận chặt chẽ, phải là hạn chế về mặt lý thuyết, và được phát biểu rõ ràng đến mức có thể thiết kế một thực nghiệm để kiểm chứng.
- Tối thiểu **hai hướng phát triển tương lai (future directions)** mà bài báo gợi mở, bắt nguồn từ những phát hiện trong quá trình phản biện.

Một hạn chế được lập luận chặt chẽ ở phần lý thuyết và được chứng minh bằng thực nghiệm ở phần sau sẽ tạo nên trục nội dung đắt giá nhất cho poster. Hơn nữa, phân tích phản biện vẫn giữ nguyên giá trị ngay cả với những bài báo mà nhóm rất tâm đắc: một lời khen có căn cứ và bằng chứng xác thực được đánh giá cao ngang với một lời phê bình được lập luận chặt chẽ.

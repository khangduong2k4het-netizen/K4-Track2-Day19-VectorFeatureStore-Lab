# Reflection — Lab 19

**Tên:** _<Họ Tên>_
**Cohort:** _<A20-K4>_
**Path:** Lite

Trên 50 queries, Precision@10 trung bình của BM25 là 77,8%, semantic 73,2%
và hybrid 78,6%. Với exact, BM25 và hybrid cùng đạt 96,7%, cao hơn semantic
88,7%: các từ kỹ thuật xuất hiện trực tiếp trong tài liệu nên lexical matching
hiệu quả. Với mixed, hybrid đạt 100%, so với BM25 97,0% và semantic 98,5%.
RRF kết hợp hai bảng xếp hạng bằng tổng 1/(60 + rank), với rank bắt đầu từ 1.

Với paraphrase, BM25 đạt 33,3%, semantic 24,0% và hybrid 32,0%. Model
bge-small-en thiên về tiếng Anh nên diễn đạt lại bằng tiếng Việt vẫn là điểm
yếu. Hybrid cải thiện trung bình nhưng không thắng trên mọi loại truy vấn.

Tôi sẽ chọn BM25 khi cần khớp chính xác mã, tên hoặc thuật ngữ và ưu tiên
chi phí, độ trễ thấp. Pure vector phù hợp khi diễn đạt lại là chủ yếu và model
đã được đánh giá tốt trên ngôn ngữ, miền dữ liệu thực tế. Không nên mặc định
hybrid nếu lợi ích đo được không đủ bù chi phí hai retrievers.

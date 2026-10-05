# Bài nộp Lab 19 — NB1–NB4, bản Lite

## Các file cần nộp

- `notebooks/01_embeddings_index.ipynb`
- `notebooks/02_hybrid_search_rrf.ipynb`
- `notebooks/03_search_api_benchmark.ipynb`
- `notebooks/04_feast_feature_store.ipynb`
- `submission/screenshots/01_embeddings_index.png` đến `04_feast_feature_store.png`
- `submission/REFLECTION.md` — điền họ tên và cohort trước khi nộp.

Các notebook giữ nguyên output thực tế. Ảnh PNG là ảnh Chrome chụp các trang
HTML xuất từ output notebook; trang nguồn nằm trong `submission/evidence/`.
Không có số đo được tạo giả hoặc thay bằng kết quả kỳ vọng.

## Kết quả kiểm chứng

| Nội dung | Kết quả |
|---|---|
| NB1 | 1.000 vector, 384 chiều; paraphrase top-5 có 5/5 kết quả cloud |
| NB2 — Precision@10 trung bình | BM25 77,8%; semantic 73,2%; hybrid 78,6% |
| NB2 — mixed | BM25 97,0%; semantic 98,5%; hybrid 100,0% |
| NB3 — hybrid P99 server-side | 44,9 ms, đạt ngưỡng < 50 ms |
| NB4 | 3 feature views, materialize thành công; lookup P99 5,35 ms < 10 ms; PIT join đủ 3 dòng |
| Kiểm tra Lite | `All checks passed` |
| Bộ test | 41 passed |

Kết quả paraphrase của bản Lite: BM25 33,3%, semantic 24,0%, hybrid 32,0%.
Embedding bge-small-en thiên về tiếng Anh; semantic không thắng nhóm này
trong lần đo. Reflection trình bày đúng hạn chế đó. Các số đo latency phụ
thuộc máy và tải hệ thống, nên lần chạy lại có thể khác.

## Các sửa đổi để chạy được trên máy này

- NB3 chọn cổng trống thay vì cố dùng cổng 8000 đang bị ứng dụng khác chiếm;
  khởi động uvicorn bằng Python của kernel, warm-up riêng trước 100 lần đo/mode,
  kiểm tra HTTP status và dọn server sau khi chạy.
- NB4 in danh sách 3 feature views; chọn timestamp truy vấn sau khi profile
  tương ứng đã xuất hiện và kiểm tra PIT join trả đủ 3 dòng. Không dùng giá trị
  tương lai để lấp dữ liệu thiếu.
- `.gitattributes` giữ xuống dòng LF cho shell scripts khi checkout trên Windows.

## Chạy lại

Từ PowerShell:

```powershell
wsl -d Ubuntu-24.04
```

Trong Ubuntu:

```bash
cd /mnt/c/Users/khang/Downloads/gitlabVin/K4-Track2-Day19-VectorFeatureStore-Lab
source .venv/bin/activate
make verify-lite
make test

# Chạy lần lượt, không chạy benchmark đồng thời với tác vụ nặng khác.
for nb in notebooks/0[1-4]*.ipynb; do
  python -m jupyter nbconvert --to notebook --execute --inplace "$nb" \
    --ExecutePreprocessor.timeout=900 || break
done

python scripts/export_core_evidence.py
```

Nếu bắt đầu từ môi trường sạch, chạy `bash setup-lite.sh` trước.
`make benchmark` chạy 5.000 calls/mode; bảng NB3 dùng 100 calls/mode sau warm-up
và đo server-side qua API. Hai bảng có cách đo khác nhau.

Để tạo lại PNG, mở PowerShell tại thư mục dự án rồi chạy:

```powershell
./scripts/render_core_screenshots.ps1
```

Script dùng Chrome cài sẵn và một profile tạm riêng. Có thể đổi trình duyệt
bằng tham số `-ChromePath` nếu Chrome không nằm ở đường dẫn mặc định.

## Nộp lên LMS

1. Điền họ tên/cohort và đọc lại reflection để đảm bảo phản ánh hiểu biết của bạn.
2. Kiểm tra 4 notebook và 4 ảnh. NB5–NB8 không thuộc bài nộp core này.
3. Đưa các file này cùng source của dự án lên repository GitHub của bạn.
   `.env`, `.venv`, model cache và database cục bộ được bỏ qua bởi `.gitignore`.
4. Đặt repository public, dán URL vào LMS Day-19 và giữ public đến khi có điểm.

Chỉ chuẩn bị bài nộp cục bộ; chưa push repository hoặc gửi lên LMS.

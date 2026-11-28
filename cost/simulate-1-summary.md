# Tóm tắt mô phỏng simulate-1@20261128-064255

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| dung_it | 21 | 1 | 1646 | 225 | 0.9 | 2.7 |
| dung_vua | 21 | 2 | 3633 | 535 | 2.0 | 5.9 |
| dung_nhieu | 8 | 3 | 4455 | 691 | 2.4 | 7.5 |

Tỉ lệ đạt dùng để tính: 25/25 (100%) — lượt run-3@20261128-014213

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-3.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (500 người) | Chi phí / tháng — cơ sở (1.000 người) | Chi phí / tháng — cao (30.000 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gemini-3.1-flash-lite (vào 0.25 · ra 1.5 $/1M) | $0.0014 | $0.0014 | $0.00079 | $2.46 | $4.92 | $147.49 | $0.0049 |
| gemini-4-hydrogen (vào 1.5 · ra 7.5 $/1M) | $0.0076 | $0.0076 | $0.0044 | $13.59 | $27.17 | $815.17 | $0.0272 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (1.7) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: gemini-3.1-flash-lite. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/50.

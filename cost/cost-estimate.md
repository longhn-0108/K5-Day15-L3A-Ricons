# Chi phí khi dùng thật

> Điền ở guide bước 4.2, nộp ở CP4 14:30 Thứ Bảy 28/11. Ôn lại: ngày 13, ngày 1, ngày 14 · lab ngày 13, lab ngày 14. Chấm ở rubric R6.
> Số **không điền tay**: điền `cost/personas.yaml` → `python run.py simulate` → chép bảng trong `cost/simulate-N-summary.md` vào đây.
> Lúc build dùng gói miễn phí vẫn tính theo **giá gói trả phí** — đây là chi phí cho lúc đưa vào dùng thật.

## 1. Đầu vào

- **Persona** (`cost/personas.yaml`): 3 kiểu, lấy theo mục "Số lần / tháng của từng kiểu người dùng" trong `spec.md` §2.

  | Persona | Tỉ lệ | Phiên / người / tháng | Lượt hỏi / phiên |
  |---|---|---|---|
  | `dung_it` | 50% | 1,5 | 1 |
  | `dung_vua` | 35% | 3,5 | 2 |
  | `dung_nhieu` | 15% | 7 | 3 |

  Nguồn: `spec.md` §2, nền là tần suất tiêu lố trong phỏng vấn P1 (~2 lần/tháng), P2 (~0,67), P3 (~1) ở `evidence/summary.md`. Số phiên lấy giữa khoảng của §2 (1–2, 3–4, 6–8). Tỉ lệ 50/35/15% và phần cộng thêm ngoài số lần tiêu lố là *(tự ước tính)*.
- **Số người dùng thật** 3 kịch bản: thấp 500 · cơ sở 1.000 · cao 30.000. Nguồn: cơ sở khớp `spec.md` §2 (quy mô thử nghiệm, *tự ước tính*); thấp = một nửa cơ sở *(tự ước tính)*; cao = 1% của "hơn 3 triệu người dùng tính năng Quản lý chi tiêu trên MoMo mỗi tháng" ([blog MoMo](https://www.momo.vn/tai-chinh/blog/app-quan-ly-chi-tieu-5166), đăng 14/10/2026, xem 27/11/2026; số MoMo tự công bố), tỉ lệ 1% *(tự ước tính)*.
- **Giá** ≥2 mức model (USD / 1 triệu token, gói trả phí, Standard): `gemini-3.1-flash-lite` vào 0,25 · ra 1,50 · `gemini-4-hydrogen` vào 1,50 · ra 7,50. Nguồn: [trang giá Gemini API](https://ai.google.dev/gemini-api/docs/pricing) (chuyển tới aistudio.google.com/docs/pricing), xem 27/11/2026; giá ra đã gồm token suy nghĩ. *(Chưa đối chiếu với `further-reading/model-prices.md` của repo đề.)*
- **Tỉ lệ đạt** dùng để tính: 25/25 (100%) — lượt `run-3` (run ID `run-3@20261128-014213`, `gemini-3.1-flash-lite`, chấm bằng `python run.py score eval/run-3.csv`)
- Đo token trên model `gemini-3.1-flash-lite`, tính giá model `gemini-3.1-flash-lite` và `gemini-4-hydrogen`

## 2. Kết quả mô phỏng

Lượt mô phỏng: `cost/simulate-1.csv` · run ID `simulate-1@20261128-064255` · 50 phiên (lỗi 0/50) · seed 42

Lệnh đã chạy:

```powershell
python run.py simulate --wait 5 --rate-from eval/run-3.csv
```

*(bảng chép từ `cost/simulate-1-summary.md`)*

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| dung_it | 21 | 1 | 1646 | 225 | 0.9 | 2.7 |
| dung_vua | 21 | 2 | 3633 | 535 | 2.0 | 5.9 |
| dung_nhieu | 8 | 3 | 4455 | 691 | 2.4 | 7.5 |

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (500 người) | Chi phí / tháng — cơ sở (1.000 người) | Chi phí / tháng — cao (30.000 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gemini-3.1-flash-lite (vào 0.25 · ra 1.5 $/1M) | $0.0014 | $0.0014 | $0.00079 | $2.46 | $4.92 | $147.49 | $0.0049 |
| gemini-4-hydrogen (vào 1.5 · ra 7.5 $/1M) | $0.0076 | $0.0076 | $0.0044 | $13.59 | $27.17 | $815.17 | $0.0272 |

Token đo trên model `gemini-3.1-flash-lite`, tính giá cho cả hai model; model khác bộ tách token thì số token thật có thể lệch.

Chi phí / task thành công = chi phí trung bình mỗi phiên ÷ tỉ lệ đạt — **không coi như đạt 100%**.

## 3. So với impact

- Impact / người / tháng (`spec.md` §2): ~42 phút rà sao kê (1,2 lần × ~35 phút, trung bình P1–P3) và khoảng 280.000–420.000đ giữ lại nếu cắt được 20–30% nhờ cảnh báo sớm (20–30% là *tự ước tính* trong §2).
- Chi phí / người / tháng (cơ sở, model `gemini-3.1-flash-lite`): $0.0049 (chưa tới 1 cent); với `gemini-4-hydrogen`: $0.0272
- **Kết luận một dòng — đáng làm không:** Đáng làm — chi phí model chưa tới 1 cent mỗi người mỗi tháng (kể cả model đắt hơn chỉ ~3 cent), rất nhỏ so với ~42 phút rà sao kê và 280.000–420.000đ giữ lại mỗi người mỗi tháng; ở quy mô cao 30.000 người cũng chỉ ~$147 / tháng.

## 4. *(Muốn sâu hơn, không bắt buộc)*

- **Câu do code xử lý không tốn token:** ở lượt `run-3`, 7/25 câu thử (B04, B05, B08, B09, B10, B24, B25 — thiếu dữ liệu, mơ hồ, bị từ chối) trả lời bằng code, không gọi model. Chặn sớm bằng code vừa an toàn vừa kéo chi phí trung bình xuống.
- **Model rẻ hay mạnh:** đổi `gemini-3.1-flash-lite` → `gemini-4-hydrogen` làm chi phí / phiên tăng khoảng 5,4 lần ($0.0014 → $0.0076, bảng mục 2), trong khi model rẻ đã đạt 25/25 ở `run-3` — chưa có lý do đổi.
- **Chi phí ngoài model:** Web Demo chạy bằng thư viện chuẩn Python, không cần dịch vụ trả phí lúc thử nghiệm; khi dùng thật cần thêm hosting và lưu trữ (chưa ước tính). Không có giờ công người duyệt, vì người dùng tự quyết định trên từng gợi ý.

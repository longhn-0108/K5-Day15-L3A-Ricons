# Data card · Dữ liệu giả lập Ricons

Bản ngày 27/11/2026. Hai bộ dữ liệu `synthetic` được soạn từ các hồ sơ giả định và `expected` trong [benchmark](../eval/benchmark.csv). Các con số bổ sung là giả định *(tự ước tính)*. Phạm vi sử dụng là chạy thử và kiểm thử.

## Ngân sách tháng · `budgets.json`

Ba hồ sơ, mỗi hồ sơ có bảy danh mục. Tệp dùng cấu trúc `user_id → label, categories`, mỗi danh mục có `name`, `limit` (VND) và `essential`. Hạn mức ăn uống của `user_van_phong` là 3.000.000đ. Cả ba hồ sơ đặt `essential: true` cho `tien_nha`, `dien_nuoc` và `thuoc_men`.

## Giao dịch · `transactions.csv`

Soạn tay theo từng hồ sơ và tháng, với ngày và số tiền cố định. Dựng các mốc ăn uống của hồ sơ văn phòng từ `expected`, sau đó thêm các khoản chi theo hồ sơ và dùng tên nhất quán cho Highlands Coffee, Trà sữa TocoToco, GrabFood và ShopeeFood đêm. Mã giao dịch được gán theo tiền tố hồ sơ và số thứ tự. Cách sinh xác định, không dùng seed.

| Hồ sơ | 10/2026 | 11/2026 | Tổng |
|---|---:|---:|---:|
| `user_sinh_vien` | 14 | 14 | 28 |
| `user_van_phong` | 29 | 35 | 64 |
| `user_gia_dinh` | 14 | 14 | 28 |
| **Tổng** | **57** | **63** | **120** |

Codex kiểm bằng Python toàn bộ 120 dòng và đối chiếu tay 7 dòng quanh mốc 19–20/10, 14–15/11 và hai khoản thuốc tháng 11. Có 0 mã trùng và 0 danh mục ngoài ngân sách của hồ sơ tương ứng. Dữ liệu tập trung vào các mốc của hồ sơ văn phòng và chỉ bao phủ hai tháng.

### Kết quả tính từ CSV đến hết ngày của câu thử

| Câu | Kết quả cho `user_van_phong` |
|---|---|
| B01 · 15/11 | 2.550.000đ / 3.000.000đ (85%), cảnh báo vàng. GrabFood 6 × 100.000đ, bớt 2 đơn giữ 200.000đ. ShopeeFood đêm 5 × 80.000đ, bớt 2 đơn giữ 160.000đ. |
| B02 · 14/11 | 2.370.000đ / 3.000.000đ (79%), còn 630.000đ, không cảnh báo sớm. |
| B03 · 20/10 | Lần đầu chạm ngưỡng vào 20/10 với 2.400.000đ / 3.000.000đ (80%). Đến hết 19/10 là 2.240.000đ (74,7%). |
| B04 · 12/2026 | 0 giao dịch ở cả ba hồ sơ. |
| B06 · 28/11 | 2.550.000đ / 3.000.000đ (85%), còn 450.000đ, không cảnh báo sớm. |
| B07 · 11/2026 | Hai khoản thuốc ngày 08/11 và 13/11, tổng 320.000đ, thuộc `thuoc_men` có `essential: true`. Công cụ loại chúng khỏi danh sách gợi ý cắt giảm. |

### Chênh lệch để Long xử lý

`_load_transactions` lọc theo hồ sơ và tháng. `check_alert_rules` dùng `current_day` để chọn ngưỡng cảnh báo, còn dữ liệu của cả ba công cụ vẫn bao gồm giao dịch sau ngày chốt. Các số dưới đây đi theo thứ tự CSV tính đến hết ngày → công cụ hiện tại.

- **B01** giao dịch 32 → 35, chi di chuyển 120.000đ → 520.000đ, chi mua sắm 0đ → 320.000đ.
- **B02** chi ăn uống 2.370.000đ → 2.550.000đ (+180.000đ), còn lại 630.000đ → 450.000đ, tỷ lệ 79% → 85%, từ không cảnh báo sang cảnh báo vàng. Giao dịch 30 → 35, chi di chuyển 120.000đ → 520.000đ, chi mua sắm 0đ → 320.000đ. GrabFood 5 → 6 đơn (+100.000đ), ShopeeFood đêm 4 → 5 đơn (+80.000đ).
- **B03** đến 20/10, giao dịch 26 → 29, chi di chuyển 48.000đ → 188.000đ, chi mua sắm 260.000đ → 450.000đ. Công cụ đưa thêm GrabBike vào gợi ý với 2 giao dịch, tổng 80.000đ. Khi kiểm thêm 19/10, chi ăn uống 2.240.000đ → 2.400.000đ (+160.000đ) và công cụ bật cảnh báo vàng sớm.

Ở lớp đọc đầu vào, `_detect_user_and_month` dùng ngày mặc định 16 cho B01 (15/11), B02 (14/11) và B03 (20/10).

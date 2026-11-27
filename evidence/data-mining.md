# Đào data — cách đếm và kết quả

> Nguồn công khai: bình luận tiếng Việt trên Google Play Store của 2 ứng dụng quản lý chi tiêu cá nhân phổ biến tại Việt Nam (**Money Lover** và **Sổ Thu Chi MISA**).
> File dữ liệu thô đã ẩn danh (không lưu tên tác giả) nằm tại `evidence/raw-reviews.csv` (được `.gitignore` bỏ qua theo quy tắc `evidence/**/raw-*`, không commit nguyên file data). Script đếm chạy lại được: [`evidence/count.py`](count.py).

## 1. Cách đếm — viết TRƯỚC khi chạy

- **Data dùng:** 300 bình luận công khai tiếng Việt (xếp theo tiêu chí *Liên quan nhất* trên Google Play, khoảng thời gian `2025-01-27` đến `2026-11-25`) của 2 app quản lý chi tiêu cá nhân:
  - Money Lover (`com.bookmark.money`): 150 bình luận.
  - Sổ Thu Chi MISA (`vn.com.misa.sothuchi`): 150 bình luận.
  - *(Ghi chú: File thu thập ban đầu có thêm 150 bình luận MoMo `com.mservice.momotransfer`, nhưng đã lọc loại khỏi mẫu số chính vì đa phần bình luận MoMo xoay quanh lỗi thanh toán, Ví Trả Sau và CSKH, không phản ánh nhu cầu quản lý ngân sách.)*
- **Lọc gì:** Giữ các bình luận có nội dung thực chất (`độ dài ≥ 30 ký tự`) để loại bình luận cụt như "OK", "Good" và loại spam quảng cáo vay tiền.
- **Mẫu số là gì:** **`N = 159`** bình luận thực chất không phải spam của 2 app quản lý chi tiêu cá nhân (`Money Lover: 76`, `MISA Sổ Thu Chi: 83`). Trong đó đánh giá 1–3 sao chiếm `74/159 (46,5%)`.
- **Đếm gì:** Tỷ lệ bình luận nêu ít nhất một trong 5 nhóm vấn đề/khoảng trống về theo dõi chi tiêu và ngân sách (một bình luận có thể thuộc nhiều nhóm; dòng tổng hợp có khử trùng theo `review_id`).
- **Script chạy lại được:** `python evidence/count.py` (thêm `--verbose` để in từng mã `RV-xxxx` khớp bộ lọc).

## 2. Đọc trước, đếm sau

Đã đọc trước 30 bình luận đầu tiên của 2 app và từ điển cột (`review_id`, `app`, `app_id`, `date`, `score`, `thumbs_up`, `content`). Các *kiểu* hành vi và phàn nàn nổi bật thấy được trước khi chốt từ khóa đếm:
- Người dùng ghi chép được giao dịch nhưng **vẫn phải tự tính toán hoặc thiếu báo cáo trực quan / dự báo sớm** để biết tiền còn lại có đủ chi tiêu hay không, hoặc bị giới hạn chỉ tạo được 1 ngân sách.
- **Rào cản nhập tay và liên kết ngân hàng/đồng bộ kém:** nhiều người muốn nhập sao kê hoặc liên kết ngân hàng để khỏi ghi tay nhưng tính năng liên kết bị lỗi, thu phí riêng, ít ngân hàng hỗ trợ hoặc đồng bộ chậm giữa các thiết bị.
- **Lỗi sai lệch số liệu / nhân đôi giao dịch:** khi cập nhật hoặc chuyển tiền giữa các ví, app cộng trùng hoặc lệch số dư làm mất niềm tin vào con số báo cáo.
- **Paywall / quảng cáo và AI gây phiền:** khóa tính năng cơ bản sau gói Premium, quảng cáo liên tục, hoặc để trợ lý AI tự hiện đè lên thao tác nhập liệu gây khó chịu.

## 3. Kết quả

Chạy `python evidence/count.py` trên `N = 159` bình luận thực chất:

| Đếm gì | x / N | % | Ghi chú |
|---|---|---|---|
| Rào cản nhập tay, liên kết ngân hàng lỗi/ít bank hoặc đồng bộ kém | 14 / 159 | 8,8% | Phản ánh đúng nguyên nhân người dùng bỏ app quản lý chi tiêu chuyên dụng |
| Bị khóa tính năng / ép mua Premium / quảng cáo gây phiền | 12 / 159 | 7,5% | Đã loại các câu khen "không có quảng cáo" / "ít quảng cáo" |
| Lỗi sai lệch số liệu / nhân đôi giao dịch / mất dữ liệu chi tiêu | 10 / 159 | 6,3% | Đã loại các câu khen "không bị mất dữ liệu" |
| Thiếu phân tích / dự báo / tổng quan dễ hiểu hoặc giới hạn ngân sách | 9 / 159 | 5,7% | Người dùng phải tự tính toán thêm xem tiền còn lại có đủ chi không |
| Phàn nàn trợ lý AI hiện gây phiền / khó thao tác | 1 / 159 | 0,6% | Đòi hỏi AI chỉ xuất hiện khi cần, không cản trở thao tác |
| **Tổng hợp: có ít nhất 1 trong 5 pain trên (khử trùng)** | **41 / 159** | **25,8%** | Hơn 1/4 bình luận thực chất gặp ít nhất một vướng mắc lớn |

## 4. ≥5 ví dụ cụ thể (mã đã ẩn danh, trích nguyên văn)

1. **`RV-0152` (MISA Sổ Thu Chi · 4★ · 2026-11-23):** *"Trải nghiệm khá mượt, cũng ít quảng cáo. Nhưng app sẽ hơi khó dùng nếu không có nhiều kiến thức quản Lý tài chính. Nếu app có thêm chức năng hỗ trợ phân tích/ dự báo tình hình tài chính dựa trên dữ liệu nhập những tháng trước thì sẽ rất rất nên recommend."*
2. **`RV-0153` (MISA Sổ Thu Chi · 4★ · 2026-11-21):** *"Việc ghi chép thu chi khá thuận tiện, tuy nhiên mình vẫn phải tự tính toán thêm nếu muốn biết số tiền còn lại đủ trang trải sinh hoạt trong những tháng tiếp theo hay không"*
3. **`RV-0001` (Money Lover · 2★ · 2026-11-14):** *"App nhiều tính năng hay, trừ một thứ là XEM TỔNG QUAN THEO LỊCH NGÀY TRONG THÁNG. Đó mới là thứ quan trọng nhất, dễ dàng xem hôm qua, hôm kia, tuần trước mình đã tiêu sài thế nào. Khá đáng tiếc, khi nào có thì mình tải lại app."*
4. **`RV-0011` (Money Lover · 3★ · 2026-08-29):** *"1. app không có phần tiết kiệm 2. app chỉ tạo được 1 ngân sách"*
5. **`RV-0178` (MISA Sổ Thu Chi · 1★ · 2026-10-20):** *"xóa sau 5 phút trãi nghiệm. bắt mua gói nhưng mua xong lại có dc mỗi 4 cái ngân hàng liên kết. mà toàn ngân hàng ko có mấy người sử dụng"*
6. **`RV-0148` (Money Lover · 1★ · 2025-02-27):** *"Ứng dụng kém. Các giao dịch chuyển tiền giữa các tài khoản dù đánh dấu là không tính vào báo cáo nhưng vẫn thể hiện trong báo cáo thành 2 khoản thu và chi độc lập và thể hiện vào biểu đồ tổng quát dẫn đến số tiền thu và chi tăng lên gấp 2-3 lần thực tế."*
7. **`RV-0239` (MISA Sổ Thu Chi · 1★ · 2026-08-01):** *"Premium vẫn có quảng cáo là sao???? Hiện trợ lý AI là 1 điểm trừ. Mà giờ 1 sao rồi trừ gì nữa Trợ lý AI khi nào cần thì người ta mở lên. Hiện lên làm gì để khó thao tác nhập"*

## 5. Giới hạn của data

- **Thiếu bối cảnh & lý do sâu:** Bình luận công khai trên Google Play cho biết người dùng *bị vướng gì trên app* nhưng không cho biết *họ tiêu lố bao nhiêu tiền mỗi tháng*, *vào tuần nào*, hay *họ phải rút bao nhiêu từ tiền tiết kiệm*.
- **Lệch mẫu (selection bias):** Người bức xúc về lỗi kỹ thuật, mất dữ liệu hoặc thu phí thường để lại đánh giá 1 sao nhiều hơn nhóm người dùng bình thường âm thầm bỏ app; ngoài ra thuật toán "Liên quan nhất" của Google Play ưu tiên các bình luận dài và có tương tác.
- **Lệch từ khóa:** Đếm theo regex có thể bỏ sót các câu viết tắt/sai chính tả không nằm trong bộ từ khóa (tỷ lệ thực tế có thể cao hơn).
- **→ Kiểm lại bằng phỏng vấn:** Nhóm đã đối chiếu với **3 cuộc phỏng vấn sâu ngoài nhóm (`evidence/interviews/P1.md`, `P2.md`, `P3.md`)** để xác nhận nguyên nhân hành vi (tiêu lố từ tuần 3 do khoản nhỏ lặp lại, bỏ app chuyên dụng vì ngại nhập tay, tắt cảnh báo vì báo muộn/gây phiền).

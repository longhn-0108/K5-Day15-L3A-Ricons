# Tổng hợp bằng chứng pain

> Điền ở guide bước 1.2, xong trước **CP3 10:00 Thứ Bảy 28/11**. Chấm ở rubric R1.
> Ba nguồn ngang nhau — tối thiểu **≥1 nguồn đạt ngưỡng**. Mạnh nhất: đào data ra insight → hỏi người dùng để kiểm lại (hoặc ngược lại).

## 1. Nguồn đã dùng

| Nguồn | Đạt ngưỡng? | File |
|---|---|---|
| Đào data (≥30 review công khai: x/N, %, cách đếm chạy lại được, ≥5 ví dụ) | ☑ *(159 review thực chất / 300 review thô)* | `evidence/data-mining.md`, `evidence/count.py` |
| Phỏng vấn (≥3 người ngoài nhóm, đúng người dùng) | ☑ *(3/3 người)* | `evidence/interviews/P1.md`, `P2.md`, `P3.md` |
| Khảo sát (≥20 người ngoài nhóm, đúng người dùng) | ☐ *(chưa làm — nếu không làm sẽ xóa thư mục trước CP3)* | `evidence/survey/` |

## 2. Số chính

- Đào data (`N = 159` bình luận thực chất từ 300 review Google Play của Money Lover & MISA Sổ Thu Chi, chạy lại bằng `python evidence/count.py`): **41/159 (25,8%)** gặp ít nhất 1 trong 5 pain chính — nổi bật là rào cản nhập tay/liên kết ngân hàng/đồng bộ **14/159 (8,8%)**, khóa tính năng/quảng cáo **12/159 (7,5%)**, sai lệch số liệu **10/159 (6,3%)**, thiếu phân tích/dự báo/tổng quan để tự quyết **9/159 (5,7%)**, và AI hiện gây phiền **1/159 (0,6%)**.
- Phỏng vấn: **3/3 người gặp** *(n nhỏ không ghi %)* · số lần / tháng: P1 ~2 lần/tháng, P2 ~0,67 lần/tháng (2 lần/3 tháng), P3 ~1 lần/tháng (3 lần/3 tháng) · mỗi lần mất **20–60 phút** rà lại giao dịch, tiêu lố **1,2–2,2 triệu/lần** · cả **3/3 người** từng phải rút **500k–1,5 triệu** từ tiền tiết kiệm bù vào.
- Khảo sát: chưa thực hiện.

| | Vai | Gặp pain? | Số lần / 1 tháng qua | Lần gần nhất mất | Đang xoay xở bằng |
|---|---|---|---|---|---|
| P1 | Nhân viên văn phòng, 27 tuổi (app ngân hàng + Excel) | Có | ~2 lần/tháng (đều 3 tháng gần đây) | 30–40 phút rà sao kê · lố ~1,2 triệu (có lần rút ~500k tiết kiệm) | App ngân hàng + Excel; cuối tháng tự nhẩm cắt ăn ngoài/cà phê hoặc rút tiết kiệm |
| P2 | Nhân viên văn phòng, lương ~18tr (2 app ngân hàng + ShopeePay) | Có | ~0,67 lần/tháng (2 lần / 3 tháng) | 50–60 phút rà sao kê · lố ~2,2 triệu (rút 1,5 triệu tiết kiệm) | Xem số dư app ngân hàng + ví; cuối tháng tự nấu cơm, từ chối order nước và rút tiết kiệm bù |
| P3 | Nhân viên văn phòng, lương ~13tr (app ngân hàng + MoMo + tiền mặt) | Có | ~1 lần/tháng (3 lần / 3 tháng) | 20–25 phút rà sao kê · lố ~1,8 triệu (rút 1,5 triệu tiết kiệm) | Vài hôm xem số dư app ngân hàng; cuối tháng ăn cơm gần công ty và rút tiết kiệm bù |

## 3. ≥5 trích dẫn hoặc ví dụ nguyên văn (có nguồn, bỏ tên)

1. "Mình nhớ có tuần đặt đồ ăn 5 bữa liền, cộng thêm 4 ly cà phê là bay gần 500k mà không để ý." — P1
2. "Cảnh báo chỉ báo động khi đã cận kề giới hạn, chứ không giúp mình điều chỉnh sớm. Nhiều lúc mình bỏ qua luôn vì biết có cắt cũng không kịp, thành ra cảm giác cảnh báo chỉ để 'báo tang' chứ không phải để 'phòng bệnh'." — P1
3. "Toàn bị 'rỉ máu' từ mấy khoản nhỏ lẻ không à. Trưa nào lười ra ngoài là lại gọi đồ ăn cỡ 60–90 nghìn một bữa, chiều anh chị trong phòng rủ nhau đặt trà sữa hay cà phê cũng mất thêm 45–60 nghìn nữa." — P2
4. "Cái làm mình thấy ức chế nhất là mấy cái cảnh báo đó nó chỉ báo cho mình biết con số đã tiêu thôi, kiểu như nói cho mình thấy tội lỗi thêm chứ chẳng chỉ ra mình phải làm gì tiếp theo." — P2
5. "Đang đi làm mà điện thoại cứ báo thì mình thường tắt đi luôn. Với cả nó báo mình vượt ngân sách rồi thì cũng đâu làm gì được nữa." — P3
6. "Ngoài ra mình hay đặt trà sữa với đồ ăn vặt ở văn phòng, mỗi lần khoảng 40–60 nghìn. Bình thường thấy số tiền cũng nhỏ nên không để ý." — P3

## 4. Các nguồn có khớp nhau không

- Phỏng vấn 3/3 người đều trùng khớp ở 4 điểm: (1) tiêu lố xảy ra từ **tuần thứ 3 (tầm ngày 20)**; (2) nguyên nhân chính là **khoản nhỏ lặp lại** (đặt đồ ăn trưa, cà phê/trà sữa, mua sắm online) chứ không phải sự cố lớn; (3) hậu quả trực tiếp là **rút tiền tiết kiệm bù vào** và mất **20–60 phút** rà lại giao dịch; (4) cảnh báo hiện tại **báo quá muộn, chung chung, gây cảm giác tội lỗi** nên bị bỏ qua.
- Đối chiếu với nguồn đào review công khai (`evidence/data-mining.md`): **khớp mạnh ở 3 điểm cốt lõi** — (1) người dùng thiếu phân tích/dự báo sớm và phải tự tính xem còn đủ tiền chi không (`9/159`, vd `RV-0152`, `RV-0153`), khớp với việc P1–P3 chỉ nhận cảnh báo quá muộn; (2) rào cản nhập tay và liên kết ngân hàng kém (`14/159`, vd `RV-0154`, `RV-0178`), khớp với việc P2, P3 bỏ app chuyên dụng; (3) yêu cầu số liệu phải chính xác (`10/159` kêu sai/nhân đôi số liệu) và AI không được hiện gây phiền (`RV-0239`), khớp trực tiếp với nguyên tắc dùng quy tắc code tính tiền + cho phép tạm tắt cảnh báo.

## 5. Kết luận

Giả thuyết ở `evidence/hypothesis.md`: **đúng phần cốt lõi (3/3 vượt ngưỡng ≥2/3)** — cả 3 người đều tiêu lố từ tuần 3 do khoản nhỏ lặp lại và bỏ qua cảnh báo trễ/chung chung.
**Điểm mới phát hiện thêm:** 2/3 người (P2, P3) đã bỏ app quản lý chi tiêu chuyên dụng sau 1–3 tuần vì **ngại nhập tay** và giao dịch phân mảnh nhiều ví/ngân hàng; cảnh báo mang giọng điệu gây "tội lỗi" hoặc bắn thông báo giờ làm việc rất dễ bị tắt.
**Điều vẫn chưa biết:** Tỷ lệ người dùng thực sự bấm làm theo gợi ý cắt giảm (so với bỏ qua/tạm tắt) khi nhận cảnh báo sớm giữa tháng — sẽ kiểm chứng qua bước dùng thử 10 phút với 2–3 người ngoài nhóm ở `validation/log.md`.

## Lịch hẹn (dùng cho CP2 — chỉ ghi vai và giờ, không tên)

| Vai | Giờ hẹn | Đã xong? |
|---|---|---|
| Nhân viên văn phòng, 27 tuổi (P1) | 27/11 12:17 | ☑ |
| Nhân viên văn phòng, lương ~18tr (P2) | 27/11 13:02 | ☑ |
| Nhân viên văn phòng, lương ~13tr (P3) | 27/11 13:01 | ☑ |

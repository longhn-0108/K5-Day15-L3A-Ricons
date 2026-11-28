# Người dùng thử *(bonus)*

> Điền ở guide bước 4.3 — 2–3 người ngoài nhóm, ~10 phút / người, theo 5 nhịp: làm quen · bối cảnh · giao việc · quan sát · hỏi sau. Ôn lại: ngày 5, ngày 13. Chấm ở rubric Bonus.
> Không ghi tên: ghi vai. Hành vi quan sát được nặng hơn lời nói; toàn lời khen = phiên chưa đạt, giao việc khó hơn.
> Người dùng thử **không thay được** bằng chứng pain ở `evidence/`.

## Kế hoạch buổi thử *(chuẩn bị trước — Nguyễn Quang Hiệp)*

- **Người thử:** 2–3 người ngoài nhóm, đúng người dùng chính: nhân viên văn phòng trẻ, có trả tiền hằng ngày qua ví hoặc app ngân hàng. Chỉ ghi vai (vd "nhân viên văn phòng, 25 tuổi, dùng MoMo").
- **Chuẩn bị máy:** `.env` có key; chạy `python run.py web`; để mặc định hồ sơ Nhân viên văn phòng, tháng 2026-11, ngày 15. Không cho người thử bấm các nút câu thử có sẵn (B01, B07…): để họ tự gõ câu hỏi. Các nút Áp dụng / Bỏ qua / Tạm tắt ghi vào `data/user_actions.jsonl` — không commit file đó.
- **Ghi chép:** một người dẫn, một người ghi (nếu được). Ghi hành vi trước, lời nói sau. Đếm số câu mỗi người gõ trong một lần dùng để kiểm lại `turns_per_session` ở `cost/personas.yaml`.

| Nhịp | Thời gian | Làm gì |
|---|---|---|
| 1. Làm quen | 1 phút | Nói rõ đang thử sản phẩm, không thử người; không có câu trả lời sai; xin phép ghi chép, không ghi tên. |
| 2. Bối cảnh | 2 phút | "Bạn đang theo dõi chi tiêu tháng bằng cách nào?" · "Lần gần nhất bạn thấy mình tiêu quá tay là khi nào, lúc đó bạn làm gì?" (hỏi chuyện đã xảy ra, không hỏi "bạn có muốn…") |
| 3. Giao việc | 4–5 phút | Giao theo kết quả, không chỉ nút (xem 3 việc dưới). Không giải thích giao diện trước. |
| 4. Quan sát | trong lúc làm | Họ nhìn chỗ nào đầu tiên? Gõ câu gì? Chỗ nào dừng lại lâu? Có tin con số không? Có hiểu 3 lựa chọn Áp dụng / Bỏ qua / Tạm tắt không? |
| 5. Hỏi sau | 2 phút | Câu "Nếu mai không được dùng nữa…" (dưới bảng) · "Chỗ nào khó hiểu nhất?" · "Có gợi ý nào bạn thấy không hợp với mình không, vì sao?" |

**Việc giao (theo kết quả):**
1. "Giả sử hôm nay là 15/11 và bạn là nhân viên văn phòng này. Hãy tìm xem tháng này bạn còn tiêu ăn uống được bao nhiêu, và nếu cần bớt thì bớt khoản nào."
2. "Tháng này bạn có khoản tiền thuốc phát sinh. Hãy hỏi xem có nên cắt bớt không."
3. *(Nếu người thử toàn khen — giao khó hơn)* "Hãy xem tình hình tháng 12" (chưa có dữ liệu) hoặc "Bạn thấy cảnh báo phiền, hãy tắt nó trong tháng này."

## Kết quả

| Người thử (vai) | Việc giao (theo kết quả, không theo nút) | Quan sát (làm gì đầu tiên, chỗ do dự, chỗ hiểu sai) | Trích nguyên văn | Mức nghiêm trọng (cao / vừa / thấp) |
|---|---|---|---|---|
| | | | | |
| | | | | |
| | | | | |

Câu hỏi sau: *"Nếu mai không được dùng nữa, bạn thấy: rất tiếc / hơi tiếc / không sao?"* → __ / __ / __

## Tổng hợp

- Chủ đề lặp nhiều nhất: __
- Sửa gì trước demo (ghi `spec.md` §10): __
- Giữ gì và vì sao: __
- Để dành sau: __

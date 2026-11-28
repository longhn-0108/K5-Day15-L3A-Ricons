# Kịch bản quay video demo dự phòng (bản nháp)

> Dùng cho slide 4 "Demo live" khi mạng hoặc model lỗi. Mục tiêu: 60–90 giây, 1 ca thường (B01) + 1 ca khó (B07).
> Đã chạy thử 27/11 trên Web Demo với `gemini-3.1-flash-lite`: B01 trả lời trong 2,48 giây, B07 trong 2,21 giây, mỗi câu 1 lượt gọi model.

## Chuẩn bị (2 phút)

1. `.env` có key thật (`MODEL_PROVIDER=gemini`, `MODEL_NAME=gemini-3.1-flash-lite`).
2. Mở Web Demo:

   ```powershell
   python run.py web
   ```

   Trình duyệt tự mở `http://127.0.0.1:8000`. Để mặc định: hồ sơ **Nhân viên văn phòng**, tháng **2026-11**, ngày **15 (85% · Cảnh báo vàng)**.
3. Trình duyệt toàn màn hình (F11), zoom 100%. Tắt thông báo Windows / Zalo / Messenger.
4. **Không để terminal hay file `.env` lọt vào khung hình** (có API key).
5. Công cụ quay trên Windows 10: **Xbox Game Bar** — bấm `Win + Alt + R` để bắt đầu / dừng quay cửa sổ trình duyệt. File MP4 lưu ở `Videos\Captures`. (Hoặc dùng OBS nếu đã cài.)

## Kịch bản

| Thời điểm | Thao tác trên màn hình | Lời thoại gợi ý |
|---|---|---|
| 0:00–0:12 | Để yên trang đầu, rê chuột qua bảng **Tiến độ hạn mức** và dòng **Ăn uống 85,0% · Sắp vượt** | “Ngày 15/11, nhóm ăn uống đã dùng 85% hạn mức, qua ngưỡng cảnh báo sớm 80%. Con số này do code Python tính, không phải AI.” |
| 0:12–0:20 | Rê qua 3 dòng **Thiết yếu · Không cắt** và danh sách **Khoản lặp lại không thiết yếu** | “Tiền nhà, điện nước, thuốc được đánh dấu thiết yếu và bị loại trước khi gửi cho AI. AI chỉ được chọn trong các khoản lặp lại như GrabFood, ShopeeFood.” |
| 0:20–0:45 | Bấm nút **B01 · Cảnh báo 15/11 (85%)** → bấm **Phân Tích Ngân Sách** → chờ kết quả, cuộn chậm | “Người dùng hỏi nếu bớt hai đơn ở mỗi chỗ hay đặt thì giữ lại được bao nhiêu. Hệ thống báo đã dùng 85%, bớt 2 đơn GrabFood giữ 200 nghìn, bớt 2 đơn ShopeeFood đêm giữ 160 nghìn, và để người dùng chọn: áp dụng, bỏ qua hoặc tạm tắt.” |
| 0:45–0:50 | Chỉ vào dòng **Trace & Token** ở cuối | “Mỗi câu chỉ gọi model một lần, khoảng 2–3 giây.” |
| 0:50–1:15 | Bấm **B07 · Bảo vệ khoản thuốc** → **Phân Tích Ngân Sách** → cuộn chậm | “Ca khó: người dùng hỏi có nên bớt mua thuốc để giữ ngân sách không. Hệ thống khẳng định không nên bớt thuốc, rồi chỉ gợi ý điều chỉnh các khoản không thiết yếu có trong dữ liệu.” |
| 1:15–1:25 *(tuỳ chọn)* | Bấm **B05 · Mơ hồ “Lố rồi”** → **Phân Tích Ngân Sách** | “Câu quá ngắn thì hệ thống không đoán, mà hỏi lại tháng và nhóm chi tiêu.” |

## Lưu ý khi quay

- Gemini đôi lúc báo **HTTP 503 (quá tải)**. Nếu câu trả lời báo lỗi, đợi vài giây rồi bấm lại; khi dựng thì cắt đoạn lỗi.
- **Không bấm** các nút *Áp Dụng Gợi Ý / Bỏ Qua Lần Này / Tạm Tắt Cảnh Báo* khi quay: chúng ghi vào `data/user_actions.jsonl`. Nếu lỡ bấm, đừng commit file đó.
- Câu trả lời của model có thể khác nhau đôi chút giữa các lần chạy (ví dụ B07 có lúc gợi ý bớt 1 đơn thay vì 2). Kiểm lại số trong video khớp bảng bên trái trước khi dùng.
- Mỗi lần quay thử tốn 2–3 lượt gọi model; key miễn phí đã từng chạm hạn mức (lỗi 429), nên đừng quay đi quay lại quá nhiều trước lượt `simulate` chính thức.

## Sau khi quay

1. Đặt tên `demo-video.mp4`, tải lên Google Drive (chế độ: ai có link cũng xem được).
2. Mở link bằng **cửa sổ ẩn danh** để chắc chắn xem được.
3. Dán link vào slide 4 (chỗ `[link video]`) và form nộp CP4.
4. Nếu Long sửa agent trước CP4, quay lại bản cuối.

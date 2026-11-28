# Video demo tự động (có giọng đọc)

Sinh `demo/out/demo.mp4` (~75 giây, 1920×1080, giọng tiếng Việt, phụ đề burn-in) + `demo/out/demo.srt`
từ Web Demo thật: B01 (ca thường) · B07 (ca khó, bảo vệ khoản thuốc) · B05 (câu mơ hồ).

```powershell
python -m pip install --user edge-tts playwright imageio-ffmpeg
python -m playwright install chromium
python demo/make_demo.py                      # cả video: tốn 3 lượt gọi model (cần .env có key)
python demo/make_demo.py --scenes s0,s1,s2    # xem thử phần đầu, không gọi model
python demo/make_demo.py --voice vi-VN-NamMinhNeural   # giọng nam
```

- Lời thoại và thao tác nằm trong `SCENES` ở đầu `make_demo.py`. Sửa câu nào thì chỉ câu đó được sinh lại giọng (cache ở `demo/build/audio/`).
- Đoạn chờ model và lỗi 503/429 (tự bấm lại) được cắt khỏi video; câu trả lời thật của model lưu ở `demo/build/answers.json` để đối chiếu với lời thoại.
- Không bấm Áp dụng / Bỏ qua / Tạm tắt, nên không ghi vào `data/user_actions.jsonl`. Chỉ quay cửa sổ trình duyệt, không lộ `.env`.
- Giọng đọc dùng dịch vụ TTS online của Microsoft (edge-tts); dịch vụ hay chập chờn nên script tự thử lại.

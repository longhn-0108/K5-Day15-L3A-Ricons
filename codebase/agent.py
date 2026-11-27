"""Luồng chính của bản chạy thử — Workflow cố định (Track E: Cảnh báo ngân sách & Gợi ý cắt giảm).

Luồng:
1. Kiểm tra đầu vào (chặn yêu cầu ngoài phạm vi: tư vấn đầu tư, tự chuyển tiền, xem dữ liệu người khác, bịa số, prompt injection; hỏi lại nếu mơ hồ).
2. Xác định ngữ cảnh (user_id, tháng, ngày).
3. Gọi công cụ Python kiểm tra quy tắc cảnh báo (`check_alert_rules`), lấy trạng thái ngân sách (`get_budget_status`)
   và tìm khoản chi lặp lại không thiết yếu (`find_cut_candidates`).
4. Gọi model AI (`call_model`) để diễn đạt cảnh báo không phán xét (hoặc báo an toàn không báo thừa nếu `has_alert=false`), trích đúng số liệu từ công cụ và gợi ý 2-3 khoản cắt giảm.
"""
import json
import re
from ai import call_model
from tools import check_alert_rules, find_cut_candidates, get_budget_status, log_user_action
from tracing import note  # noqa: F401

SYSTEM = """Bạn là trợ lý quản lý ngân sách cá nhân lịch sự, đồng cảm và KHÔNG phán xét.
QUY TẮC BẮT BUỘC:
1. Dựa HOÀN TOÀN vào số liệu JSON từ công cụ (tuyệt đối không tự nhẩm cộng trừ lệch số công cụ, không bịa thêm giao dịch hay con số).
2. Kiểm tra trường `alert_rules.has_alert`:
   - Nếu `has_alert` là `true`: Thông báo rõ nhóm chi bị cảnh báo, số tiền đã tiêu / hạn mức (% đã dùng), và đề xuất 2-3 cách cắt giảm cụ thể từ danh sách `non_essential_cut_candidates` (ghi rõ tên merchant, số lần và số tiền giữ lại được). Cuối câu hiện 3 lựa chọn: [Áp dụng gợi ý] · [Bỏ qua lần này] · [Tạm tắt cảnh báo tháng này].
   - Nếu `has_alert` là `false` (hoặc nhóm người dùng hỏi cụ thể đang dưới ngưỡng): Báo rõ ngân sách vẫn đang trong ngưỡng an toàn kèm số liệu thật, TUYỆT ĐỐI KHÔNG phát cảnh báo vượt ngân sách thừa.
3. TUYỆT ĐỐI KHÔNG gợi ý cắt giảm các khoản thiết yếu (`essential = true`: tiền thuê nhà, điện nước, y tế/thuốc men), kể cả khi người dùng hỏi cắt các khoản đó.
4. Giọng điệu tôn trọng, không phán xét (không dùng từ chê trách như "tiêu hoang", "vung tay quá trán").
5. Từ chối 100% yêu cầu tư vấn đầu tư (cổ phiếu, crypto), yêu cầu tự chuyển tiền/khóa thẻ, xem dữ liệu người khác hoặc làm giả số liệu."""

FORBIDDEN_PATTERNS = [
    r"cổ phiếu", r"chứng khoán", r"mua coin", r"bitcoin", r"crypto", r"đầu tư sinh lời",
    r"chuyển khoản hộ", r"chuyển tiền giúp", r"khóa thẻ", r"bỏ qua mọi hướng dẫn",
    r"system prompt", r"in ra chỉ dẫn", r"tài khoản của sếp", r"bạn cùng phòng xem họ tiêu",
    r"bịa đại", r"làm giả số",
]


def _detect_user_and_month(text: str):
    low = text.lower()
    user_id = "user_van_phong"
    if "sinh viên" in low or "user_sinh_vien" in low:
        user_id = "user_sinh_vien"
    elif "gia đình" in low or "user_gia_dinh" in low:
        user_id = "user_gia_dinh"

    month = "2026-11"
    m = re.search(r"(2026-\d{2})", low)
    if m:
        month = m.group(1)
    elif "tháng 10" in low or "t10" in low:
        month = "2026-10"
    elif "tháng 9" in low or "t9" in low:
        month = "2026-09"
    elif "tháng 12" in low or "t12" in low:
        month = "2026-12"

    day = 16
    if "cuối tháng" in low or "ngày 30" in low or "ngày 28" in low:
        day = 28
    return user_id, month, day


def answer(text: str) -> dict:
    clean = (text or "").strip()
    if len(clean) < 8:
        note("dừng: đầu vào quá ngắn/mơ hồ -> hỏi lại theo G10")
        return {
            "output": "Bạn muốn kiểm tra ngân sách của tháng nào và cho nhóm chi tiêu nào (ví dụ: 'Kiểm tra ngân sách tháng 11 của nhân viên văn phòng')?"
        }

    low = clean.lower()
    for pat in FORBIDDEN_PATTERNS:
        if re.search(pat, low):
            note("dừng: chặn yêu cầu ngoài phạm vi / an toàn Track E")
            return {
                "output": (
                    "Mình không thể thực hiện yêu cầu này. Trợ lý chỉ hỗ trợ theo dõi hạn mức ngân sách cá nhân "
                    "của chính bạn dựa trên số liệu thật và gợi ý cắt giảm khoản chi không thiết yếu — "
                    "không tư vấn đầu tư tài chính, không tự thực hiện giao dịch, không truy cập tài khoản người khác "
                    "và không làm giả số liệu."
                )
            }

    user_id, month, day = _detect_user_and_month(clean)
    if "tạm tắt" in low:
        res = log_user_action(user_id=user_id, category="an_uong", action="tam_tat")
        note("dừng: đã ghi nhận thao tác tạm tắt cảnh báo")
        return {"output": f"Đã ghi nhận tạm tắt cảnh báo cho nhóm chi tiêu trong tháng {month} ({res.get('logged', {}).get('ts', '')})."}

    alert_info = check_alert_rules(user_id=user_id, month=month, current_day=day)
    if "error" in alert_info:
        note("dừng: tháng/hồ sơ chưa có dữ liệu")
        return {"output": f"Hiện chưa có dữ liệu chi tiêu cho yêu cầu này ({alert_info['error']}). Mình không tự ước tính khi thiếu dữ liệu."}

    budget_status = get_budget_status(user_id=user_id, month=month)
    candidates = find_cut_candidates(user_id=user_id, month=month)

    payload = {
        "user_query": clean,
        "alert_rules": alert_info,
        "budget_status": budget_status,
        "non_essential_cut_candidates": candidates.get("candidates", []),
    }
    prompt = "Dữ liệu chính xác từ công cụ (JSON):\n" + json.dumps(payload, ensure_ascii=False, indent=2)
    reply = call_model(SYSTEM, prompt)
    return {"output": reply["text"]}

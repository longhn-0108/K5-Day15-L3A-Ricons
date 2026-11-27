"""Công cụ của bài toán cảnh báo vượt ngân sách & gợi ý cắt giảm (Track E).

Mỗi công cụ có @tool và docstring ghi đủ 4 ý: tên · input · output · có tác động ra ngoài không.
Đọc trực tiếp từ `data/budgets.json` và `data/transactions.csv` (lọc giao dịch tính đến hết ngày `current_day`).
"""
import csv
import datetime
import json
import os
from collections import defaultdict
from tracing import tool, TOOLS  # noqa: F401

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
ACTION_LOG = os.path.join(DATA_DIR, "user_actions.jsonl")


def _load_budgets():
    path = os.path.join(DATA_DIR, "budgets.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _load_transactions(user_id: str, month: str, current_day: int = 31):
    """Đọc các giao dịch của `user_id` trong `month` tính đến hết ngày `current_day` (inclusive)."""
    path = os.path.join(DATA_DIR, "transactions.csv")
    if not os.path.exists(path):
        return [], False
    month_has_any = False
    rows = []
    with open(path, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if r["user_id"] == user_id and r["date"].startswith(month):
                month_has_any = True
                try:
                    tx_day = int(r["date"].split("-")[2])
                except (IndexError, ValueError):
                    tx_day = 1
                if tx_day <= current_day:
                    rows.append({
                        "tx_id": r["tx_id"],
                        "date": r["date"],
                        "description": r["description"],
                        "amount": int(r["amount"]),
                        "category": r["category"],
                    })
    return rows, month_has_any


def _compute_budget_status(user_id: str, month: str, current_day: int = 31) -> dict:
    """Hàm nội bộ tính tổng chi, số còn lại và tỷ lệ % hạn mức đến hết ngày `current_day`."""
    budgets = _load_budgets()
    if user_id not in budgets:
        return {"error": f"Không tìm thấy dữ liệu hồ sơ '{user_id}'."}
    txs, month_has_any = _load_transactions(user_id, month, current_day=current_day)
    if not month_has_any:
        return {"error": f"Chưa có lịch sử giao dịch nào cho tháng {month}."}

    spent_by_cat = defaultdict(int)
    for t in txs:
        spent_by_cat[t["category"]] += t["amount"]

    cats = budgets[user_id]["categories"]
    summary = {}
    for cat_key, meta in cats.items():
        spent = spent_by_cat.get(cat_key, 0)
        limit = meta["limit"]
        pct = round(spent / limit * 100, 1) if limit > 0 else 0.0
        summary[cat_key] = {
            "name": meta["name"],
            "limit": limit,
            "spent": spent,
            "remaining": limit - spent,
            "percent": pct,
            "essential": meta["essential"],
        }
    return {
        "user_id": user_id,
        "label": budgets[user_id]["label"],
        "month": month,
        "as_of_day": current_day,
        "tx_count": len(txs),
        "categories": summary,
    }


@tool
def get_budget_status(user_id: str = "user_van_phong", month: str = "2026-11", current_day: int = 15) -> dict:
    """Tra trạng thái ngân sách, số đã chi, số còn lại và phần trăm từng nhóm tính đến hết ngày `current_day`.
    Input: user_id (str), month dạng YYYY-MM (str), current_day (int).
    Output: dict gồm thông tin hồ sơ và chi tiết từng nhóm (limit, spent, remaining, percent, essential).
    Không tác động ra ngoài (chỉ đọc data/)."""
    return _compute_budget_status(user_id=user_id, month=month, current_day=current_day)


@tool
def check_alert_rules(user_id: str = "user_van_phong", month: str = "2026-11", current_day: int = 15) -> dict:
    """Kiểm tra quy tắc kích hoạt cảnh báo sớm ngân sách bằng code (không dùng AI phán đoán).
    Quy tắc: Nếu ngày <= 20 (giữa tháng) mà nhóm không thiết yếu đã dùng >= 80% hạn mức,
    hoặc bất kỳ ngày nào dùng >= 90% hạn mức -> bật cảnh báo.
    Input: user_id (str), month (str), current_day (int).
    Output: dict danh sách các nhóm bị bật cảnh báo kèm mức độ. Không tác động ra ngoài."""
    status = _compute_budget_status(user_id=user_id, month=month, current_day=current_day)
    if "error" in status:
        return status

    alerts = []
    for cat_key, info in status["categories"].items():
        if info["essential"]:
            continue
        pct = info["percent"]
        if (current_day <= 20 and pct >= 80.0) or pct >= 90.0:
            severity = "DO" if pct >= 90.0 else "VANG"
            alerts.append({
                "category": cat_key,
                "name": info["name"],
                "spent": info["spent"],
                "limit": info["limit"],
                "remaining": info["remaining"],
                "percent": pct,
                "severity": severity,
            })
    return {
        "user_id": user_id,
        "month": month,
        "current_day": current_day,
        "has_alert": len(alerts) > 0,
        "alerts": alerts,
    }


@tool
def find_cut_candidates(user_id: str = "user_van_phong", month: str = "2026-11", current_day: int = 15) -> dict:
    """Tìm các khoản chi lặp lại nhiều lần thuộc nhóm KHÔNG thiết yếu tính đến hết ngày `current_day`.
    Tuyệt đối loại trừ mọi nhóm có essential=True (tiền nhà, điện nước, thuốc men).
    Input: user_id (str), month (str), current_day (int).
    Output: dict danh sách các khoản lặp lại kèm số đơn, đơn giá TB và mức tiết kiệm nếu bớt 1 hoặc 2 đơn.
    Không tác động ra ngoài."""
    budgets = _load_budgets()
    if user_id not in budgets:
        return {"error": f"Không tìm thấy hồ sơ '{user_id}'."}
    cats = budgets[user_id]["categories"]
    txs, month_has_any = _load_transactions(user_id, month, current_day=current_day)
    if not month_has_any:
        return {"error": f"Chưa có giao dịch trong tháng {month}."}

    grouped = defaultdict(lambda: {"count": 0, "total": 0, "category": "", "category_name": ""})
    for t in txs:
        cat_key = t["category"]
        if cat_key not in cats or cats[cat_key]["essential"]:
            continue
        desc = t["description"]
        grouped[desc]["count"] += 1
        grouped[desc]["total"] += t["amount"]
        grouped[desc]["category"] = cat_key
        grouped[desc]["category_name"] = cats[cat_key]["name"]

    candidates = []
    for desc, stats in grouped.items():
        if stats["count"] >= 2:
            avg_amt = round(stats["total"] / stats["count"])
            candidates.append({
                "merchant": desc,
                "category": stats["category"],
                "category_name": stats["category_name"],
                "count": stats["count"],
                "total_spent": stats["total"],
                "avg_amount": avg_amt,
                "save_if_cut_1": avg_amt,
                "save_if_cut_2": avg_amt * 2,
            })
    candidates.sort(key=lambda x: (x["count"], x["total_spent"]), reverse=True)
    return {"user_id": user_id, "month": month, "as_of_day": current_day, "candidates": candidates[:5]}


@tool
def log_user_action(user_id: str, category: str, action: str) -> dict:
    """Ghi nhận lựa chọn của người dùng với cảnh báo (ap_dung / bo_qua / tam_tat).
    Input: user_id (str), category (str), action (str).
    Output: dict xác nhận đã ghi. Có ghi log cục bộ (đảo lại được)."""
    valid = {"ap_dung", "bo_qua", "tam_tat"}
    if action not in valid:
        return {"ok": False, "error": f"Hành động phải thuộc {sorted(valid)}"}
    entry = {
        "ts": datetime.datetime.now().isoformat(timespec="seconds"),
        "user_id": user_id,
        "category": category,
        "action": action,
    }
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(ACTION_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return {"ok": True, "logged": entry}

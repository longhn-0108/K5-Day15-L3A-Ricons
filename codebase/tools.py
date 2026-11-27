"""Công cụ của bài toán cảnh báo vượt ngân sách & gợi ý cắt giảm (Track E).

Mỗi công cụ có @tool và docstring ghi đủ 4 ý: tên · input · output · có tác động ra ngoài không.
Khi chưa có file dữ liệu trong `data/` (trước khi thành viên phụ trách dữ liệu đẩy lên), công cụ dùng
bộ dữ liệu mẫu dự phòng (mock) để khung `python run.py` vẫn đi hết luồng trước CP2 đúng yêu cầu BTC.
Khi đã có `data/budgets.json` và `data/transactions.csv`, công cụ tự động đọc từ `data/`.
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

MOCK_BUDGETS = {
    "user_van_phong": {
        "label": "Nhân viên văn phòng trẻ (mock khung CP2)",
        "categories": {
            "an_uong": {"name": "Ăn uống", "limit": 3000000, "essential": False},
            "ca_phe_tra_sua": {"name": "Cà phê & Trà sữa", "limit": 800000, "essential": False},
            "di_chuyen": {"name": "Di chuyển", "limit": 1000000, "essential": False},
            "mua_sam": {"name": "Mua sắm online", "limit": 1500000, "essential": False},
            "tien_nha": {"name": "Tiền thuê nhà", "limit": 4500000, "essential": True},
            "dien_nuoc": {"name": "Điện nước & Internet", "limit": 600000, "essential": True},
            "thuoc_men": {"name": "Y tế & Thuốc men", "limit": 500000, "essential": True},
        },
    }
}

MOCK_TRANSACTIONS = [
    {"tx_id": "M01", "user_id": "user_van_phong", "date": "2026-11-05", "description": "CK TIEN PHONG TRO T11", "amount": 4500000, "category": "tien_nha"},
    {"tx_id": "M02", "user_id": "user_van_phong", "date": "2026-11-06", "description": "VNPT EPAY*EVN DIEN NUOC", "amount": 580000, "category": "dien_nuoc"},
    {"tx_id": "M03", "user_id": "user_van_phong", "date": "2026-11-08", "description": "NHA THUOC LONG CHAU", "amount": 320000, "category": "thuoc_men"},
    {"tx_id": "M04", "user_id": "user_van_phong", "date": "2026-11-10", "description": "GRAB*FOOD HN", "amount": 1300000, "category": "an_uong"},
    {"tx_id": "M05", "user_id": "user_van_phong", "date": "2026-11-12", "description": "GRAB*FOOD HN", "amount": 650000, "category": "an_uong"},
    {"tx_id": "M06", "user_id": "user_van_phong", "date": "2026-11-14", "description": "SHOPEEFOOD*DEM", "amount": 360000, "category": "an_uong"},
    {"tx_id": "M07", "user_id": "user_van_phong", "date": "2026-11-15", "description": "SHOPEEFOOD*DEM", "amount": 180000, "category": "an_uong"},
    {"tx_id": "M08", "user_id": "user_van_phong", "date": "2026-11-15", "description": "PHUC LONG COFFEE", "amount": 350000, "category": "ca_phe_tra_sua"},
    {"tx_id": "M09", "user_id": "user_van_phong", "date": "2026-11-16", "description": "PHUC LONG COFFEE", "amount": 330000, "category": "ca_phe_tra_sua"},
]


def _load_budgets():
    path = os.path.join(DATA_DIR, "budgets.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f), False
    return MOCK_BUDGETS, True


def _load_transactions(user_id: str, month: str):
    path = os.path.join(DATA_DIR, "transactions.csv")
    if os.path.exists(path):
        rows = []
        with open(path, encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                if r["user_id"] == user_id and r["date"].startswith(month):
                    rows.append({
                        "tx_id": r["tx_id"],
                        "date": r["date"],
                        "description": r["description"],
                        "amount": int(r["amount"]),
                        "category": r["category"],
                    })
        return rows
    return [dict(r) for r in MOCK_TRANSACTIONS if r["user_id"] == user_id and r["date"].startswith(month)]


def _compute_budget_status(user_id: str, month: str) -> dict:
    """Hàm nội bộ tính tổng chi và phần trăm hạn mức bằng code Python (tránh nhân đôi sự kiện @tool trong trace)."""
    budgets, is_mock = _load_budgets()
    if user_id not in budgets:
        return {"error": f"Không tìm thấy dữ liệu người dùng '{user_id}'."}
    txs = _load_transactions(user_id, month)
    if not txs:
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
        "is_mock_data": is_mock,
        "tx_count": len(txs),
        "categories": summary,
    }


@tool
def get_budget_status(user_id: str = "user_van_phong", month: str = "2026-11") -> dict:
    """Tra trạng thái ngân sách và tổng chi từng nhóm của người dùng trong tháng.
    Input: user_id (str), month dạng YYYY-MM (str).
    Output: dict gồm thông tin persona và chi tiết từng nhóm (limit, spent, percent, remaining, essential).
    Không tác động ra ngoài (chỉ đọc data/)."""
    return _compute_budget_status(user_id=user_id, month=month)


@tool
def check_alert_rules(user_id: str = "user_van_phong", month: str = "2026-11", current_day: int = 16) -> dict:
    """Kiểm tra quy tắc kích hoạt cảnh báo sớm ngân sách bằng code (không dùng AI phán đoán).
    Quy tắc: Nếu ngày <= 20 (chưa hết 2/3 tháng) mà nhóm không thiết yếu đã dùng >= 80% hạn mức,
    hoặc bất kỳ ngày nào dùng >= 90% hạn mức -> bật cảnh báo.
    Input: user_id (str), month (str), current_day (int).
    Output: dict danh sách các nhóm bị bật cảnh báo kèm mức độ. Không tác động ra ngoài."""
    status = _compute_budget_status(user_id=user_id, month=month)
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
                "percent": pct,
                "remaining": info["remaining"],
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
def find_cut_candidates(user_id: str = "user_van_phong", month: str = "2026-11") -> dict:
    """Tìm các khoản chi lặp lại nhiều lần thuộc nhóm KHÔNG thiết yếu để gợi ý cắt giảm.
    Tuyệt đối loại trừ mọi nhóm có essential=True (tiền nhà, điện nước, thuốc men).
    Input: user_id (str), month (str).
    Output: dict danh sách các khoản lặp lại xếp theo tổng tiền giảm dần. Không tác động ra ngoài."""
    budgets, _ = _load_budgets()
    if user_id not in budgets:
        return {"error": f"Không tìm thấy người dùng '{user_id}'."}
    cats = budgets[user_id]["categories"]
    txs = _load_transactions(user_id, month)
    if not txs:
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
            })
    candidates.sort(key=lambda x: x["total_spent"], reverse=True)
    return {"user_id": user_id, "month": month, "candidates": candidates[:5]}


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

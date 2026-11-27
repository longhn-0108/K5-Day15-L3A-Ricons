"""Reproducible review-mining counter for Ricons (Track E).

Reads anonymized public Google Play reviews (no author names) from
`evidence/reviews-anonymized.csv` and counts
recurring user pain themes among personal-finance apps (Money Lover & MISA So Thu Chi).

Usage:
    python evidence/count.py
    python evidence/count.py --verbose
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import Counter
from pathlib import Path

DEFAULT_CSV = Path(__file__).parent / "reviews-anonymized.csv"
TARGET_APPS = {"Money Lover", "MISA So Thu Chi"}
MIN_CONTENT_LEN = 30

# Exclude obvious spam (e.g., loan ads posted in reviews)
SPAM_RX = re.compile(r"vay\s*onl|vaytotnhat|thiếu số|cho vay", re.IGNORECASE)

# Each category: (label, include_regex, optional_exclude_regex)
CATEGORIES: dict[str, tuple[str, re.Pattern[str], re.Pattern[str] | None]] = {
    "missing_insight_forecast": (
        "Thiếu phân tích/dự báo/tổng quan dễ hiểu hoặc giới hạn ngân sách",
        re.compile(
            r"tổng quan|chỉ số|phân tích|dự báo|phải tự tính toán|trực quan|khó hiểu|chỉ tạo được 1 ngân sách|không có phần tiết kiệm|ít báo cáo",
            re.IGNORECASE,
        ),
        None,
    ),
    "bank_sync_manual_friction": (
        "Rào cản nhập tay, liên kết ngân hàng lỗi/ít bank hoặc đồng bộ kém",
        re.compile(
            r"liên kết.*ngân hàng|liên kết ví|liên kết.*lỗi|phí liên kết|ngân hàng liên kết|nhập khẩu.*sao kê|chăm ghi|không đồng bộ|đồng bộ kém|khó đồng bộ|đợi đồng bộ|đồng bộ.*wifi",
            re.IGNORECASE,
        ),
        None,
    ),
    "data_accuracy_bug": (
        "Lỗi sai lệch số liệu / nhân đôi giao dịch / mất dữ liệu chi tiêu",
        re.compile(
            r"sai s[ôố] tiền|sai.*số liệu|số liệu sai|gấp đôi|gấp 2|nhân đôi|thành 2 lần|lệch số liệu|bị lệch|mất hết dữ liệu|mất dữ liệu cũ|mất luôn dữ liệu|xáo trộn|tự copy giao dịch|nhảy sai|lẫn lộn|mất.*lịch sử",
            re.IGNORECASE,
        ),
        re.compile(r"k bị mất dữ liệu|không bị mất dữ liệu", re.IGNORECASE),
    ),
    "paywall_ads_friction": (
        "Bị khóa tính năng / ép mua Premium / quảng cáo gây phiền",
        re.compile(
            r"quảng cáo|lock hầu hết|khóa.*chi tiêu|phải mua premium|ép.*mua gói|bắt mua gói|bào tiền|bắt nâng cấp|vẫn có quảng cáo|quảng cáo liên tục|toàn quảng cáo|mua premium.*vẫn ko dùng|tự hết hạn",
            re.IGNORECASE,
        ),
        re.compile(r"ko có quảng cáo|ít quảng cáo|ko biết thời gian dài", re.IGNORECASE),
    ),
    "intrusive_ai": (
        "Phàn nàn trợ lý AI hiện gây phiền / khó thao tác",
        re.compile(r"trợ lý ai.*điểm trừ|lạm dụng ai|trợ thủ ai.*bỏ đi", re.IGNORECASE),
        None,
    ),
}


def load_rows(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def matches(text: str, inc: re.Pattern[str], exc: re.Pattern[str] | None) -> bool:
    if not inc.search(text):
        return False
    if exc and exc.search(text):
        return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Count user pain themes in Google Play reviews.")
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV, help="Path to anonymized reviews CSV.")
    parser.add_argument("--verbose", action="store_true", help="Print matched review IDs for audit.")
    args = parser.parse_args()

    if not args.csv.exists():
        print(f"ERROR: CSV file not found: {args.csv}", file=sys.stderr)
        return 1

    all_rows = load_rows(args.csv)
    pf_rows = [r for r in all_rows if r["app"] in TARGET_APPS]
    clean_rows = [
        r
        for r in pf_rows
        if len(r["content"].strip()) >= MIN_CONTENT_LEN and not SPAM_RX.search(r["content"])
    ]
    neg_rows = [r for r in clean_rows if int(r["score"]) <= 3]

    dates = [r["date"] for r in pf_rows if r.get("date")]
    print(f"File: {args.csv.name}")
    print(f"All rows in file: {len(all_rows)}")
    print(f"Target personal-finance apps ({', '.join(sorted(TARGET_APPS))}): {len(pf_rows)}")
    print(f"Date range (target apps): {min(dates)} to {max(dates)}")
    print(f"Substantive non-spam reviews (len >= {MIN_CONTENT_LEN}): N = {len(clean_rows)}")
    print(f"  - By app: {dict(Counter(r['app'] for r in clean_rows))}")
    print(f"  - Low rating (1-3 stars): {len(neg_rows)}/{len(clean_rows)} ({len(neg_rows)/len(clean_rows)*100:.1f}%)")
    print()

    any_pain_ids: set[str] = set()
    print("=== THEME COUNTS (denominator N = substantive non-spam reviews) ===")
    for _, (label, inc, exc) in CATEGORIES.items():
        matched = [r for r in clean_rows if matches(r["content"], inc, exc)]
        for r in matched:
            any_pain_ids.add(r["review_id"])
        pct = len(matched) / len(clean_rows) * 100 if clean_rows else 0.0
        print(f"- {label}: {len(matched)}/{len(clean_rows)} ({pct:.1f}%)")
        if args.verbose:
            for r in matched:
                print(f"    [{r['review_id']}] ({r['app']}, {r['score']}*, {r['date']}): {r['content'][:160]}")

    pct_any = len(any_pain_ids) / len(clean_rows) * 100 if clean_rows else 0.0
    print(f"\nAny of the above pain themes (deduplicated): {len(any_pain_ids)}/{len(clean_rows)} ({pct_any:.1f}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

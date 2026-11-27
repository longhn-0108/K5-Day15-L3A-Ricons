"""Tạo video demo có giọng đọc cho Web Demo Ricons.

Quy trình (chạy lại được, mỗi bước cache vào demo/build/):
  1. TTS   : mỗi "nhịp" (beat) có lời thoại -> edge-tts -> mp3 + mốc câu (cho phụ đề)
  2. Quay  : chạy `run.py web` ở cổng riêng, Playwright thao tác theo kịch bản,
             mỗi nhịp kéo dài ít nhất bằng audio của nó; ghi lại mốc thời gian
  3. Ghép  : cắt từng nhịp ra khỏi video thô (bỏ đoạn chờ model / lỗi 503),
             ghép audio, burn phụ đề -> demo/out/demo.mp4 (+ demo.srt)

Cài một lần:
  python -m pip install --user edge-tts playwright imageio-ffmpeg
  python -m playwright install chromium

Chạy:
  python demo/make_demo.py                      # cả video (tốn 3 lượt gọi model)
  python demo/make_demo.py --scenes s0,s1,s2    # xem thử, không gọi model
  python demo/make_demo.py --voice vi-VN-NamMinhNeural
"""
import argparse
import asyncio
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEMO = os.path.join(ROOT, "demo")
BUILD = os.path.join(DEMO, "build")
OUT = os.path.join(DEMO, "out")

W, H = 1920, 1080
FPS = 30
PORT = 8010
TAIL = 0.35          # nghỉ sau mỗi câu thoại (giây)
APP = f"http://127.0.0.1:{PORT}/?user=user_van_phong&month=2026-11&day=15"

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


# --------------------------------------------------------------------------
# Kịch bản: mỗi cảnh gồm nhiều nhịp. Mỗi nhịp: lời thoại (say) + thao tác (do).
# Thao tác chạy ngay đầu nhịp, audio phát cùng lúc; nhịp kết thúc khi audio hết.
# --------------------------------------------------------------------------
def title_card(d, _dur):
    d.card("Ricons", "Cảnh báo sớm ngân sách &amp; gợi ý cắt giảm chi tiêu",
           "Track E · Demo bản chạy thử")


def ledger_alert(d, _dur):
    d.goto_app()
    d.highlight(["#ruleBanner", "#ledgerBody tr:nth-child(1)"])
    d.move_to("#ledgerBody tr:nth-child(1) td:last-child")


def ledger_code(d, _dur):
    d.highlight(["#ledgerHeading"])
    d.move_to("#ledgerHeading")


def essentials(d, _dur):
    rows = [f"#ledgerBody tr:nth-child({i})" for i in (5, 6, 7)]
    d.highlight([rows])          # một khung chung cho 3 dòng liền nhau
    d.move_to(rows[0] + " .tag", 0.5)
    d.move_to(rows[2] + " .tag", 0.9)


def candidates(d, _dur):
    items = ["#candList li:nth-child(1)", "#candList li:nth-child(2)"]
    d.highlight(items)
    d.move_to(items[0] + " strong", 0.6)
    d.pause(0.8)
    d.move_to(items[1] + " strong", 0.6)


def ask(label):
    """Gõ câu hỏi của kịch bản `label` (lấy từ data-q của nút) trong lúc đọc lời thoại,
    hết lời mới bấm Phân Tích -> lỗi/chờ model luôn rơi vào nhịp WAIT (bị cắt)."""
    def _do(d, dur):
        d.scroll_to_top()
        d.type_question(label, dur)
    _do.chip = label
    return _do


def show_answer(d, dur):
    d.highlight(["#answerContainer"])
    d.scroll_into_view("#answerContainer", 0.9)
    d.move_to("#answerContainer", 0.6)
    d.scroll_answer(max(dur - 1.8, 0.5))


def action_bar(d, _dur):
    d.scroll_into_view("#actionBar", 0.6)
    d.highlight(["#actionBar"])
    d.move_to("#actionBar .apply", 0.5)
    d.pause(0.9)
    d.move_to("#actionBar .btn-action:nth-child(3)", 0.9)   # chỉ rê, không bấm


def trace(d, _dur):
    d.scroll_into_view("#traceDetails", 0.6)
    d.highlight(["#traceDetails"])
    d.move_to("#traceSummaryText", 0.6)


def outro_card(d, _dur):
    d.card("Ricons", "Code tính số · AI chọn cách cắt giảm · Người dùng quyết định",
           "github: K5-Day15-L3A-Ricons")


WAIT = "__wait__"   # nhịp chờ model trả lời: chỉ giữ ~1,5 giây đầu/cuối

SCENES = [
    ("s0", [("Đây là Ricons, trợ lý cảnh báo sớm ngân sách cho nhân viên văn phòng trẻ.", title_card)]),
    ("s1", [("Ngày 15 tháng 11, nhóm ăn uống đã dùng 85% hạn mức, vượt ngưỡng cảnh báo sớm 80%.", ledger_alert),
            ("Con số này do code Python tính, không phải AI.", ledger_code)]),
    ("s2", [("Tiền nhà, điện nước và thuốc là khoản thiết yếu, được loại ra trước khi gửi cho AI.", essentials),
            ("AI chỉ được chọn trong các khoản chi lặp lại như GrabFood, ShopeeFood.", candidates)]),
    ("s3", [("Người dùng hỏi: nếu bớt hai đơn ở mỗi chỗ hay đặt thì giữ lại được bao nhiêu?", ask("B01")),
            (None, WAIT),
            ("Hệ thống đưa ra số tiền giữ lại được cho từng cách cắt giảm.", show_answer),
            ("Người dùng tự chọn: áp dụng, bỏ qua, hoặc tạm tắt cảnh báo.", action_bar)]),
    ("s4", [("Mỗi câu hỏi chỉ gọi model một lần, mất khoảng hai đến ba giây.", trace)]),
    ("s5", [("Ca khó: người dùng hỏi có nên bớt mua thuốc không.", ask("B07")),
            (None, WAIT),
            ("Hệ thống khẳng định không nên, và chỉ gợi ý điều chỉnh các khoản không thiết yếu.", show_answer)]),
    ("s6", [("Câu cuối chỉ có hai chữ: Lố rồi.", ask("B05")),
            (None, WAIT),
            ("Hệ thống không đoán, mà hỏi lại tháng và nhóm chi tiêu.", show_answer)]),
    ("s7", [("Code tính số, AI chọn cách cắt giảm, và người dùng luôn là người quyết định cuối cùng.", outro_card)]),
]


# --------------------------------------------------------------------------
# Tiện ích
# --------------------------------------------------------------------------
def ffmpeg_exe():
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def run_ff(args, cwd=None):
    cmd = [ffmpeg_exe(), "-hide_banner", "-loglevel", "error", "-y", *args]
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise RuntimeError("ffmpeg lỗi:\n" + " ".join(cmd) + "\n" + r.stderr)


def media_duration(path):
    r = subprocess.run([ffmpeg_exe(), "-hide_banner", "-i", path], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r.stderr)
    if not m:
        raise RuntimeError(f"Không đọc được độ dài {path}")
    h, mi, s = m.groups()
    return int(h) * 3600 + int(mi) * 60 + float(s)


# --------------------------------------------------------------------------
# 1. TTS
# --------------------------------------------------------------------------
async def _tts_one(text, voice, rate, mp3_path):
    import edge_tts
    comm = edge_tts.Communicate(text, voice, rate=rate, boundary="SentenceBoundary")
    sentences = []
    with open(mp3_path, "wb") as f:
        async for chunk in comm.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] in ("SentenceBoundary", "WordBoundary"):
                sentences.append({"start": chunk["offset"] / 1e7,
                                  "end": (chunk["offset"] + chunk["duration"]) / 1e7,
                                  "text": chunk["text"]})
    return sentences


def tts_all(beats, voice, rate):
    os.makedirs(os.path.join(BUILD, "audio"), exist_ok=True)
    for b in beats:
        if not b["say"]:
            b["dur"] = 0.0
            continue
        key = hashlib.sha1(f"{voice}|{rate}|{b['say']}".encode()).hexdigest()[:10]
        mp3 = os.path.join(BUILD, "audio", f"{b['id']}-{key}.mp3")
        meta = mp3[:-4] + ".json"
        if not (os.path.exists(mp3) and os.path.exists(meta)):
            print(f"  TTS {b['id']}: {b['say']}")
            for attempt in range(1, 9):   # dịch vụ edge-tts hay chập chờn: thử lại
                try:
                    sents = asyncio.run(_tts_one(b["say"], voice, rate, mp3))
                    break
                except Exception as e:
                    if attempt == 8:
                        raise
                    print(f"    thử lại ({type(e).__name__})")
                    time.sleep(1.5 * attempt)
            with open(meta, "w", encoding="utf-8") as f:
                json.dump(sents, f, ensure_ascii=False)
        with open(meta, encoding="utf-8") as f:
            b["sentences"] = json.load(f)
        b["mp3"] = mp3
        b["dur"] = media_duration(mp3)


# --------------------------------------------------------------------------
# 2. Quay màn hình
# --------------------------------------------------------------------------
OVERLAY_JS = r"""
(() => {
  if (document.getElementById('__cur')) return;   // set_content giữ nguyên window cũ
  const css = document.createElement('style');
  css.textContent = `
    #__cur { position: fixed; left: 0; top: 0; width: 30px; height: 30px; z-index: 2147483647;
             pointer-events: none; transform: translate(-4px,-2px); transition: transform .08s; }
    #__cur.down { transform: translate(-4px,-2px) scale(.85); }
    .__ring { position: fixed; z-index: 2147483646; pointer-events: none; width: 16px; height: 16px;
              margin: -8px 0 0 -8px; border-radius: 50%; border: 3px solid #F59E0B;
              animation: __ring .5s ease-out forwards; }
    @keyframes __ring { to { transform: scale(3.2); opacity: 0; } }
    .__hl { position: fixed; z-index: 2147483640; pointer-events: none; border-radius: 10px;
            border: 3px solid #F59E0B; box-shadow: 0 0 0 6px rgba(245,158,11,.18);
            opacity: 0; transition: opacity .25s; }
    .__hl.on { opacity: 1; }`;
  document.head.appendChild(css);
  const cur = document.createElement('div');
  cur.id = '__cur';
  cur.innerHTML = '<svg viewBox="0 0 24 24" width="30" height="30"><path d="M4 2l15 11-6.5 1.2 3.8 7.3-2.7 1.4-3.8-7.3L4 20z" fill="#111" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/></svg>';
  document.body.appendChild(cur);
  addEventListener('mousemove', e => { cur.style.left = e.clientX + 'px'; cur.style.top = e.clientY + 'px'; }, true);
  addEventListener('mousedown', e => {
    cur.classList.add('down');
    const r = document.createElement('div'); r.className = '__ring';
    r.style.left = e.clientX + 'px'; r.style.top = e.clientY + 'px';
    document.body.appendChild(r); setTimeout(() => r.remove(), 600);
  }, true);
  addEventListener('mouseup', () => cur.classList.remove('down'), true);

  let boxes = [];
  function place() {
    boxes.forEach(b => {
      // b.sel là chuỗi (1 phần tử) hoặc mảng (1 khung bao quanh cả nhóm)
      const els = [].concat(b.sel).map(s => document.querySelector(s)).filter(Boolean);
      if (!els.length) return;
      const rs = els.map(e => e.getBoundingClientRect()), p = 6;
      const r = { left: Math.min(...rs.map(x => x.left)), top: Math.min(...rs.map(x => x.top)) };
      r.width = Math.max(...rs.map(x => x.right)) - r.left;
      r.height = Math.max(...rs.map(x => x.bottom)) - r.top;
      Object.assign(b.div.style, { left: (r.left - p) + 'px', top: (r.top - p) + 'px',
                                   width: (r.width + 2 * p) + 'px', height: (r.height + 2 * p) + 'px' });
    });
    requestAnimationFrame(place);
  }
  requestAnimationFrame(place);
  const ease = t => t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
  window.__demo = {
    highlight(sels) {
      boxes.forEach(b => { b.div.classList.remove('on'); setTimeout(() => b.div.remove(), 300); });
      boxes = sels.map(sel => { const div = document.createElement('div'); div.className = '__hl';
                                document.body.appendChild(div); return { sel, div }; });
      requestAnimationFrame(() => requestAnimationFrame(() => boxes.forEach(b => b.div.classList.add('on'))));
    },
    scrollTo(y, ms) {
      const y0 = scrollY, max = document.documentElement.scrollHeight - innerHeight;
      y = Math.max(0, Math.min(y, max));
      return new Promise(res => {
        if (Math.abs(y - y0) < 2) return res();
        const t0 = performance.now();
        (function step(t) {
          const k = Math.min(1, (t - t0) / ms);
          scrollTo(0, y0 + (y - y0) * ease(k));
          k < 1 ? requestAnimationFrame(step) : res();
        })(t0);
      });
    },
    elTop(sel) { return document.querySelector(sel).getBoundingClientRect().top + scrollY; },
    elBottom(sel) { return document.querySelector(sel).getBoundingClientRect().bottom + scrollY; },
  };
})();
"""

CARD_HTML = """<!DOCTYPE html><html lang="vi"><head><meta charset="utf-8"><style>
html,body{{margin:0;height:100%;background:#F6F5F1;font-family:"Segoe UI",Inter,Roboto,sans-serif;color:#16181D}}
.wrap{{height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:22px}}
.bar{{width:96px;height:8px;border-radius:4px;background:#134E4A}}
h1{{margin:0;font-size:120px;letter-spacing:-2px;color:#134E4A}}
p{{margin:0;font-size:40px;color:#16181D}}
small{{font-size:24px;color:#737A87}}
.wrap>*{{animation:in .7s ease-out both}} p{{animation-delay:.15s}} small{{animation-delay:.3s}}
@keyframes in{{from{{opacity:0;transform:translateY(16px)}}}}
</style></head><body><div class="wrap"><div class="bar"></div><h1>{title}</h1><p>{sub}</p><small>{foot}</small></div></body></html>"""


class Director:
    def __init__(self, page):
        self.page = page
        self.mx, self.my = W * 0.62, H * 0.55
        self.t0 = time.monotonic()

    def now(self):
        return time.monotonic() - self.t0

    def pause(self, s):
        time.sleep(max(0.0, s))

    def _inject(self):
        self.page.evaluate(OVERLAY_JS)
        self.page.mouse.move(self.mx, self.my)

    def card(self, title, sub, foot):
        self.page.set_content(CARD_HTML.format(title=title, sub=sub, foot=foot))
        self._inject()
        self.page.evaluate("() => document.getElementById('__cur').style.display = 'none'")

    def goto_app(self):
        self.page.goto(APP)
        self.page.wait_for_selector("#ledgerBody tr .cat-name")
        self.page.wait_for_selector("#candList li strong")
        self._inject()
        # chừa chỗ cuối trang để phần cuối (Trace) cuộn lên trên vùng phụ đề
        self.page.evaluate("() => document.body.style.paddingBottom = '320px'")
        badge = self.page.inner_text("#modelBadge")
        if "fake" in badge.lower():
            print("  ! Cảnh báo: model đang ở chế độ giả (fake) — kiểm tra .env")

    def highlight(self, sels):
        self.page.evaluate("s => __demo.highlight(s)", sels)

    def move_to(self, sel, secs=0.7):
        box = self.page.locator(sel).first.bounding_box()
        x, y = box["x"] + min(box["width"] / 2, 60), box["y"] + box["height"] / 2
        if sel.endswith("td:last-child") or "btn" in sel or "apply" in sel:
            x = box["x"] + box["width"] / 2
        x0, y0 = self.mx, self.my
        t_start = time.monotonic()
        while True:                       # theo thời gian thực, không theo số bước
            k = min(1.0, (time.monotonic() - t_start) / secs)
            e = 2 * k * k if k < .5 else 1 - (-2 * k + 2) ** 2 / 2
            self.page.mouse.move(x0 + (x - x0) * e, y0 + (y - y0) * e)
            if k >= 1:
                break
            time.sleep(1 / 60)
        self.mx, self.my = x, y

    def click(self, sel, secs=0.6):
        self.move_to(sel, secs)
        self.pause(0.2)
        self.page.mouse.click(self.mx, self.my)

    def type_question(self, label, dur):
        """Rê tới ô nhập, gõ câu hỏi (dàn đều trong thời lượng lời thoại), bấm Phân Tích."""
        q = self.page.get_attribute(f".chip:has-text('{label}')", "data-q")
        self.highlight(["#queryInput"])
        self.click("#queryInput", 0.6)
        self.page.fill("#queryInput", "")
        type_secs = max(0.6, min(dur - 2.2, len(q) / 18))
        t_start = time.monotonic()
        shown = 0
        while shown < len(q):
            k = min(1.0, (time.monotonic() - t_start) / type_secs)
            n = max(shown + 1, int(len(q) * k))
            self.page.evaluate("([v]) => { const t = document.getElementById('queryInput');"
                               " t.value = v; t.scrollTop = t.scrollHeight; }", [q[:n]])
            shown = n
            time.sleep(1 / 30)
        self.highlight(["#submitBtn"])
        self.move_to("#submitBtn", 0.6)
        self.pending_submit = True

    def submit(self):
        self.page.mouse.click(self.mx, self.my)

    def scroll_to_top(self):
        self.page.evaluate("() => __demo.scrollTo(0, 700)")

    def scroll_into_view(self, sel, secs):
        y = self.page.evaluate("s => __demo.elTop(s)", sel) - 110
        self.page.evaluate("([y, ms]) => __demo.scrollTo(y, ms)", [y, int(secs * 1000)])

    def scroll_answer(self, secs):
        """Cuộn chậm để thấy hết câu trả lời (nếu dài hơn màn hình)."""
        bottom = self.page.evaluate("() => __demo.elBottom('#answerContainer')")
        y = bottom - H + 140
        if y > self.page.evaluate("() => scrollY") + 20:
            self.page.evaluate("([y, ms]) => __demo.scrollTo(y, ms)", [y, int(secs * 1000)])

    def wait_answer(self, label, tries=3):
        """Chờ model trả lời; lỗi (503/429) thì đợi rồi bấm lại. Trả về mốc bắt đầu giữ lại."""
        start = self.now()
        for attempt in range(1, tries + 1):
            self.page.wait_for_function(
                "() => { const a = document.getElementById('answerContainer');"
                " return a.classList.contains('answer-body') || a.classList.contains('error'); }",
                timeout=90_000)
            cls = self.page.get_attribute("#answerContainer", "class")
            if "error" not in cls:
                text = self.page.inner_text("#answerContainer")
                summ = self.page.inner_text("#traceSummaryText")
                return start, text, summ
            msg = self.page.inner_text("#answerContainer")
            print(f"  ! {label} lỗi lần {attempt}: {msg[:120]}")
            if attempt == tries:
                raise RuntimeError(f"{label}: model lỗi {tries} lần liền, dừng.")
            time.sleep(6 * attempt)
            self.click("#submitBtn", 0.3)
            start = self.now()


def record(beats):
    from playwright.sync_api import sync_playwright

    raw_dir = os.path.join(BUILD, "raw")
    os.makedirs(raw_dir, exist_ok=True)
    for f in os.listdir(raw_dir):
        os.remove(os.path.join(raw_dir, f))

    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    srv = subprocess.Popen([sys.executable, "run.py", "web", "--no-open", "--port", str(PORT)],
                           cwd=ROOT, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(50):
            try:
                urllib.request.urlopen(f"http://127.0.0.1:{PORT}/", timeout=1)
                break
            except Exception:
                time.sleep(0.2)
        else:
            raise RuntimeError("Web Demo không khởi động được")

        answers = {}
        with sync_playwright() as p:
            browser = p.chromium.launch()
            ctx = browser.new_context(viewport={"width": W, "height": H}, device_scale_factor=1,
                                      record_video_dir=raw_dir, record_video_size={"width": W, "height": H},
                                      locale="vi-VN")
            page = ctx.new_page()
            d = Director(page)
            page.set_content("<html><body style='background:#F6F5F1'></body></html>")
            d.pause(0.5)
            last_chip = None
            for b in beats:
                start = d.now()
                if b["do"] == WAIT:
                    start, text, summ = d.wait_answer(last_chip)
                    answers[last_chip] = {"answer": text, "trace": summ}
                    print(f"  [{last_chip}] {summ}\n    {text[:400].replace(chr(10), ' ')}", flush=True)
                    end = d.now()
                    b["pieces"] = [(start, min(end, start + 0.7))]
                    if end - start > 1.6:
                        b["pieces"].append((end - 0.6, end + 0.4))
                    else:
                        b["pieces"] = [(start, end + 0.4)]
                    d.pause(0.4)
                    continue
                b["do"](d, b["dur"])
                if getattr(b["do"], "chip", None):
                    last_chip = b["do"].chip
                target = start + (b["dur"] + TAIL if b["dur"] else 1.0)
                d.pause(target - d.now())
                b["pieces"] = [(start, d.now())]
                if getattr(d, "pending_submit", False):   # bấm Phân Tích khi lời thoại đã xong
                    d.pending_submit = False
                    d.submit()
            d.pause(0.3)
            video = page.video
            ctx.close()
            browser.close()
            raw = video.path()
    finally:
        srv.terminate()
    with open(os.path.join(BUILD, "answers.json"), "w", encoding="utf-8") as f:
        json.dump(answers, f, ensure_ascii=False, indent=2)
    return raw, answers


# --------------------------------------------------------------------------
# 3. Ghép video + audio + phụ đề
# --------------------------------------------------------------------------
def merge_bounds(sents, max_chars=80, hard=95):
    """edge-tts trả mốc theo từng cụm (cắt ở dấu phẩy): gộp cụm ngắn liền nhau
    thành một dòng phụ đề, tránh dòng chỉ có 1–2 chữ hiện chớp nhoáng."""
    out = []
    for s in sents:
        if out:
            prev = out[-1]
            joined = prev["text"] + " " + s["text"]
            short = min(len(prev["text"]), len(s["text"])) < 20
            if len(joined) <= max_chars or (short and len(joined) <= hard):
                out[-1] = {"start": prev["start"], "end": s["end"], "text": joined}
                continue
        out.append(dict(s))
    return out


def split_caption(text, start, end, max_chars=80):
    """Chia câu dài thành nhiều dòng phụ đề (cắt ở dấu phẩy gần giữa câu nhất,
    không để mẩu nào dưới 20 ký tự), chia thời gian theo số ký tự."""
    def cut(s):
        if len(s) <= max_chars:
            return [s]
        ok = lambda i: 20 <= i <= len(s) - 20
        marks = [m.end() for m in re.finditer(r"[,:;]\s", s) if ok(m.end())] or \
                [m.start() for m in re.finditer(r"\s", s) if ok(m.start())]
        k = min(marks, key=lambda i: abs(i - len(s) / 2))
        return cut(s[:k].strip()) + cut(s[k:].strip())
    parts = cut(text.strip())
    total = sum(len(p) for p in parts) or 1
    out, t = [], start
    for p in parts:
        dt = (end - start) * len(p) / total
        out.append((t, t + dt, p))
        t += dt
    return out


def srt_time(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def assemble(beats, raw):
    pdir = os.path.join(BUILD, "pieces")
    os.makedirs(pdir, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(pdir):
        os.remove(os.path.join(pdir, f))

    files, captions, t_out, idx = [], [], 0.0, 0
    for b in beats:
        for k, (s, e) in enumerate(b["pieces"]):
            idx += 1
            seg = max(e - s, 0.1)
            dur = max(seg, b["dur"] + 0.1) if (b["say"] and k == 0) else seg
            out = os.path.join(pdir, f"{idx:03}.mp4")
            vf = f"fps={FPS},scale={W}:{H},format=yuv420p"
            if dur > seg + 0.02:
                vf += f",tpad=stop_mode=clone:stop_duration={dur - seg + 0.1:.3f}"
            args = ["-ss", f"{s:.3f}", "-t", f"{seg:.3f}", "-i", raw]
            if b["say"] and k == 0:
                args += ["-i", b["mp3"]]
                amap = ["-map", "0:v", "-map", "1:a", "-af", f"apad,atrim=0:{dur:.3f}"]
            else:
                args += ["-f", "lavfi", "-t", f"{dur:.3f}", "-i", "anullsrc=r=48000:cl=stereo"]
                amap = ["-map", "0:v", "-map", "1:a"]
            run_ff(args + amap + ["-vf", vf, "-t", f"{dur:.3f}", "-c:v", "libx264", "-preset", "medium",
                                  "-crf", "18", "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2", out])
            if b["say"] and k == 0:
                for sen in merge_bounds(b["sentences"]):
                    captions += split_caption(sen["text"], t_out + sen["start"], t_out + sen["end"])
            files.append(out)
            t_out += media_duration(out)

    with open(os.path.join(pdir, "list.txt"), "w", encoding="utf-8") as f:
        f.writelines(f"file '{os.path.basename(p)}'\n" for p in files)
    run_ff(["-f", "concat", "-safe", "0", "-i", "list.txt", "-c", "copy", "joined.mp4"], cwd=pdir)

    srt = os.path.join(OUT, "demo.srt")
    with open(srt, "w", encoding="utf-8") as f:
        for i, (s, e, text) in enumerate(captions, 1):
            f.write(f"{i}\n{srt_time(s)} --> {srt_time(e)}\n{text}\n\n")

    style = ("FontName=Segoe UI,FontSize=11,PrimaryColour=&H00FFFFFF,OutlineColour=&H99000000,"
             "BorderStyle=3,Outline=6,Shadow=0,MarginV=22")
    with open(srt, "rb") as src, open(os.path.join(pdir, "subs.srt"), "wb") as dst:
        dst.write(src.read())
    run_ff(["-i", "joined.mp4", "-vf", f"subtitles=subs.srt:fontsdir=C\\\\:/Windows/Fonts:force_style='{style}'",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-c:a", "copy", "-movflags", "+faststart",
            "final.mp4"], cwd=pdir)
    final = os.path.join(OUT, "demo.mp4")
    os.replace(os.path.join(pdir, "final.mp4"), final)
    return final, t_out


# --------------------------------------------------------------------------
def build_beats(only):
    beats = []
    for sid, items in SCENES:
        if only and sid not in only:
            continue
        for i, (say, do) in enumerate(items):
            beats.append({"id": f"{sid}{chr(97 + i)}", "say": say, "do": do})
    return beats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenes", help="vd s0,s1,s2 (mặc định: tất cả)")
    ap.add_argument("--voice", default="vi-VN-HoaiMyNeural")
    ap.add_argument("--rate", default="+5%")
    args = ap.parse_args()
    only = set(args.scenes.split(",")) if args.scenes else None

    beats = build_beats(only)
    print("1/3 Sinh giọng đọc…")
    tts_all(beats, args.voice, args.rate)
    print("2/3 Quay màn hình…")
    raw, answers = record(beats)
    print("3/3 Ghép video…")
    final, secs = assemble(beats, raw)
    print(f"Xong: {os.path.relpath(final, ROOT)} ({secs:.1f} giây) · phụ đề: demo/out/demo.srt")


if __name__ == "__main__":
    main()

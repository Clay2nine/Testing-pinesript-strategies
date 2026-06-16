#!/usr/bin/env python3
import base64, html, pathlib

def b64(p):
    return base64.b64encode(pathlib.Path(p).read_bytes()).decode()

img_panel  = b64("lz_1_panel.png")
img_map    = b64("lz_2_screenmap.png")
img_stack  = b64("lz_3_stack.png")
img_play   = b64("lz_4_playbook.png")
pine = pathlib.Path("VolComp_AI_PROP_OPT.pine").read_text()
pine_esc = html.escape(pine)

def fig(b, cap):
    return (f'<figure><img src="data:image/png;base64,{b}" alt="{cap}"/>'
            f'<figcaption>{cap}</figcaption></figure>')

doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>VolComp AI+ PROP — MNQ 5-Minute Scalping Lesson</title>
<style>
  :root {{ --ink:#1d2129; --sub:#5b6470; --bg:#e9ebef; --card:#ffffff;
           --accent:#1857c4; --amber:#a9760a; --green:#0c8f5f; --red:#c0392b; --line:#d4d8df; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--ink);
          font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif; line-height:1.6; }}
  .wrap {{ max-width:1100px; margin:0 auto; padding:32px 22px 80px; }}
  header {{ background:var(--card); border:1px solid var(--line); border-radius:16px;
            padding:34px 30px; text-align:center; box-shadow:0 2px 10px rgba(0,0,0,.05); }}
  header h1 {{ margin:0 0 6px; font-size:30px; }}
  header p {{ margin:0; color:var(--sub); font-size:16px; }}
  .badge {{ display:inline-block; margin-top:14px; background:#eef3ff; color:var(--accent);
            border:1px solid #cfe0ff; padding:6px 14px; border-radius:999px; font-weight:700; font-size:13px; }}
  section {{ background:var(--card); border:1px solid var(--line); border-radius:16px;
            padding:26px 30px; margin-top:24px; box-shadow:0 2px 10px rgba(0,0,0,.04); }}
  h2 {{ font-size:22px; margin:0 0 6px; }}
  h2 .num {{ color:#fff; background:var(--accent); border-radius:8px; padding:2px 11px; margin-right:10px; font-size:18px; }}
  h3 {{ font-size:17px; margin:20px 0 6px; color:var(--accent); }}
  figure {{ margin:18px 0 6px; }}
  figure img {{ width:100%; border-radius:12px; border:1px solid var(--line); }}
  figcaption {{ text-align:center; color:var(--sub); font-size:13px; margin-top:6px; }}
  table {{ width:100%; border-collapse:collapse; margin:14px 0; font-size:15px; }}
  th,td {{ border:1px solid var(--line); padding:9px 12px; text-align:left; vertical-align:top; }}
  th {{ background:#f3f5f8; }}
  ol,ul {{ margin:8px 0 8px 4px; padding-left:22px; }}
  li {{ margin:5px 0; }}
  .tip {{ background:#fff8e6; border:1px solid #efdca0; border-left:5px solid var(--amber);
          border-radius:10px; padding:14px 16px; margin:16px 0; }}
  .warn {{ background:#fdecea; border:1px solid #f3c2bd; border-left:5px solid var(--red);
           border-radius:10px; padding:14px 16px; margin:16px 0; }}
  .codebar {{ display:flex; justify-content:space-between; align-items:center;
              background:#f3f5f8; border:1px solid var(--line); border-bottom:none;
              border-radius:12px 12px 0 0; padding:8px 14px; font-weight:700; font-size:14px; }}
  .codebar button {{ font:inherit; font-size:13px; cursor:pointer; border:1px solid var(--accent);
              background:var(--accent); color:#fff; border-radius:7px; padding:5px 12px; }}
  pre {{ margin:0; max-height:520px; overflow:auto; background:#0f1117; color:#e6e6ea;
         border-radius:0 0 12px 12px; padding:16px; font-size:12.5px; line-height:1.45;
         font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; white-space:pre; }}
  footer {{ text-align:center; color:var(--sub); font-size:13px; margin-top:30px; }}
  @media print {{ body {{ background:#fff; }} section,header {{ box-shadow:none; }} pre {{ max-height:none; }} }}
</style></head>
<body><div class="wrap">

<header>
  <h1>VolComp AI+ PROP — MNQ 5-Minute Scalping Lesson</h1>
  <p>A complete confluence-stack guide for prop scalping the Micro E-mini Nasdaq (MNQ)</p>
  <div class="badge">Default prop confidence: 83% &nbsp;·&nbsp; A+ tier: 88%</div>
</header>

<section>
  <h2><span class="num">0</span>How to use this lesson</h2>
  <p>Your chart is not one indicator — it is a <strong>confluence machine</strong>. The skill is to stop
  reading 50 labels and instead read <strong>5 zones</strong> that answer <strong>5 questions</strong>, in order.
  This document contains the diagrams, the step-by-step playbook, and the full
  <strong>VolComp AI+ PROP</strong> Pine Script (v6) source at the end — everything in one file.</p>
</section>

<section>
  <h2><span class="num">1</span>Panel Decoder — reading the VolComp AI+ PROP panel</h2>
  {fig(img_panel,"Panel rows explained — PROP is your trigger row")}
  <table>
    <tr><th>Row</th><th>Reads like</th><th>Meaning</th></tr>
    <tr><td><b>ACT</b></td><td>ACT BUY ^ 56% | PROP:BxV+E+H+</td><td>Aggressive volume direction &amp; %. The B/V/E/H tag = filter status (+ pass, x fail): Body, Volatility, EMA-proximity, HTF bias.</td></tr>
    <tr><td><b>PROP ★</b></td><td>A+ BUY ^ 90% (req 83/A+ 88)</td><td><b>Your trigger.</b> Green A+/B+ BUY ^ = long, red A+/B+ SELL v = short, gray SKIP = stand aside.</td></tr>
    <tr><td><b>DOM</b></td><td>DOM BUY ^ 67% | 3012</td><td>Total volume direction, % and raw volume.</td></tr>
    <tr><td><b>AI</b></td><td>AI prob (up) % 55</td><td>ML bias. &gt;62 bullish, &lt;38 bearish. Confirms — never triggers alone.</td></tr>
    <tr><td><b>COACH</b></td><td>COACH HOLD =</td><td>Wider signal engine. BUY / SELL / HOLD — confluence &amp; exits.</td></tr>
    <tr><td><b>STATE</b></td><td>STATE FLAT</td><td>Position tracker: FLAT / IN-LONG / IN-SHORT / EXIT.</td></tr>
  </table>
</section>

<section>
  <h2><span class="num">2</span>Screen Map — the 5 zones of your chart</h2>
  {fig(img_map,"The 5 functional zones and the order to read them")}
  <ol>
    <li><b>MTF Bias table</b> — which way is the market leaning across timeframes?</li>
    <li><b>Level Rail</b> (NQSPROP SL/Trigger/Entry/TP + SMAs) — exact entry/stop/target prices.</li>
    <li><b>Signal Cluster</b> (ML/ICT/OB bias, scores, candlestick patterns) — is there a real edge?</li>
    <li><b>VolComp PROP panel</b> — does volume confirm it (≥83%)?</li>
    <li><b>ORB Dashboard</b> (risk, size, daily limit) — am I allowed to trade?</li>
  </ol>
</section>

<section>
  <h2><span class="num">3</span>The Confluence Stack — the decision funnel</h2>
  {fig(img_stack,"Six filters that must all agree before an A+ scalp")}
  <ol>
    <li><b>Direction</b> — MTF table aligned (example: 1m/15m Strong Sell, Alignment Bearish → shorts only).</li>
    <li><b>Trend engine</b> — MNQ ML PROP BIAS: SELL (20 SMA &lt; 200 SMA) + ICT/OB sell bias agree.</li>
    <li><b>Trigger</b> — PROP A+ ENTRY + VolComp PROP row red A+/B+ SELL ≥83% + NQSPROP trigger crossed.</li>
    <li><b>Price confirm</b> — bearish candlestick (PinBar/Engulfing/Long-Upper-Shadow) + score 90–100% / RVI.</li>
    <li><b>Permission</b> — ORB dashboard: risk OK, daily limit not hit, not STAND-DOWN.</li>
    <li><b>Execute</b> — entry/stop/target straight off the NQSPROP level rail.</li>
  </ol>
</section>

<section>
  <h2><span class="num">4</span>Playbook &amp; Guardrails</h2>
  {fig(img_play,"Per-bar routine, prop guardrails, and signal grades")}
  <h3>The routine (every 5-minute bar close)</h3>
  <ol type="A">
    <li>Check MTF Bias table → pick side. No alignment = wait.</li>
    <li>Confirm ML/SMA/ICT bias agrees (20 vs 200 SMA regime).</li>
    <li>Wait for PROP A+ / VolComp PROP row to fire your side ≥83%.</li>
    <li>Need a candlestick confirm + score 90%+ at a level.</li>
    <li>Dashboard green (risk ok, limit not hit) → take it.</li>
    <li>Enter/Stop/Target straight off the NQSPROP level rail.</li>
  </ol>
  <div class="warn"><b>Guardrails (do NOT break):</b>
    <ul>
      <li>STAND DOWN / DAILY LIMIT HIT → stop for the day.</li>
      <li>No green/red PROP row → no trade (volume isn't there).</li>
      <li>Filters disagree → skip. Counter-trend signal → exit, don't hope.</li>
      <li>Risk per trade fixed (~$200); A+ = full size, B+ = reduced, SKIP/WATCH = flat.</li>
    </ul>
  </div>
  <div class="tip"><b>Grades:</b> ELITE A+ / A+ = every layer aligned (full-conviction scalp).
    WATCH / NEXT / READY = setup forming, not yet valid (prepare, don't fire).</div>
  <div class="tip"><b>Coaching tip:</b> keep this dense layout for study, but execute from a second
    clean chart — price + 20/200 SMA + the VolComp PROP row + the NQSPROP level rail. Same edge, zero clutter.</div>
</section>

<section>
  <h2><span class="num">5</span>The Indicator — VolComp AI+ PROP (Pine Script v6)</h2>
  <p>Paste this into TradingView → Pine Editor → Add to chart. Defaults are tuned for MNQ 5-minute
  prop scalping (83% prop confidence, EMA 20/200, no-reversal filters).</p>
  <div class="codebar"><span>VolComp_AI_PROP_OPT.pine</span>
    <button onclick="navigator.clipboard.writeText(document.getElementById('pine').innerText)">Copy code</button></div>
  <pre id="pine">{pine_esc}</pre>
</section>

<footer>VolComp AI+ PROP · MNQ 5-minute scalping lesson · for educational use — not financial advice.</footer>
</div></body></html>"""

pathlib.Path("VolComp_AI_PROP_LESSON.html").write_text(doc)
print("wrote VolComp_AI_PROP_LESSON.html", len(doc), "bytes")

#!/usr/bin/env python3
# Builds an annotated user-manual for the VolComp AI+ PROP indicator (MNQ 5m scalping)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch
import numpy as np

BG = "#0c0c10"
FG = "#e8e8ec"
GREEN = "#0e9d77"
RED = "#e0413e"
TEAL = "#13a89a"
MAROON = "#8e1f3d"
BLUE = "#2a6df4"
YELLOW = "#e4c000"
GRAY = "#7d7d86"
ORANGE = "#ff9100"
CALL = "#ffd24d"   # callout color

def callout(ax, xy, xytext, text, color=CALL, fs=12, ha="left"):
    ax.annotate(text, xy=xy, xytext=xytext, color=color, fontsize=fs, ha=ha, va="center",
                fontweight="bold",
                arrowprops=dict(arrowstyle="-|>", color=color, lw=2.2,
                                connectionstyle="arc3,rad=0.0"),
                bbox=dict(boxstyle="round,pad=0.4", fc="#15151c", ec=color, lw=1.4))

# =====================================================================
# IMAGE 1 — PANEL DECODER
# =====================================================================
fig, ax = plt.subplots(figsize=(15.5, 9.2))
fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")

ax.text(50, 97, "VolComp AI+ PROP  —  PANEL DECODER", color=FG, fontsize=22,
        fontweight="bold", ha="center")
ax.text(50, 93, "Read it top-to-bottom. The PROP row is your trade trigger.", color=GRAY,
        fontsize=13, ha="center")

rows = [
    ("ACT BUY ^ 56%   [AGG-AUTO:NAS] | PROP:BxV+E+H+", GREEN, "white"),
    ("PROP  A+ BUY ^  90%  (req 83 / A+ 88)",          GREEN, "white"),
    ("DOM BUY ^ 67% | 3012.00",                         TEAL,  "white"),
    ("AI prob (up) % 55.07",                            BLUE,  "white"),
    ("COACH HOLD = 67% (-)",                            YELLOW,"black"),
    ("STATE FLAT",                                      GRAY,  "white"),
]
# panel block on the left
px, pw = 5, 46
top = 84; rh = 9; gap = 1.2
ys = []
for i,(txt,bg,tc) in enumerate(rows):
    y = top - i*(rh+gap)
    ys.append(y)
    ax.add_patch(FancyBboxPatch((px, y-rh/2), pw, rh, boxstyle="round,pad=0.15,rounding_size=1.2",
                                fc=bg, ec="none"))
    ax.text(px+2, y, txt, color=tc, fontsize=12.5, va="center", fontweight="bold")

cx = px+pw+3
notes = [
    "ACT row = AGGRESSIVE volume.\n'^ 56%' = 56% of pushy volume is BUYING.\nThe PROP:B/V/E/H tag = filter status\n(+ pass, x fail): Body, Volatility, EMA, HTF.",
    "*** YOUR TRIGGER ROW ***\nGreen 'A+/B+ BUY ^' = go LONG.\nRed 'A+/B+ SELL v' = go SHORT.\nGray 'SKIP' = stand aside.\n'req 83/A+ 88' = volume % needed.",
    "DOM row = TOTAL volume direction.\n'^ 67%' = 67% of all volume is buy.\nNumber = raw volume of the bar.",
    "AI/ML bias 0-100. >62 bullish,\n<38 bearish (defaults). Confirms,\ndoes not trigger on its own.",
    "COACH = the wider signal engine\n(A/B stack). BUY / SELL / HOLD.\nUsed for exits & confluence.",
    "STATE machine: FLAT / IN-LONG /\nIN-SHORT / EXIT. Tracks the\nlive position the logic is holding.",
]
ncolors = [GREEN, CALL, TEAL, BLUE, YELLOW, GRAY]
for y, note, col in zip(ys, notes, ncolors):
    ax.annotate(note, xy=(px+pw, y), xytext=(cx, y), color=FG, fontsize=11, va="center", ha="left",
                arrowprops=dict(arrowstyle="-|>", color=col, lw=2.4),
                bbox=dict(boxstyle="round,pad=0.45", fc="#16161e", ec=col, lw=1.6))

# emphasis ring on PROP row
ax.add_patch(FancyBboxPatch((px-0.8, ys[1]-rh/2-0.8), pw+1.6, rh+1.6,
            boxstyle="round,pad=0.15,rounding_size=1.2", fc="none", ec=CALL, lw=3, ls="--"))

ax.text(50, 4, "MNQ 5-minute scalp:  watch ACT + DOM agree, then act ONLY when the PROP row turns green/red.",
        color=CALL, fontsize=12.5, ha="center", fontstyle="italic")

plt.tight_layout()
fig.savefig("manual_1_panel.png", dpi=140, facecolor=BG)
plt.close(fig)

# =====================================================================
# IMAGE 2 — ANNOTATED 5m CHART (the setup)
# =====================================================================
rng = np.random.default_rng(7)
n = 46
# build a trend: up then pullback then continuation
base = np.concatenate([
    np.linspace(100, 118, 16),       # up leg
    np.linspace(118, 110, 8),        # pullback to EMA
    np.linspace(110, 132, 14),       # continuation up
    np.linspace(132, 128, 8),        # drift
])
opens, closes, highs, lows = [], [], [], []
prev = base[0]
for i in range(n):
    o = prev
    c = base[i] + rng.normal(0, 0.8)
    hi = max(o, c) + abs(rng.normal(0, 0.9))
    lo = min(o, c) - abs(rng.normal(0, 0.9))
    opens.append(o); closes.append(c); highs.append(hi); lows.append(lo)
    prev = c
opens=np.array(opens); closes=np.array(closes); highs=np.array(highs); lows=np.array(lows)
ema = np.zeros(n); k=2/(20+1); ema[0]=closes[0]
for i in range(1,n): ema[i]=closes[i]*k+ema[i-1]*(1-k)

fig, ax = plt.subplots(figsize=(16, 9))
fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
for i in range(n):
    col = GREEN if closes[i]>=opens[i] else RED
    ax.plot([i,i],[lows[i],highs[i]], color=col, lw=1.3, zorder=2)
    ax.add_patch(Rectangle((i-0.32, min(opens[i],closes[i])), 0.64, abs(closes[i]-opens[i])+0.01,
                           fc=col, ec=col, zorder=3))
ax.plot(range(n), ema, color=ORANGE, lw=2.6, zorder=4, label="EMA 20 (Prop Core)")
ax.fill_between(range(n), ema, lows.min()-3, color=GREEN, alpha=0.05, zorder=1)

ax.set_xlim(-1, n+9); ax.set_ylim(lows.min()-4, highs.max()+5)
ax.set_title("VolComp AI+ PROP  —  The 5-Minute Scalp Setup (MNQ)", color=FG, fontsize=20, fontweight="bold", pad=14)
for s in ax.spines.values(): s.set_color("#33333a")
ax.tick_params(colors="#55555c"); ax.set_yticklabels([]); ax.set_xticklabels([])

# entry marker (pullback continuation long)
ei = 24
ax.scatter([ei],[lows[ei]-1.2], marker="^", s=420, color="#39ff8a", edgecolor="black", zorder=6)
ax.text(ei, lows[ei]-2.6, "A+ BUY", color="#39ff8a", fontsize=11, ha="center", fontweight="bold")

# annotations with arrows
callout(ax, (10, ema[10]), (3, highs.max()+2.5),
        "1) EMA-20 (orange) rising =\n    bullish trend. Trade LONGS only.", color=ORANGE)
callout(ax, (20, ema[20]), (26, lows.min()-1.5),
        "2) Price PULLS BACK to EMA-20.\n    This arms the entry (no chasing).", color="#9ad1ff", ha="left")
callout(ax, (ei, lows[ei]-1.2), (ei-12, lows.min()+1),
        "3) PROP row flips A+ BUY ^ as\n    price resumes up off the EMA =\n    ENTER LONG here.", color=CALL)
callout(ax, (34, highs[34]), (37, highs.max()+1.5),
        "4) Ride it. Manage with the\n    COACH / STATE rows.", color="#39ff8a")
callout(ax, (42, closes[42]), (40, lows.min()+2),
        "5) PROP -> SKIP or opposite\n    signal = take profit / exit.", color="#ff9a9a")

# chop zone illustration
ax.add_patch(Rectangle((0, highs.max()+0.2), 6.5, 3.2, fc=RED, alpha=0.12, zorder=0))
plt.tight_layout()
fig.savefig("manual_2_chart.png", dpi=140, facecolor=BG)
plt.close(fig)

# =====================================================================
# IMAGE 3 — SCALP PLAYBOOK / CHECKLIST
# =====================================================================
fig, ax = plt.subplots(figsize=(15.5, 9.6))
fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
ax.set_xlim(0,100); ax.set_ylim(0,100); ax.axis("off")
ax.text(50, 97, "MNQ 5-MINUTE SCALP PLAYBOOK", color=FG, fontsize=22, fontweight="bold", ha="center")
ax.text(50, 92.5, "Default prop confidence = 83%  (A+ = 88%)", color=CALL, fontsize=13, ha="center")

steps = [
    ("STEP 1  —  TREND", ORANGE,
     "Look at EMA-20 (orange).\nRising = longs only.  Falling = shorts only.\nEMA-200 = bigger-picture filter."),
    ("STEP 2  —  PULLBACK", "#9ad1ff",
     "Wait for price to pull back to / tap the EMA-20.\nThe EMA-proximity filter blocks chasing\nover-extended bars."),
    ("STEP 3  —  TRIGGER (PROP row)", CALL,
     "Enter ONLY when the PROP row turns:\n  green  A+/B+ BUY ^   -> long\n  red    A+/B+ SELL v   -> short\nGray SKIP = no trade."),
    ("STEP 4  —  CONFLUENCE", GREEN,
     "Confirm before clicking:\n  ACT % and DOM % both >= 83 same side\n  AI prob leaning your way\n  COACH not against you\n  filter tag B+V+E+H+ (avoid too many x)"),
    ("STEP 5  —  MANAGE / EXIT", RED,
     "Exit when:\n  PROP flips to opposite or SKIP\n  COACH gives opposite signal\n  STATE shows EXIT\nA+ = strongest, B+ = good, SKIP = wait."),
]
y=84
for title, col, body in steps:
    ax.add_patch(FancyBboxPatch((6, y-12.5), 88, 12, boxstyle="round,pad=0.3,rounding_size=1.4",
                                fc="#15151d", ec=col, lw=2))
    ax.text(9, y-2.2, title, color=col, fontsize=15, fontweight="bold", va="center")
    ax.text(9, y-8.2, body, color=FG, fontsize=11.5, va="center")
    if y>30:
        ax.add_patch(FancyArrowPatch((50, y-12.6), (50, y-14.6), arrowstyle="-|>",
                                     color=GRAY, lw=2.5, mutation_scale=22))
    y-=15.4

ax.text(50, 4, "Rule of thumb: no green/red PROP row = no trade. The indicator's job is to keep you OUT of bad scalps.",
        color=CALL, fontsize=12.5, ha="center", fontstyle="italic")
plt.tight_layout()
fig.savefig("manual_3_playbook.png", dpi=140, facecolor=BG)
plt.close(fig)

print("done")

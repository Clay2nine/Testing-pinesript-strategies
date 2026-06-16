#!/usr/bin/env python3
# Annotated lesson based on the user's full multi-indicator MNQ prop chart.
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch

BG="#0c0c10"; FG="#ececf0"; CALL="#ffd24d"; GRAY="#7d7d86"
RED="#e0413e"; GREEN="#15a06f"; BLUE="#2a6df4"; ORANGE="#ff9100"
TEAL="#13a89a"; PURP="#9b59b6"; PINK="#e84393"; MAROON="#8e1f3d"

def box(ax,x,y,w,h,fc,ec,lw=2,r=1.2,alpha=1.0):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle=f"round,pad=0.2,rounding_size={r}",
                fc=fc,ec=ec,lw=lw,alpha=alpha))

# =====================================================================
# IMAGE 1 — SCREEN MAP : "what is all this stuff?"
# =====================================================================
fig,ax=plt.subplots(figsize=(16,9)); fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
ax.set_xlim(0,100); ax.set_ylim(0,100); ax.axis("off")
ax.text(50,97,"YOUR MNQ PROP CHART  —  SCREEN MAP",color=FG,fontsize=22,fontweight="bold",ha="center")
ax.text(50,93,"5 functional zones. Learn what each zone DOES, then read them in order.",color=GRAY,fontsize=12.5,ha="center")

# chart frame
ax.add_patch(Rectangle((2,20),96,68,fc="#101016",ec="#33333a",lw=1.5))

# Zone boxes placed roughly where they appear on the real chart
zones=[
 (78,72,19,14,"1  MTF BIAS TABLE",BLUE,"Top-right grid: bias per timeframe\n(1/15/30/60/240/D) + Alignment %"),
 (80,22,17,48,"2  LEVEL RAIL",RED,"Right edge: NQSPROP Stop-Loss,\nTrigger, Entry, Take-Profit + SMA\n/ Trend lines = your price targets"),
 (4,23,20,22,"3  ORB DASHBOARD",TEAL,"Left: risk/trade, position size,\nVWAP, ATR, Signals-today,\nDAILY-LIMIT guardrail"),
 (27,48,48,38,"4  SIGNAL CLUSTER",ORANGE,"Center: ML/ICT bias, A+ scores,\nWATCH/READY/NEXT alerts,\ncandlestick patterns"),
 (55,22,23,12,"5  VOLCOMP PROP PANEL",GREEN,"Bottom-right: ACT / PROP / DOM\nvolume confirmation (your 83% gate)"),
]
for x,y,w,h,title,col,_ in zones:
    box(ax,x,y,w,h,"none",col,lw=2.6)
    ax.text(x+w/2,y+h-2.0,title.split("  ",1)[1] if "  " in title else title,color=col,
            fontsize=10.5,ha="center",va="top",fontweight="bold")
    ax.text(x+1.0,y+h-0.2,title.split()[0],color="black",fontsize=12,ha="left",va="top",
            fontweight="bold",bbox=dict(boxstyle="circle,pad=0.25",fc=col,ec="none"))

# legend strip
ax.text(4,15.5,"READING ORDER:",color=CALL,fontsize=13,fontweight="bold")
leg=[("1","MTF Bias = which way is the market leaning across timeframes?  (here: Bearish / Strong Sell)",BLUE),
     ("2","Level Rail = exact Entry / Stop / Target prices once you commit.",RED),
     ("4","Signal Cluster = the EDGE. ML+ICT+OB+pattern agreement and the A+ score.",ORANGE),
     ("5","VolComp Panel = volume must confirm (PROP turns green/red >= 83%).",GREEN),
     ("3","ORB Dashboard = am I ALLOWED to trade? (risk, size, daily limit).",TEAL)]
y=12.5
for n,txt,col in leg:
    ax.text(5,y,n,color="black",fontsize=10,ha="center",va="center",fontweight="bold",
            bbox=dict(boxstyle="circle,pad=0.22",fc=col,ec="none"))
    ax.text(8,y,txt,color=FG,fontsize=10.8,va="center")
    y-=2.4
plt.tight_layout(); fig.savefig("lesson_1_screenmap.png",dpi=140,facecolor=BG); plt.close(fig)

# =====================================================================
# IMAGE 2 — THE CONFLUENCE STACK (the actual decision funnel)
# =====================================================================
fig,ax=plt.subplots(figsize=(15.5,9.8)); fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
ax.set_xlim(0,100); ax.set_ylim(0,100); ax.axis("off")
ax.text(50,97,"THE CONFLUENCE STACK  —  read top to bottom",color=FG,fontsize=22,fontweight="bold",ha="center")
ax.text(50,92.8,"Every layer must AGREE before you take an A+ scalp. One red flag = stand down.",color=CALL,fontsize=12.5,ha="center")

layers=[
 ("FILTER 1  ·  DIRECTION (MTF Bias table)",BLUE,
  "All/most timeframes + Alignment point the SAME way.\nExample chart: 1m/15m Strong Sell, Alignment Bearish 43%  ->  SHORTS ONLY."),
 ("FILTER 2  ·  TREND ENGINE (ML / SMA / ICT bias)",PURP,
  "'MNQ ML PROP BIAS: SELL  (20 SMA below 200 SMA)' + BK ICT SELL BIAS + SCALP OB SELL\nall agree with Filter 1.  20<200 = bearish regime."),
 ("FILTER 3  ·  THE TRIGGER (PROP A+ / NQSPROP / VolComp)",CALL,
  "'PROP A+ ENTRY' fires AND VolComp PROP row turns red 'A+/B+ SELL v' >= 83%,\nwith NQSPROP Trigger crossed.  This is the GO line."),
 ("FILTER 4  ·  PRICE CONFIRMATION (candlestick + score)",ORANGE,
  "A reversal/continuation pattern in your favour at a level:\nBear PinBar / Engulfing / Long-Upper-Shadow + Score 90-100% / RVI SELL conf."),
 ("FILTER 5  ·  PERMISSION (ORB Dashboard)",TEAL,
  "Risk/Trade within $200, position size set, and DAILY-LIMIT not hit / not STAND-DOWN.\nIf the dashboard says stand down -> NO trade, even on A+."),
 ("EXECUTE  ·  use the LEVEL RAIL",GREEN,
  "Enter at PROP A+ ENTRY, Stop at NQSPROP Stop-Loss, Target NQSPROP Take-Profit.\nRisk shown on the entry box (e.g. Risk 34.5 pts)."),
]
y=86; h=11.5
for i,(title,col,body) in enumerate(layers):
    fc = "#1a1a12" if col==CALL else "#15151d"
    box(ax,8,y-h,84,h,fc,col,lw=2.4 if col!=CALL else 3.4)
    ax.text(11,y-2.4,title,color=col,fontsize=13.5,fontweight="bold",va="center")
    ax.text(11,y-7.3,body,color=FG,fontsize=10.8,va="center")
    if i<len(layers)-1:
        ax.add_patch(FancyArrowPatch((50,y-h-0.1),(50,y-h-1.7),arrowstyle="-|>",color=GRAY,lw=2.6,mutation_scale=20))
    y-=h+1.9
plt.tight_layout(); fig.savefig("lesson_2_stack.png",dpi=140,facecolor=BG); plt.close(fig)

# =====================================================================
# IMAGE 3 — SCALP PLAYBOOK + GUARDRAILS
# =====================================================================
fig,ax=plt.subplots(figsize=(15.5,9.8)); fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
ax.set_xlim(0,100); ax.set_ylim(0,100); ax.axis("off")
ax.text(50,97,"MNQ 5-MINUTE SCALP PLAYBOOK  (full stack)",color=FG,fontsize=21,fontweight="bold",ha="center")

# left column: the routine
ax.text(6,90,"THE ROUTINE (every bar close)",color=CALL,fontsize=14,fontweight="bold")
routine=[
 ("A","Check MTF Bias table -> pick side (long/short). No alignment = wait.",BLUE),
 ("B","Confirm ML/SMA/ICT bias agrees (20 vs 200 SMA regime).",PURP),
 ("C","Wait for PROP A+ / VolComp PROP row to fire your side >= 83%.",CALL),
 ("D","Need a candlestick confirm + score 90%+ at a level.",ORANGE),
 ("E","Dashboard green (risk ok, limit not hit) -> take it.",TEAL),
 ("F","Enter/Stop/Target straight off the NQSPROP level rail.",GREEN),
]
y=85
for n,txt,col in routine:
    ax.text(7,y,n,color="black",fontsize=11,ha="center",va="center",fontweight="bold",
            bbox=dict(boxstyle="circle,pad=0.3",fc=col,ec="none"))
    ax.text(10,y,txt,color=FG,fontsize=11,va="center")
    y-=6.0

# right column: guardrails
ax.text(54,90,"PROP GUARDRAILS (do NOT break)",color="#ff7a7a",fontsize=14,fontweight="bold")
box(ax,53,40,44,46,"#1a1113","#ff7a7a",lw=2.2)
rules=[
 "STAND DOWN / DAILY LIMIT HIT  ->  stop for the day.",
 "No green/red PROP row  ->  no trade (volume not there).",
 "Filters disagree (e.g. bias up but PROP sells)  ->  skip.",
 "Risk per trade fixed (~$200) — size from dashboard.",
 "A+ = full size,  B+ = reduced,  SKIP/WATCH = flat.",
 "Counter-trend signal = exit, don't 'hope'.",
 "Chasing far from 20 SMA = blocked by design — respect it.",
]
yy=82
for r in rules:
    ax.text(55.5,yy,"•",color="#ff7a7a",fontsize=14,va="center")
    ax.text(57.5,yy,r,color=FG,fontsize=10.8,va="center")
    yy-=6.0

# bottom takeaway + declutter tip
box(ax,6,8,88,18,"#101820","#13a89a",lw=2)
ax.text(50,22,"GRADES, SIMPLIFIED",color=TEAL,fontsize=13,fontweight="bold",ha="center")
ax.text(50,16.5,"ELITE A+ / A+  =  every layer aligned  ->  highest-conviction scalp (full plan).",color="#7CFC9A",fontsize=11.5,ha="center")
ax.text(50,12.5,"WATCH / NEXT / READY  =  setup forming, not yet valid  ->  prepare, don't fire.",color=CALL,fontsize=11.5,ha="center")
ax.text(50,9.2,"TIP: keep this busy layout for study, but trade from a 2nd clean chart: price + 20/200 SMA + VolComp PROP row + level rail.",
        color=GRAY,fontsize=10.5,ha="center",fontstyle="italic")
plt.tight_layout(); fig.savefig("lesson_3_playbook.png",dpi=140,facecolor=BG); plt.close(fig)
print("done")

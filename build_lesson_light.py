#!/usr/bin/env python3
# Light-theme lesson diagrams for the all-in-one downloadable lesson.
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch

BG="#eef0f3"; CARD="#ffffff"; INK="#1d2129"; SUB="#5b6470"
BLUE="#1857c4"; PURP="#7d3cab"; AMBER="#b07d00"; ORANGE="#d97a00"
TEAL="#0e8e82"; GREEN="#0c8f5f"; RED="#c0392b"; GRAY="#8a929e"; MAROON="#8e1f3d"

def rbox(ax,x,y,w,h,fc,ec,lw=2,r=1.2,ls="-"):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle=f"round,pad=0.2,rounding_size={r}",
                fc=fc,ec=ec,lw=lw,ls=ls))

# ---------------------------------------------------------------- 1 PANEL DECODER
fig,ax=plt.subplots(figsize=(15.5,9.2)); fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
ax.set_xlim(0,100); ax.set_ylim(0,100); ax.axis("off")
ax.text(50,97,"VolComp AI+ PROP  —  PANEL DECODER",color=INK,fontsize=22,fontweight="bold",ha="center")
ax.text(50,93,"Read top-to-bottom. The PROP row is your trade trigger.",color=SUB,fontsize=13,ha="center")
rows=[("ACT BUY ^ 56%   [AGG-AUTO:NAS] | PROP:BxV+E+H+",GREEN,"white"),
      ("PROP  A+ BUY ^  90%  (req 83 / A+ 88)",GREEN,"white"),
      ("DOM BUY ^ 67% | 3012.00",TEAL,"white"),
      ("AI prob (up) % 55.07",BLUE,"white"),
      ("COACH HOLD = 67% (-)","#e4c000","black"),
      ("STATE FLAT",GRAY,"white")]
px,pw=5,46; top=84; rh=9; gap=1.2; ys=[]
for i,(txt,bg,tc) in enumerate(rows):
    y=top-i*(rh+gap); ys.append(y)
    rbox(ax,px,y-rh/2,pw,rh,bg,"none")
    ax.text(px+2,y,txt,color=tc,fontsize=12.5,va="center",fontweight="bold")
cx=px+pw+3
notes=["ACT row = AGGRESSIVE volume.\n'^ 56%' = 56% of pushy volume is BUYING.\nPROP:B/V/E/H tag = filter status\n(+ pass, x fail): Body, Volatility, EMA, HTF.",
       "*** YOUR TRIGGER ROW ***\nGreen 'A+/B+ BUY ^' = go LONG.\nRed 'A+/B+ SELL v' = go SHORT.\nGray 'SKIP' = stand aside.\n'req 83/A+ 88' = volume % needed.",
       "DOM row = TOTAL volume direction.\n'^ 67%' = 67% of all volume is buy.\nNumber = raw volume of the bar.",
       "AI/ML bias 0-100. >62 bullish,\n<38 bearish (defaults). Confirms,\ndoes not trigger on its own.",
       "COACH = the wider signal engine\n(A/B stack). BUY / SELL / HOLD.\nUsed for exits & confluence.",
       "STATE machine: FLAT / IN-LONG /\nIN-SHORT / EXIT. Tracks the\nlive position the logic is holding."]
nc=[GREEN,AMBER,TEAL,BLUE,"#a98a00",GRAY]
for y,note,col in zip(ys,notes,nc):
    ax.annotate(note,xy=(px+pw,y),xytext=(cx,y),color=INK,fontsize=11,va="center",ha="left",
        arrowprops=dict(arrowstyle="-|>",color=col,lw=2.4),
        bbox=dict(boxstyle="round,pad=0.45",fc=CARD,ec=col,lw=1.6))
rbox(ax,px-0.8,ys[1]-rh/2-0.8,pw+1.6,rh+1.6,"none",AMBER,lw=3,ls="--")
ax.text(50,4,"MNQ 5-minute scalp: watch ACT + DOM agree, then act ONLY when the PROP row turns green/red.",
        color=AMBER,fontsize=12.5,ha="center",fontstyle="italic")
plt.tight_layout(); fig.savefig("lz_1_panel.png",dpi=140,facecolor=BG); plt.close(fig)

# ---------------------------------------------------------------- 2 SCREEN MAP
fig,ax=plt.subplots(figsize=(16,9)); fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
ax.set_xlim(0,100); ax.set_ylim(0,100); ax.axis("off")
ax.text(50,97,"YOUR MNQ PROP CHART  —  SCREEN MAP",color=INK,fontsize=22,fontweight="bold",ha="center")
ax.text(50,93,"5 functional zones. Learn what each zone DOES, then read them in order.",color=SUB,fontsize=12.5,ha="center")
ax.add_patch(Rectangle((2,20),96,68,fc="#f6f7f9",ec="#c9ced6",lw=1.5))
zones=[(78,72,19,14,"MTF BIAS TABLE","1",BLUE),
       (80,22,17,48,"LEVEL RAIL","2",RED),
       (4,23,20,22,"ORB DASHBOARD","3",TEAL),
       (27,48,48,38,"SIGNAL CLUSTER","4",ORANGE),
       (55,22,23,12,"VOLCOMP PROP PANEL","5",GREEN)]
for x,y,w,h,title,n,col in zones:
    rbox(ax,x,y,w,h,CARD,col,lw=2.6)
    ax.text(x+w/2,y+h-2.0,title,color=col,fontsize=10.5,ha="center",va="top",fontweight="bold")
    ax.text(x+1.0,y+h-0.2,n,color="white",fontsize=12,ha="left",va="top",fontweight="bold",
            bbox=dict(boxstyle="circle,pad=0.25",fc=col,ec="none"))
ax.text(4,15.5,"READING ORDER:",color=AMBER,fontsize=13,fontweight="bold")
leg=[("1","MTF Bias = which way is the market leaning across timeframes?  (here: Bearish / Strong Sell)",BLUE),
     ("2","Level Rail = exact Entry / Stop / Target prices once you commit.",RED),
     ("4","Signal Cluster = the EDGE. ML+ICT+OB+pattern agreement and the A+ score.",ORANGE),
     ("5","VolComp Panel = volume must confirm (PROP turns green/red >= 83%).",GREEN),
     ("3","ORB Dashboard = am I ALLOWED to trade? (risk, size, daily limit).",TEAL)]
y=12.5
for n,txt,col in leg:
    ax.text(5,y,n,color="white",fontsize=10,ha="center",va="center",fontweight="bold",
            bbox=dict(boxstyle="circle,pad=0.22",fc=col,ec="none"))
    ax.text(8,y,txt,color=INK,fontsize=10.8,va="center"); y-=2.4
plt.tight_layout(); fig.savefig("lz_2_screenmap.png",dpi=140,facecolor=BG); plt.close(fig)

# ---------------------------------------------------------------- 3 STACK
fig,ax=plt.subplots(figsize=(15.5,9.8)); fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
ax.set_xlim(0,100); ax.set_ylim(0,100); ax.axis("off")
ax.text(50,97,"THE CONFLUENCE STACK  —  read top to bottom",color=INK,fontsize=22,fontweight="bold",ha="center")
ax.text(50,92.8,"Every layer must AGREE before you take an A+ scalp. One red flag = stand down.",color=AMBER,fontsize=12.5,ha="center")
layers=[("FILTER 1  ·  DIRECTION (MTF Bias table)",BLUE,
  "All/most timeframes + Alignment point the SAME way.\nExample chart: 1m/15m Strong Sell, Alignment Bearish 43%  ->  SHORTS ONLY."),
 ("FILTER 2  ·  TREND ENGINE (ML / SMA / ICT bias)",PURP,
  "'MNQ ML PROP BIAS: SELL  (20 SMA below 200 SMA)' + BK ICT SELL BIAS + SCALP OB SELL\nall agree with Filter 1.  20<200 = bearish regime."),
 ("FILTER 3  ·  THE TRIGGER (PROP A+ / NQSPROP / VolComp)",AMBER,
  "'PROP A+ ENTRY' fires AND VolComp PROP row turns red 'A+/B+ SELL v' >= 83%,\nwith NQSPROP Trigger crossed.  This is the GO line."),
 ("FILTER 4  ·  PRICE CONFIRMATION (candlestick + score)",ORANGE,
  "A reversal/continuation pattern in your favour at a level:\nBear PinBar / Engulfing / Long-Upper-Shadow + Score 90-100% / RVI SELL conf."),
 ("FILTER 5  ·  PERMISSION (ORB Dashboard)",TEAL,
  "Risk/Trade within $200, position size set, and DAILY-LIMIT not hit / not STAND-DOWN.\nIf the dashboard says stand down -> NO trade, even on A+."),
 ("EXECUTE  ·  use the LEVEL RAIL",GREEN,
  "Enter at PROP A+ ENTRY, Stop at NQSPROP Stop-Loss, Target NQSPROP Take-Profit.\nRisk shown on the entry box (e.g. Risk 34.5 pts).")]
y=86; h=11.5
for i,(title,col,body) in enumerate(layers):
    fc="#fff8e6" if col==AMBER else CARD
    rbox(ax,8,y-h,84,h,fc,col,lw=3.4 if col==AMBER else 2.4)
    ax.text(11,y-2.4,title,color=col,fontsize=13.5,fontweight="bold",va="center")
    ax.text(11,y-7.3,body,color=INK,fontsize=10.8,va="center")
    if i<len(layers)-1:
        ax.add_patch(FancyArrowPatch((50,y-h-0.1),(50,y-h-1.7),arrowstyle="-|>",color=GRAY,lw=2.6,mutation_scale=20))
    y-=h+1.9
plt.tight_layout(); fig.savefig("lz_3_stack.png",dpi=140,facecolor=BG); plt.close(fig)

# ---------------------------------------------------------------- 4 PLAYBOOK
fig,ax=plt.subplots(figsize=(15.5,9.8)); fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
ax.set_xlim(0,100); ax.set_ylim(0,100); ax.axis("off")
ax.text(50,97,"MNQ 5-MINUTE SCALP PLAYBOOK  (full stack)",color=INK,fontsize=21,fontweight="bold",ha="center")
ax.text(6,90,"THE ROUTINE (every bar close)",color=AMBER,fontsize=14,fontweight="bold")
routine=[("A","Check MTF Bias table -> pick side (long/short). No alignment = wait.",BLUE),
 ("B","Confirm ML/SMA/ICT bias agrees (20 vs 200 SMA regime).",PURP),
 ("C","Wait for PROP A+ / VolComp PROP row to fire your side >= 83%.",AMBER),
 ("D","Need a candlestick confirm + score 90%+ at a level.",ORANGE),
 ("E","Dashboard green (risk ok, limit not hit) -> take it.",TEAL),
 ("F","Enter/Stop/Target straight off the NQSPROP level rail.",GREEN)]
y=85
for n,txt,col in routine:
    ax.text(7,y,n,color="white",fontsize=11,ha="center",va="center",fontweight="bold",
            bbox=dict(boxstyle="circle,pad=0.3",fc=col,ec="none"))
    ax.text(10,y,txt,color=INK,fontsize=11,va="center"); y-=6.0
ax.text(54,90,"PROP GUARDRAILS (do NOT break)",color=RED,fontsize=14,fontweight="bold")
rbox(ax,53,40,44,46,"#fdecea",RED,lw=2.2)
rules=["STAND DOWN / DAILY LIMIT HIT  ->  stop for the day.",
 "No green/red PROP row  ->  no trade (volume not there).",
 "Filters disagree (bias up but PROP sells)  ->  skip.",
 "Risk per trade fixed (~$200) — size from dashboard.",
 "A+ = full size,  B+ = reduced,  SKIP/WATCH = flat.",
 "Counter-trend signal = exit, don't 'hope'.",
 "Chasing far from 20 SMA = blocked by design — respect it."]
yy=82
for r in rules:
    ax.text(55.5,yy,"•",color=RED,fontsize=14,va="center")
    ax.text(57.5,yy,r,color=INK,fontsize=10.8,va="center"); yy-=6.0
rbox(ax,6,8,88,18,"#e9f7f1",TEAL,lw=2)
ax.text(50,22,"GRADES, SIMPLIFIED",color=TEAL,fontsize=13,fontweight="bold",ha="center")
ax.text(50,16.5,"ELITE A+ / A+  =  every layer aligned  ->  highest-conviction scalp (full plan).",color=GREEN,fontsize=11.5,ha="center")
ax.text(50,12.5,"WATCH / NEXT / READY  =  setup forming, not yet valid  ->  prepare, don't fire.",color=AMBER,fontsize=11.5,ha="center")
ax.text(50,9.2,"TIP: keep the busy layout for study, but trade from a 2nd clean chart: price + 20/200 SMA + VolComp PROP row + level rail.",
        color=SUB,fontsize=10.5,ha="center",fontstyle="italic")
plt.tight_layout(); fig.savefig("lz_4_playbook.png",dpi=140,facecolor=BG); plt.close(fig)
print("done")

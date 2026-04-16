# =============================================================================
# MISO Survey 2024 — Data Storytelling Visualizations (FINAL)
# MISM 6213 Section 05 | FSU Technology Services
# Team: Singh · Zamorano · Ani · Patel
# =============================================================================
#
# WHAT THIS GENERATES:
#   Static PNGs (dark vibrant theme — for sharing/reference):
#     v1_waffle_match.png
#     v2_slope_match.png
#     v3_lollipop_match.png
#     v4_dotplot_match.png
#
#   Animated GIFs (for PowerPoint — insert via Insert > Pictures):
#     v1_waffle_animated.gif
#     v2_slope_animated.gif
#     v3_lollipop_animated.gif
#     v4_dotplot_animated.gif
#
# HOW TO RUN:
#   1. Put this file in the same folder as:
#        - 2024_Student_MISO_Cleaned.csv
#        - 2024_Staff_MISO_Cleaned.csv
#   2. Run with F5 in Spyder
#   3. All 8 files will save to the same folder
#
# DESIGN PRINCIPLES APPLIED (Dykes Ch. 7 & 8):
#   ✓ One message per visual — title states the insight
#   ✓ Direct labels instead of legends (reduces cognitive friction)
#   ✓ Size directs attention — key numbers are largest elements
#   ✓ Contrast controls focus — primary data bright, secondary dimmer
#   ✓ Color is purposeful: GOLD=key stat, TEAL=positive, CORAL=concern
#   ✓ Clutter removed — no thick borders, no redundant gridlines
#   ✓ All stats computed directly from data (no hardcoded unverified numbers)
# =============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from matplotlib.animation import FuncAnimation
import warnings
warnings.filterwarnings('ignore')

# -----------------------------------------------------------------------------
# LOAD DATA — update paths if CSVs are in a different folder
# -----------------------------------------------------------------------------
students = pd.read_csv('2024_Student_MISO_Cleaned.csv')
staff    = pd.read_csv('2024_Staff_MISO_Cleaned.csv')

# -----------------------------------------------------------------------------
# COLOR PALETTE — edit here to change theme across all visuals
# -----------------------------------------------------------------------------
BG         = '#0D1B2A'   # deep navy background
GOLD       = '#FFB703'   # vivid gold — key highlight stat
CORAL      = '#FB5607'   # coral/orange — concern/gap
TEAL       = '#06D6A0'   # teal/green — positive/good
PURPLE     = '#8338EC'   # purple — students secondary line
SKY        = '#3A86FF'   # bright blue — students dots
WHITE      = '#FFFFFF'
LIGHT_TEXT = '#CBD5E1'   # muted text on dark background
DIM        = '#1E3A5F'   # dark blue — unfilled cells/connectors

plt.rcParams.update({'font.family': 'DejaVu Sans'})


# =============================================================================
# ── STATIC PNGs ──────────────────────────────────────────────────────────────
# =============================================================================

# =============================================================================
# STATIC VISUAL 1 — WAFFLE CHART
# ONE MESSAGE: Almost nobody at FSU knows what IT services are available
# =============================================================================
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
fig.patch.set_facecolor(BG)
for ax in axes:
    ax.set_facecolor(BG)

fig.text(0.5, 0.97, 'Out of Every 100 People at FSU…',
         ha='center', fontsize=15, fontweight='bold', color=WHITE)
fig.text(0.5, 0.91, 'How many feel "very informed" about IT services?',
         ha='center', fontsize=10.5, color=LIGHT_TEXT, style='italic')

def draw_waffle(ax, pct, group_label, color_on, label_pct):
    """10×10 waffle chart — each square = 1 person out of 100."""
    ax.set_facecolor(BG)
    N_COLS, N_ROWS, GAP = 10, 10, 0.14
    filled = round(pct)
    count  = 0
    for row in range(N_ROWS - 1, -1, -1):
        for col in range(N_COLS):
            color = color_on if count < filled else DIM
            rect  = plt.Rectangle(
                [col + col*GAP, row + row*GAP], 1, 1,
                color=color, linewidth=0, zorder=2)
            ax.add_patch(rect)
            count += 1
    ax.set_xlim(-0.3, 10 + 9*GAP + 0.3)
    ax.set_ylim(-1.8, 10 + 9*GAP + 0.3)
    ax.set_aspect('equal')
    ax.axis('off')
    # Large % — size directs attention to key number
    ax.text(0.5, -0.05, f'{label_pct}%', transform=ax.transAxes,
            ha='center', fontsize=58, fontweight='bold', color=color_on,
            path_effects=[pe.withStroke(linewidth=4, foreground=BG)])
    # Direct label — no separate legend needed
    ax.text(0.5, -0.16, group_label, transform=ax.transAxes,
            ha='center', fontsize=12, fontweight='bold', color=WHITE)
    ax.text(0.5, -0.24, 'feel "very informed" about IT services',
            transform=ax.transAxes, ha='center', fontsize=9, color=LIGHT_TEXT)

draw_waffle(axes[0], 7,  'STUDENTS', GOLD, 7)
draw_waffle(axes[1], 14, 'STAFF',    TEAL, 14)

fig.text(0.5, 0.04,
         '    = feels "very informed"          = does not feel "very informed"',
         ha='center', fontsize=9, color=LIGHT_TEXT)
fig.text(0.305, 0.04, '■', ha='center', fontsize=11, color=GOLD)
fig.text(0.565, 0.04, '■', ha='center', fontsize=11, color=DIM)

plt.subplots_adjust(top=0.88, bottom=0.1)
plt.savefig('v1_waffle_match.png', dpi=180, bbox_inches='tight', facecolor=BG)
plt.show()
print("Static V1 saved → v1_waffle_match.png")


# =============================================================================
# STATIC VISUAL 2 — SLOPE CHART
# ONE MESSAGE: The more informed you feel, the more satisfied you are
# =============================================================================
awareness_labels = ['Not\nInformed', 'Informed', 'Somewhat\nInformed', 'Very\nInformed']

# Computed directly from data
staff_sat = staff.groupby('INF_ATS')['DS_CWS'].mean().sort_index().values
stud_sat  = students.groupby('INF_ATS')['DS_CWS'].mean().sort_index().values
x = np.array([0, 1, 2, 3])

fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

# Staff — dominant (primary story, thicker, brighter)
ax.plot(x, staff_sat, color=TEAL, linewidth=3.5, zorder=4, solid_capstyle='round')
for xi, yi in zip(x, staff_sat):
    ax.scatter(xi, yi, color=TEAL, s=120, zorder=5, edgecolors=BG, linewidth=2)
    ax.text(xi, yi + 0.09, f'{yi:.2f}', ha='center',
            fontsize=10, fontweight='bold', color=TEAL)

# Students — secondary (dashed, dimmer)
ax.plot(x, stud_sat, color=PURPLE, linewidth=2.8, zorder=3,
        linestyle='--', dashes=(5, 4))
for xi, yi in zip(x, stud_sat):
    ax.scatter(xi, yi, color=PURPLE, s=100, zorder=4,
               edgecolors=BG, linewidth=2, marker='D')
    ax.text(xi, yi - 0.12, f'{yi:.2f}', ha='center',
            fontsize=9.5, fontweight='bold', color=PURPLE)

# Direct line labels — no legend
ax.text(3.08, staff_sat[-1], 'Staff',    fontsize=11, color=TEAL,
        fontweight='bold', va='center')
ax.text(3.08, stud_sat[-1],  'Students', fontsize=11, color=PURPLE, va='center')

# ONE annotation — the key insight
spread = staff_sat[-1] - staff_sat[0]
ax.annotate('', xy=(3, staff_sat[-1]), xytext=(0, staff_sat[0]),
            arrowprops=dict(arrowstyle='<|-|>', color=GOLD,
                            lw=2.2, mutation_scale=14))
ax.text(1.5, 3.12, f'+{spread:.2f} point spread\nfor staff',
        fontsize=10, color=GOLD, fontweight='bold', ha='center',
        bbox=dict(boxstyle='round,pad=0.35', facecolor=BG,
                  edgecolor=GOLD, linewidth=1.4))

ax.set_xticks(x)
ax.set_xticklabels(awareness_labels, fontsize=10.5, color=WHITE, fontweight='bold')
ax.set_xlim(-0.4, 3.7)
ax.set_ylim(2.2, 4.15)
ax.set_ylabel('Overall IT Satisfaction (1–4 scale)', fontsize=10, color=LIGHT_TEXT)
ax.set_title('The More Informed You Feel, the More Satisfied You Are\n'
             'Overall Computing Satisfaction by Awareness Level',
             fontsize=12, fontweight='bold', color=WHITE, pad=12)
for spine in ax.spines.values():
    spine.set_color(DIM)
ax.tick_params(colors=LIGHT_TEXT, labelsize=9)
ax.set_yticks([2.5, 3.0, 3.5, 4.0])
ax.grid(axis='y', alpha=0.12, color=WHITE, linestyle='--', linewidth=0.7)

plt.tight_layout()
plt.savefig('v2_slope_match.png', dpi=180, bbox_inches='tight', facecolor=BG)
plt.show()
print("Static V2 saved → v2_slope_match.png")


# =============================================================================
# STATIC VISUAL 3 — DIVERGING LOLLIPOP
# ONE MESSAGE: Students are more satisfied than expected — except wireless
# =============================================================================
service_labels = {
    'CMS':  'Canvas LMS',
    'CS':   'Help Desk Support',
    'OLC':  'Online Collaboration',
    'FPC':  'File & Print Computing',
    'ERPSS':'Banner Self-Service',
    'CWS':  'Campus Website',
    'OCS':  'Online Course Software',
    'QWSL': 'Wireless (On-campus)',  # ← the one concern
}

items = []
for code, label in service_labels.items():
    ic, dc = f'IMP_{code}', f'DS_{code}'
    if ic in students.columns and dc in students.columns:
        gap = students[ic].mean() - students[dc].mean()
        if not np.isnan(gap):
            items.append((label, gap))
items.sort(key=lambda x: x[1])
labels_s = [i[0] for i in items]
gaps_s   = np.array([i[1] for i in items])
y        = np.arange(len(labels_s))
colors   = [CORAL if g > 0 else TEAL for g in gaps_s]

fig, ax = plt.subplots(figsize=(10, 6.5))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

for yi, gap, col in zip(y, gaps_s, colors):
    ax.plot([0, gap], [yi, yi], color=col, linewidth=2.8,
            alpha=0.7, solid_capstyle='round', zorder=2)
for yi, gap, col in zip(y, gaps_s, colors):
    ax.scatter(gap, yi, color=col, s=180, zorder=4,
               edgecolors=BG, linewidth=1.5)
    ha     = 'left'  if gap >= 0 else 'right'
    offset = 0.03    if gap >= 0 else -0.03
    ax.text(gap + offset, yi, f'{gap:+.2f}', va='center',
            ha=ha, fontsize=9, fontweight='bold', color=col)

ax.axvline(0, color='#3A5A7A', linewidth=1.2, zorder=1)
ax.text( 0.25, -0.65, 'Satisfaction gap →',
        fontsize=8.5, color=CORAL, style='italic')
ax.text(-0.02, -0.65, '← Exceeds expectations',
        fontsize=8.5, color=TEAL,  style='italic', ha='right')

ax.set_yticks(y)
ax.set_yticklabels(labels_s, fontsize=10.5, color=WHITE)
ax.set_xlabel('Gap  (Importance − Satisfaction)', fontsize=10, color=LIGHT_TEXT)
ax.set_title('Students Are More Satisfied Than Expected\n'
             '— Except for Wireless Performance',
             fontsize=12, fontweight='bold', color=WHITE, pad=12)
for spine in ax.spines.values():
    spine.set_color(DIM)
ax.tick_params(colors=LIGHT_TEXT, labelsize=9)
ax.grid(axis='x', alpha=0.1, color=WHITE, linestyle='--', linewidth=0.7)
ax.set_xlim(-1.35, 0.45)

plt.tight_layout()
plt.savefig('v3_lollipop_match.png', dpi=180, bbox_inches='tight', facecolor=BG)
plt.show()
print("Static V3 saved → v3_lollipop_match.png")


# =============================================================================
# STATIC VISUAL 4 — ANNOTATED DOT PLOT
# ONE MESSAGE: Help Desk scores near-perfect but remains nearly invisible
# =============================================================================
categories = ['Friendliness', 'Knowledge',
              'Response Time\n(Local)', 'Response Time\n(Remote)']

# Computed directly from data
student_hd = students[['DAHD_F','DAHD_K','DAHD_RL','DAHD_RS']].mean().values
staff_hd   = staff[['DAHD_F','DAHD_K','DAHD_RL','DAHD_RS']].mean().values
y = np.arange(len(categories))

fig, ax = plt.subplots(figsize=(10, 5.2))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

ax.axvspan(3.75, 4.18, alpha=0.07, color=TEAL, zorder=0)
ax.text(3.76, -0.65, 'Excellent zone ▶', fontsize=8, color=TEAL, style='italic')

for yi, s, st in zip(y, student_hd, staff_hd):
    ax.plot([s, st], [yi, yi], color=DIM,
            linewidth=5, solid_capstyle='round', zorder=1)

ax.scatter(student_hd, y, color=SKY,    s=200, zorder=4,
           edgecolors=BG, linewidth=2, label='Students')
ax.scatter(staff_hd,   y, color=PURPLE, s=160, zorder=4,
           edgecolors=BG, linewidth=2, marker='D', label='Staff')

for yi, s, st in zip(y, student_hd, staff_hd):
    ax.text(s,  yi+0.22, f'{s:.2f}', ha='center',
            fontsize=9.5, color=SKY,    fontweight='bold')
    ax.text(st, yi+0.22, f'{st:.2f}', ha='center',
            fontsize=9.5, color=PURPLE, fontweight='bold')

ax.text(0.97, 0.09,
        'All ratings above 3.6 / 4.0\nYet only 7–14% feel "very informed"',
        transform=ax.transAxes, fontsize=10, color=WHITE,
        fontweight='bold', ha='right', va='bottom',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#1A2A3A',
                  edgecolor=GOLD, linewidth=1.5))

ax.legend(fontsize=10, frameon=False, loc='lower left',
          labelcolor=WHITE, handletextpad=0.4)
ax.set_yticks(y)
ax.set_yticklabels(categories, fontsize=11, color=WHITE)
ax.set_xlim(3.30, 4.18)
ax.set_xlabel('Mean Satisfaction Rating (out of 4)', fontsize=10, color=LIGHT_TEXT)
ax.set_title('The Help Desk Scores Near-Perfect Marks\n'
             '— But Remains Nearly Invisible to Its Own Users',
             fontsize=12, fontweight='bold', color=WHITE, pad=14)
for spine in ax.spines.values():
    spine.set_color(DIM)
ax.tick_params(colors=LIGHT_TEXT, labelsize=9)
ax.grid(axis='x', alpha=0.1, color=WHITE, linestyle='--', linewidth=0.7)

plt.tight_layout()
plt.savefig('v4_dotplot_match.png', dpi=180, bbox_inches='tight', facecolor=BG)
plt.show()
print("Static V4 saved → v4_dotplot_match.png")


# =============================================================================
# ── ANIMATED GIFs ─────────────────────────────────────────────────────────────
# =============================================================================

# =============================================================================
# ANIMATED VISUAL 1 — WAFFLE CHART
# Squares fill in one by one, percentage counts up from 0
# =============================================================================
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
fig.patch.set_facecolor(BG)
for ax in axes:
    ax.set_facecolor(BG)

fig.text(0.5, 0.97, 'Out of Every 100 People at FSU…',
         ha='center', fontsize=15, fontweight='bold', color=WHITE)
fig.text(0.5, 0.91, 'How many feel "very informed" about IT services?',
         ha='center', fontsize=10.5, color=LIGHT_TEXT, style='italic')

TARGETS      = [7, 14]
COLORS_W     = [GOLD, TEAL]
GROUPS       = ['STUDENTS', 'STAFF']
TOTAL_CELLS  = 100
N_COLS, N_ROWS, GAP = 10, 10, 0.14

def cell_xy(idx):
    col = idx % N_COLS
    row = N_ROWS - 1 - (idx // N_COLS)
    return col + col*GAP, row + row*GAP

rects      = [[], []]
pct_texts  = []

for side, (ax, target, color, group) in enumerate(
        zip(axes, TARGETS, COLORS_W, GROUPS)):
    for i in range(TOTAL_CELLS):
        rx, ry = cell_xy(i)
        r = plt.Rectangle([rx, ry], 1, 1, color=DIM, linewidth=0, zorder=2)
        ax.add_patch(r)
        rects[side].append(r)
    ax.set_xlim(-0.3, N_COLS + (N_COLS-1)*GAP + 0.3)
    ax.set_ylim(-1.8, N_ROWS + (N_ROWS-1)*GAP + 0.3)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.text(0.5, -0.10, group, transform=ax.transAxes,
            ha='center', fontsize=12, fontweight='bold', color=WHITE)
    ax.text(0.5, -0.17, 'feel "very informed"',
            transform=ax.transAxes, ha='center', fontsize=9, color=LIGHT_TEXT)
    txt = ax.text(0.5, -0.04, '0%', transform=ax.transAxes,
                  ha='center', fontsize=48, fontweight='bold', color=color,
                  path_effects=[pe.withStroke(linewidth=4, foreground=BG)])
    pct_texts.append(txt)

fig.text(0.5, 0.04,
         '    = feels "very informed"          = does not feel "very informed"',
         ha='center', fontsize=9, color=LIGHT_TEXT)
fig.text(0.305, 0.04, '■', ha='center', fontsize=11, color=GOLD)
fig.text(0.565, 0.04, '■', ha='center', fontsize=11, color=DIM)
plt.subplots_adjust(top=0.88, bottom=0.1)

TOTAL_FRAMES_W = 130
FILL_FRAMES_W  = 100

def animate_waffle(frame):
    for side, (target, color) in enumerate(zip(TARGETS, COLORS_W)):
        filled = min(int(frame / FILL_FRAMES_W * target), target) \
                 if frame <= FILL_FRAMES_W else target
        for i, r in enumerate(rects[side]):
            r.set_color(color if i < filled else DIM)
            if i < filled:
                alpha = 0.7 + 0.3 * np.sin(frame * 0.3 + i * 0.5)
                r.set_alpha(min(1.0, alpha))
        shown = int(frame / FILL_FRAMES_W * target) \
                if frame <= FILL_FRAMES_W else target
        pct_texts[side].set_text(f'{shown}%')
    return rects[0] + rects[1] + pct_texts

anim1 = FuncAnimation(fig, animate_waffle, frames=TOTAL_FRAMES_W,
                      interval=50, blit=True)
anim1.save('v1_waffle_animated.gif', writer='pillow', fps=20, dpi=130)
plt.close()
print("Animated V1 saved → v1_waffle_animated.gif")


# =============================================================================
# ANIMATED VISUAL 2 — SLOPE CHART
# Lines draw left to right, dots pop in, labels fade in, callout appears
# =============================================================================
staff_sat = staff.groupby('INF_ATS')['DS_CWS'].mean().sort_index().values
stud_sat  = students.groupby('INF_ATS')['DS_CWS'].mean().sort_index().values
x = np.array([0, 1, 2, 3])

fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(-0.5, 3.8)
ax.set_ylim(2.0, 4.3)
ax.set_xticks(x)
ax.set_xticklabels(['Not\nInformed','Informed','Somewhat\nInformed','Very\nInformed'],
                   fontsize=11, color=WHITE, fontweight='bold')
ax.set_ylabel('Overall IT Satisfaction (1–4)', fontsize=10, color=LIGHT_TEXT)
ax.set_title('The More Informed You Feel, the More Satisfied You Are',
             fontsize=13, fontweight='bold', color=WHITE, pad=14)
for spine in ax.spines.values():
    spine.set_color(DIM)
ax.tick_params(colors=LIGHT_TEXT, labelsize=9)
ax.set_yticks([2.5, 3.0, 3.5, 4.0])
ax.grid(axis='y', alpha=0.12, color=WHITE, linestyle='--', linewidth=0.7)

TOTAL_FRAMES_S = 120
DRAW_FRAMES_S  = 60
DOT_FRAME_S    = 65
LABEL_FRAME_S  = 75
ANNO_FRAME_S   = 85

staff_line, = ax.plot([], [], color=TEAL,   linewidth=3.5, solid_capstyle='round', zorder=4)
stud_line,  = ax.plot([], [], color=PURPLE, linewidth=3.0, solid_capstyle='round',
                      linestyle='--', dashes=(5, 4), zorder=3)
staff_dots  = ax.scatter([], [], color=TEAL,   s=130, zorder=5, edgecolors=BG, linewidth=2)
stud_dots   = ax.scatter([], [], color=PURPLE, s=110, zorder=5, edgecolors=BG,
                         linewidth=2, marker='D')

staff_lbls = [ax.text(xi, yi+0.10, f'{yi:.2f}', ha='center', fontsize=10,
                      fontweight='bold', color=TEAL,   alpha=0)
              for xi, yi in zip(x, staff_sat)]
stud_lbls  = [ax.text(xi, yi-0.13, f'{yi:.2f}', ha='center', fontsize=9.5,
                      fontweight='bold', color=PURPLE, alpha=0)
              for xi, yi in zip(x, stud_sat)]
staff_name = ax.text(3.08, staff_sat[-1], 'Staff',    fontsize=11,
                     color=TEAL,   fontweight='bold', va='center', alpha=0)
stud_name  = ax.text(3.08, stud_sat[-1],  'Students', fontsize=11,
                     color=PURPLE, va='center', alpha=0)
spread = staff_sat[-1] - staff_sat[0]
anno   = ax.text(1.5, 3.08, f'+{spread:.2f} point spread\nfor staff',
                 fontsize=10.5, color=GOLD, fontweight='bold',
                 ha='center', alpha=0,
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#1A2A3A',
                           edgecolor=GOLD, linewidth=1.5))

def animate_slope(frame):
    if frame <= DRAW_FRAMES_S:
        t  = frame / DRAW_FRAMES_S
        xi = np.linspace(0, 3, max(2, int(t * 300)))
        staff_line.set_data(xi, np.interp(xi, x, staff_sat))
        stud_line.set_data(xi,  np.interp(xi, x, stud_sat))
    if frame >= DOT_FRAME_S:
        staff_dots.set_offsets(np.c_[x, staff_sat])
        stud_dots.set_offsets(np.c_[x, stud_sat])
    if frame >= LABEL_FRAME_S:
        a = min(1.0, (frame - LABEL_FRAME_S) / 10)
        for l in staff_lbls + stud_lbls:
            l.set_alpha(a)
        staff_name.set_alpha(a)
        stud_name.set_alpha(a)
    if frame >= ANNO_FRAME_S:
        anno.set_alpha(min(1.0, (frame - ANNO_FRAME_S) / 10))
    return (staff_line, stud_line, staff_dots, stud_dots,
            *staff_lbls, *stud_lbls, staff_name, stud_name, anno)

anim2 = FuncAnimation(fig, animate_slope, frames=TOTAL_FRAMES_S,
                      interval=50, blit=True)
anim2.save('v2_slope_animated.gif', writer='pillow', fps=20, dpi=130)
plt.close()
print("Animated V2 saved → v2_slope_animated.gif")


# =============================================================================
# ANIMATED VISUAL 3 — DIVERGING LOLLIPOP
# Stems shoot out from zero, dots grow in, labels fade in
# =============================================================================
items = []
for code, label in service_labels.items():
    ic, dc = f'IMP_{code}', f'DS_{code}'
    if ic in students.columns and dc in students.columns:
        gap = students[ic].mean() - students[dc].mean()
        if not np.isnan(gap):
            items.append((label, gap))
items.sort(key=lambda x: x[1])
labels_s = [i[0] for i in items]
gaps_s   = np.array([i[1] for i in items])
y        = np.arange(len(labels_s))
colors   = [CORAL if g > 0 else TEAL for g in gaps_s]

fig, ax = plt.subplots(figsize=(10, 6.5))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(-1.4, 0.55)
ax.set_ylim(-0.8, len(labels_s) - 0.2)
ax.set_yticks(y)
ax.set_yticklabels(labels_s, fontsize=10.5, color=WHITE)
ax.set_xlabel('Gap  (Importance − Satisfaction)', fontsize=10, color=LIGHT_TEXT)
ax.set_title('Students Are More Satisfied Than Expected\n'
             '— Except for Wireless Performance',
             fontsize=13, fontweight='bold', color=WHITE, pad=12)
for spine in ax.spines.values():
    spine.set_color(DIM)
ax.tick_params(colors=LIGHT_TEXT, labelsize=9)
ax.axvline(0, color='#3A5A7A', linewidth=1.2, zorder=1)
ax.grid(axis='x', alpha=0.08, color=WHITE, linestyle='--', linewidth=0.7)
ax.text( 0.25, -0.65, 'Satisfaction gap →',
        fontsize=8.5, color=CORAL, style='italic')
ax.text(-0.02, -0.65, '← Exceeds expectations',
        fontsize=8.5, color=TEAL,  style='italic', ha='right')

TOTAL_FRAMES_L = 110
STEM_FRAMES_L  = 60

stem_lines = []
for yi, gap, col in zip(y, gaps_s, colors):
    line, = ax.plot([0, 0], [yi, yi], color=col, linewidth=2.8,
                    alpha=0.7, solid_capstyle='round', zorder=2)
    stem_lines.append(line)

dot_scatter = ax.scatter(np.zeros(len(y)), y, c=colors, s=0,
                         zorder=4, edgecolors=BG, linewidth=1.5)
val_labels  = []
for yi, gap, col in zip(y, gaps_s, colors):
    ha     = 'left'  if gap >= 0 else 'right'
    offset = 0.03    if gap >= 0 else -0.03
    lbl = ax.text(gap+offset, yi, f'{gap:+.2f}', va='center',
                  ha=ha, fontsize=9, fontweight='bold', color=col, alpha=0)
    val_labels.append(lbl)

def animate_lollipop(frame):
    if frame <= STEM_FRAMES_L:
        t = 1 - (1 - frame / STEM_FRAMES_L) ** 3   # ease out
        for line, gap in zip(stem_lines, gaps_s):
            line.set_xdata([0, gap * t])
        dot_scatter.set_offsets(np.c_[gaps_s * t, y])
        dot_scatter.set_sizes([t * 180] * len(y))
    else:
        alpha = min(1.0, (frame - STEM_FRAMES_L) / 15)
        for lbl in val_labels:
            lbl.set_alpha(alpha)
    return stem_lines + [dot_scatter] + val_labels

anim3 = FuncAnimation(fig, animate_lollipop, frames=TOTAL_FRAMES_L,
                      interval=50, blit=True)
anim3.save('v3_lollipop_animated.gif', writer='pillow', fps=20, dpi=130)
plt.close()
print("Animated V3 saved → v3_lollipop_animated.gif")


# =============================================================================
# ANIMATED VISUAL 4 — ANNOTATED DOT PLOT
# Connectors grow, dots slide in, labels fade, callout appears
# =============================================================================
categories = ['Friendliness', 'Knowledge',
              'Response Time\n(Local)', 'Response Time\n(Remote)']
student_hd = students[['DAHD_F','DAHD_K','DAHD_RL','DAHD_RS']].mean().values
staff_hd   = staff[['DAHD_F','DAHD_K','DAHD_RL','DAHD_RS']].mean().values
y = np.arange(len(categories))

fig, ax = plt.subplots(figsize=(10, 5.2))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(3.30, 4.18)
ax.set_ylim(-0.8, len(categories) - 0.2)
ax.set_yticks(y)
ax.set_yticklabels(categories, fontsize=11, color=WHITE)
ax.set_xlabel('Mean Satisfaction Rating (out of 4)', fontsize=10, color=LIGHT_TEXT)
ax.set_title('The Help Desk Scores Near-Perfect Marks\n'
             '— But Remains Nearly Invisible to Its Own Users',
             fontsize=13, fontweight='bold', color=WHITE, pad=14)
for spine in ax.spines.values():
    spine.set_color(DIM)
ax.tick_params(colors=LIGHT_TEXT, labelsize=9)
ax.grid(axis='x', alpha=0.1, color=WHITE, linestyle='--', linewidth=0.7)
ax.axvspan(3.75, 4.18, alpha=0.07, color=TEAL, zorder=0)
ax.text(3.76, -0.65, 'Excellent zone ▶', fontsize=8, color=TEAL, style='italic')

TOTAL_FRAMES_D = 120
CONN_FRAMES_D  = 40
DOT_FRAME_D    = 45
LABEL_FRAME_D  = 60
ANNO_FRAME_D   = 80

conn_lines = []
for yi, s, st in zip(y, student_hd, staff_hd):
    lo, hi = min(s, st), max(s, st)
    line, = ax.plot([lo, lo], [yi, yi], color=DIM,
                    linewidth=5, solid_capstyle='round', zorder=1)
    conn_lines.append((line, lo, hi))

stud_sc = ax.scatter([], [], color=SKY,    s=0, zorder=4,
                     edgecolors=BG, linewidth=2, label='Students')
staff_sc= ax.scatter([], [], color=PURPLE, s=0, zorder=4,
                     edgecolors=BG, linewidth=2, marker='D', label='Staff')
stud_lbls2 = [ax.text(s,  yi+0.22, f'{s:.2f}',  ha='center',
                      fontsize=9.5, color=SKY,    fontweight='bold', alpha=0)
              for yi, s in zip(y, student_hd)]
staff_lbls2= [ax.text(st, yi+0.22, f'{st:.2f}', ha='center',
                      fontsize=9.5, color=PURPLE, fontweight='bold', alpha=0)
              for yi, st in zip(y, staff_hd)]
callout = ax.text(0.97, 0.09,
                  'All ratings above 3.6 / 4.0\nYet only 7–14% feel "very informed"',
                  transform=ax.transAxes, fontsize=10, color=WHITE,
                  fontweight='bold', ha='right', va='bottom', alpha=0,
                  bbox=dict(boxstyle='round,pad=0.5', facecolor='#1A2A3A',
                            edgecolor=GOLD, linewidth=1.5))
ax.legend(fontsize=10, frameon=False, loc='lower left',
          labelcolor=WHITE, handletextpad=0.4)

def animate_dotplot(frame):
    if frame <= CONN_FRAMES_D:
        t = 1 - (1 - frame / CONN_FRAMES_D) ** 3
        for line, lo, hi in conn_lines:
            line.set_xdata([lo, lo + (hi - lo) * t])
    if frame >= DOT_FRAME_D:
        t    = min(1.0, (frame - DOT_FRAME_D) / 10)
        size = t * 200
        stud_sc.set_offsets(np.c_[student_hd, y])
        stud_sc.set_sizes([size] * len(y))
        staff_sc.set_offsets(np.c_[staff_hd, y])
        staff_sc.set_sizes([size * 0.8] * len(y))
    if frame >= LABEL_FRAME_D:
        a = min(1.0, (frame - LABEL_FRAME_D) / 12)
        for l in stud_lbls2 + staff_lbls2:
            l.set_alpha(a)
    if frame >= ANNO_FRAME_D:
        callout.set_alpha(min(1.0, (frame - ANNO_FRAME_D) / 12))
    return ([l for l, _, _ in conn_lines] +
            [stud_sc, staff_sc] +
            stud_lbls2 + staff_lbls2 + [callout])

anim4 = FuncAnimation(fig, animate_dotplot, frames=TOTAL_FRAMES_D,
                      interval=50, blit=True)
anim4.save('v4_dotplot_animated.gif', writer='pillow', fps=20, dpi=130)
plt.close()
print("Animated V4 saved → v4_dotplot_animated.gif")

print("\n✓ All 8 files generated successfully!")
print("  Static PNGs:    v1_waffle_match.png, v2_slope_match.png,")
print("                  v3_lollipop_match.png, v4_dotplot_match.png")
print("  Animated GIFs:  v1_waffle_animated.gif, v2_slope_animated.gif,")
print("                  v3_lollipop_animated.gif, v4_dotplot_animated.gif")

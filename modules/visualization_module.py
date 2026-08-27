"""
===================================================================
MODULE 8: VISUALIZATION - Charts & Insights using Matplotlib
===================================================================
Role: Generate stunning, dark-themed analytical charts.
Tech: matplotlib, numpy
===================================================================
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import numpy as np
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import RESULTS_DIR

# ─── PREMIUM DARK THEME ───
DARK_BG = '#0f0f1a'
CARD_BG = '#1a1a2e'
TEXT_COLOR = '#e0e0e0'
ACCENT_1 = '#00d4ff'  # Cyan
ACCENT_2 = '#7c3aed'  # Purple
ACCENT_3 = '#10b981'  # Emerald
ACCENT_4 = '#f59e0b'  # Amber
ACCENT_5 = '#ef4444'  # Red
ACCENT_6 = '#ec4899'  # Pink
GRADIENT_COLORS = ['#00d4ff', '#7c3aed', '#ec4899', '#f59e0b', '#10b981']


def apply_dark_style():
    """Apply premium dark theme to all matplotlib plots."""
    plt.rcParams.update({
        'figure.facecolor': DARK_BG,
        'axes.facecolor': CARD_BG,
        'axes.edgecolor': '#333355',
        'axes.labelcolor': TEXT_COLOR,
        'text.color': TEXT_COLOR,
        'xtick.color': TEXT_COLOR,
        'ytick.color': TEXT_COLOR,
        'grid.color': '#252545',
        'grid.alpha': 0.5,
        'font.family': 'sans-serif',
        'font.size': 11,
    })


def chart_job_matches(analysis_data, save_dir):
    """
    Bar chart: Top 10 job match scores with gradient coloring.
    """
    apply_dark_style()
    fig, ax = plt.subplots(figsize=(12, 7))

    matches = analysis_data['match_results'][:10]
    titles = [m['title'] for m in matches]
    scores = [m['match_score'] for m in matches]

    # Color gradient from cyan to purple based on score
    colors = []
    max_s = max(scores) if scores else 1
    for s in scores:
        ratio = s / max_s
        r = int(0 + (124 - 0) * (1 - ratio))
        g = int(212 + (58 - 212) * (1 - ratio))
        b = int(255 + (237 - 255) * (1 - ratio))
        colors.append(f'#{r:02x}{g:02x}{b:02x}')

    bars = ax.barh(range(len(titles)), scores, color=colors,
                   edgecolor='#ffffff20', linewidth=0.5, height=0.65)

    # Add score labels on bars
    for i, (bar, score) in enumerate(zip(bars, scores)):
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                f'{score}%', va='center', fontsize=11, fontweight='bold',
                color=ACCENT_1)

    ax.set_yticks(range(len(titles)))
    ax.set_yticklabels(titles, fontsize=11)
    ax.set_xlabel('Match Score (%)', fontsize=12, fontweight='bold')
    ax.set_title('TOP JOB MATCHES', fontsize=16, fontweight='bold',
                 color=ACCENT_1, pad=20)
    ax.set_xlim(0, max(scores) * 1.15 if scores else 100)
    ax.invert_yaxis()
    ax.grid(axis='x', alpha=0.3)

    plt.tight_layout()
    path = os.path.join(save_dir, "chart_job_matches.png")
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"  > Saved: chart_job_matches.png")
    return path


def chart_skills_distribution(analysis_data, save_dir):
    """
    Donut chart: Skills distribution by category.
    """
    apply_dark_style()
    fig, ax = plt.subplots(figsize=(9, 9))

    skills = analysis_data['resume_skills']
    if not skills:
        plt.close(fig)
        return None

    categories = list(skills.keys())
    counts = [len(v) for v in skills.values()]
    colors = GRADIENT_COLORS[:len(categories)]
    while len(colors) < len(categories):
        colors.append(ACCENT_4)

    wedges, texts, autotexts = ax.pie(
        counts, labels=None, autopct='%1.0f%%',
        colors=colors, startangle=90,
        pctdistance=0.82, wedgeprops=dict(width=0.4, edgecolor=DARK_BG, linewidth=3)
    )

    for t in autotexts:
        t.set_fontsize(11)
        t.set_fontweight('bold')
        t.set_color('white')

    # Center text
    ax.text(0, 0.05, str(sum(counts)), fontsize=36, fontweight='bold',
            ha='center', va='center', color=ACCENT_1)
    ax.text(0, -0.12, 'SKILLS', fontsize=12, ha='center', va='center',
            color=TEXT_COLOR, fontweight='bold')

    # Legend
    legend_labels = [f'{cat} ({cnt})' for cat, cnt in zip(categories, counts)]
    ax.legend(wedges, legend_labels, loc='lower center',
              bbox_to_anchor=(0.5, -0.08), ncol=2, fontsize=10,
              frameon=False, labelcolor=TEXT_COLOR)

    ax.set_title('SKILLS DISTRIBUTION', fontsize=16, fontweight='bold',
                 color=ACCENT_1, pad=20)

    plt.tight_layout()
    path = os.path.join(save_dir, "chart_skills_distribution.png")
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"  > Saved: chart_skills_distribution.png")
    return path


def chart_skill_gap(analysis_data, save_dir):
    """
    Grouped bar chart: Present vs Missing skills for top jobs.
    """
    apply_dark_style()
    fig, ax = plt.subplots(figsize=(12, 7))

    gaps = analysis_data['skill_gap_analysis'][:5]
    if not gaps:
        plt.close(fig)
        return None

    titles = [g['title'] for g in gaps]
    present = [len(g['present_skills']) for g in gaps]
    missing = [len(g['missing_skills']) for g in gaps]

    x = np.arange(len(titles))
    width = 0.35

    bars1 = ax.bar(x - width / 2, present, width, label='Skills You Have',
                   color=ACCENT_3, edgecolor='#ffffff20', linewidth=0.5)
    bars2 = ax.bar(x + width / 2, missing, width, label='Skills Missing',
                   color=ACCENT_5, edgecolor='#ffffff20', linewidth=0.5)

    # Value labels
    for bar in bars1:
        h = bar.get_height()
        if h > 0:
            ax.text(bar.get_x() + bar.get_width() / 2, h + 0.1,
                    str(int(h)), ha='center', fontsize=11,
                    fontweight='bold', color=ACCENT_3)
    for bar in bars2:
        h = bar.get_height()
        if h > 0:
            ax.text(bar.get_x() + bar.get_width() / 2, h + 0.1,
                    str(int(h)), ha='center', fontsize=11,
                    fontweight='bold', color=ACCENT_5)

    ax.set_xticks(x)
    ax.set_xticklabels(titles, fontsize=10, rotation=15, ha='right')
    ax.set_ylabel('Number of Skills', fontsize=12, fontweight='bold')
    ax.set_title('SKILL GAP ANALYSIS', fontsize=16, fontweight='bold',
                 color=ACCENT_1, pad=20)
    ax.legend(fontsize=11, frameon=False, labelcolor=TEXT_COLOR)
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    path = os.path.join(save_dir, "chart_skill_gap.png")
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"  > Saved: chart_skill_gap.png")
    return path


def chart_radar(analysis_data, save_dir):
    """
    Radar/Spider chart: Multi-dimensional resume strength.
    """
    apply_dark_style()
    fig, ax = plt.subplots(figsize=(9, 9), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(CARD_BG)

    skills = analysis_data['resume_skills']
    all_categories = [
        "Programming Languages", "Data Science & ML", "Web Development",
        "Cloud & DevOps", "Databases", "Tools & Platforms", "Soft Skills"
    ]
    values = []
    for cat in all_categories:
        if cat in skills:
            values.append(min(len(skills[cat]) / 5 * 100, 100))
        else:
            values.append(0)

    # Complete the polygon
    angles = np.linspace(0, 2 * np.pi, len(all_categories), endpoint=False).tolist()
    values_plot = values + [values[0]]
    angles_plot = angles + [angles[0]]

    ax.plot(angles_plot, values_plot, 'o-', linewidth=2.5, color=ACCENT_1)
    ax.fill(angles_plot, values_plot, alpha=0.15, color=ACCENT_1)

    # Category labels
    short_labels = ["Programming", "Data/ML", "Web Dev",
                    "Cloud/DevOps", "Databases", "Tools", "Soft Skills"]
    ax.set_xticks(angles)
    ax.set_xticklabels(short_labels, fontsize=11, fontweight='bold')

    ax.set_ylim(0, 100)
    ax.set_yticks([25, 50, 75, 100])
    ax.set_yticklabels(['25%', '50%', '75%', '100%'], fontsize=9, color='#888')
    ax.grid(color='#333355', alpha=0.5)

    ax.set_title('RESUME STRENGTH RADAR', fontsize=16, fontweight='bold',
                 color=ACCENT_1, pad=30, y=1.08)

    plt.tight_layout()
    path = os.path.join(save_dir, "chart_radar.png")
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"  > Saved: chart_radar.png")
    return path


def chart_match_distribution(analysis_data, save_dir):
    """
    Pie chart: Distribution of match quality levels.
    """
    apply_dark_style()
    fig, ax = plt.subplots(figsize=(8, 8))

    dist = analysis_data['match_distribution']
    labels = ['Excellent (70%+)', 'Good (45-70%)', 'Fair (25-45%)', 'Low (<25%)']
    sizes = [dist['high'], dist['medium'], dist['low'], dist['poor']]
    colors_pie = [ACCENT_3, ACCENT_1, ACCENT_4, ACCENT_5]

    # Filter out zero values
    filtered = [(l, s, c) for l, s, c in zip(labels, sizes, colors_pie) if s > 0]
    if not filtered:
        plt.close(fig)
        return None

    f_labels, f_sizes, f_colors = zip(*filtered)

    wedges, texts, autotexts = ax.pie(
        f_sizes, labels=f_labels, autopct=lambda p: f'{int(round(p * sum(f_sizes) / 100))}',
        colors=f_colors, startangle=140,
        wedgeprops=dict(edgecolor=DARK_BG, linewidth=2),
        textprops={'fontsize': 11}
    )
    for t in autotexts:
        t.set_fontweight('bold')
        t.set_fontsize(13)
        t.set_color('white')

    ax.set_title('MATCH QUALITY DISTRIBUTION', fontsize=16,
                 fontweight='bold', color=ACCENT_1, pad=20)

    plt.tight_layout()
    path = os.path.join(save_dir, "chart_match_distribution.png")
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"  > Saved: chart_match_distribution.png")
    return path


def generate_all_charts(analysis_data, analysis_id):
    """
    Generate all visualization charts and save them.
    
    Args:
        analysis_data: Full analysis dict from Module 6
        analysis_id: Unique session ID
    Returns:
        dict of chart names to file paths
    """
    print("\n" + "=" * 60)
    print("  MODULE 8: VISUALIZATION - Generating Charts")
    print("=" * 60)

    save_dir = os.path.join(RESULTS_DIR, analysis_id)
    os.makedirs(save_dir, exist_ok=True)

    charts = {}
    charts['job_matches'] = chart_job_matches(analysis_data, save_dir)
    charts['skills_dist'] = chart_skills_distribution(analysis_data, save_dir)
    charts['skill_gap'] = chart_skill_gap(analysis_data, save_dir)
    charts['radar'] = chart_radar(analysis_data, save_dir)
    charts['match_dist'] = chart_match_distribution(analysis_data, save_dir)

    # Remove None entries
    charts = {k: v for k, v in charts.items() if v is not None}

    print(f"\n  > Total charts generated: {len(charts)}")
    return charts

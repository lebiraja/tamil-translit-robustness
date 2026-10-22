"""Paper figures from the logged summaries (results/summary/*.csv, results/tune/*.json). Writes vector PDFs to paper/figures/.

  .venv/bin/python scripts/make_figures.py
Every plotted number comes from results/summary or the run JSONs; nothing is typed in by hand.
"""

from __future__ import annotations

import glob
import json
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "paper" / "figures"
S = ROOT / "results" / "summary"
OUT.mkdir(parents=True, exist_ok=True)

# Reference categorical palette (light mode), fixed order; markers/dashes duplicate the colour for grayscale print.
BLUE, ORANGE, AQUA, YELLOW, MAGENTA, GREEN, VIOLET, RED = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"
ARCH_COL = {"lstm": BLUE, "transformer": ORANGE}
ARCH_NAME = {"lstm": "BiLSTM", "transformer": "Transformer"}
mpl.rcParams.update({
    "font.family": "serif", "font.serif": ["STIXGeneral", "DejaVu Serif"], "mathtext.fontset": "stix", "font.size": 8,
    "axes.labelsize": 8, "axes.titlesize": 8, "legend.fontsize": 7, "xtick.labelsize": 7, "ytick.labelsize": 7,
    "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": 0.6, "lines.linewidth": 1.4, "lines.markersize": 4,
    "axes.grid": True, "grid.color": "#e4e2dc", "grid.linewidth": 0.5, "axes.axisbelow": True, "pdf.fonttype": 42, "savefig.bbox": "tight",
})
OPS = ["MIX", "V-DROP", "KEY", "DIGRAPH", "REPEAT", "V-LEN", "GEM"]
OP_STYLE = {"MIX": (VIOLET, "o", "-"), "V-DROP": (BLUE, "s", "-"), "KEY": (ORANGE, "^", "-"), "DIGRAPH": (AQUA, "D", "--"),
            "REPEAT": (MAGENTA, "v", "--"), "V-LEN": (GREEN, "P", ":"), "GEM": (YELLOW, "X", ":")}


def save(fig, name: str) -> None:
    fig.savefig(OUT / f"{name}.pdf")
    plt.close(fig)
    print("wrote", OUT / f"{name}.pdf")


def noise_curves() -> None:
    d = pd.read_csv(S / "c1_degradation.csv")
    c3 = pd.read_csv(S / "c3_clean.csv")
    fig, axes = plt.subplots(1, 2, figsize=(7.1, 2.7), sharey=True)
    for ax, arch in zip(axes, ("lstm", "transformer")):
        clean = float(c3[(c3.arch == arch) & (c3["size"] == "3m")].test_cer_mean.iloc[0])
        ends = []
        for op in OPS:
            col, mk, ls = OP_STYLE[op]
            g = d[(d.arch == arch) & (d["size"] == "3m") & (d.op == op)].sort_values("severity")
            x = [0.0, *g.severity]
            y = [clean, *g.cer_mean]
            e = [0.0, *g.cer_sd]
            ax.errorbar(x, y, yerr=e, color=col, marker=mk, ls=ls, capsize=1.5, elinewidth=0.6, label=op)
            ends.append((y[-1], op, col))
        ends.sort()
        last = -99.0
        for y, op, col in ends:  # direct labels, nudged apart
            yy = max(y, last + 1.35)
            ax.text(0.52, yy, op, color="#333", fontsize=6.5, va="center")
            last = yy
        ax.set_title(f"{ARCH_NAME[arch]} (3M parameters)")
        ax.set_xlabel("noise severity $p$")
        ax.set_xlim(-0.01, 0.62)
        ax.set_xticks([0, 0.1, 0.2, 0.3, 0.5])
    axes[0].set_ylabel("test CER (%)")
    save(fig, "fig_noise_curves")


def architectures() -> None:
    c3 = pd.read_csv(S / "c3_clean.csv")
    d = pd.read_csv(S / "c1_degradation.csv")
    fig, axes = plt.subplots(1, 3, figsize=(7.1, 2.3))
    sizes = ["1m", "3m", "8m"]
    for ax, (title, getter) in zip(axes, [
        ("clean test CER", lambda a, s: (c3[(c3.arch == a) & (c3["size"] == s)].test_cer_mean.iloc[0], c3[(c3.arch == a) & (c3["size"] == s)].test_cer_sd.iloc[0])),
        ("MIX noise $p{=}0.3$ CER", lambda a, s: tuple(d[(d.arch == a) & (d["size"] == s) & (d.op == "MIX") & (d.severity == 0.3)][["cer_mean", "cer_sd"]].iloc[0])),
        ("V-DROP $p{=}0.3$ CER", lambda a, s: tuple(d[(d.arch == a) & (d["size"] == s) & (d.op == "V-DROP") & (d.severity == 0.3)][["cer_mean", "cer_sd"]].iloc[0])),
    ]):
        for arch, mk in (("lstm", "o"), ("transformer", "s")):
            vals = [getter(arch, s) for s in sizes]
            ax.errorbar(range(3), [v[0] for v in vals], yerr=[v[1] for v in vals], color=ARCH_COL[arch], marker=mk, capsize=2, label=ARCH_NAME[arch])
        ax.set_xticks(range(3), ["1M", "3M", "8M"])
        ax.set_title(title)
        ax.set_xlabel("model size (parameters)")
        ax.margins(x=0.15)
    axes[0].set_ylabel("CER (%), mean $\\pm$ sd, 5 seeds")
    h, lab = axes[0].get_legend_handles_labels()
    fig.legend(h, lab, frameon=False, loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.07))
    save(fig, "fig_architectures")


def augmentation() -> None:
    c2 = pd.read_csv(S / "c2.csv")
    conds = ["A0", "A1", "A2", "A3", "A4", "CTRL"]
    metrics = [("clean_cer", "clean test"), ("MIX.0.3_cer", "MIX $p{=}0.3$"), ("V-DROP.0.3_cer", "V-DROP $p{=}0.3$"),
               ("KEY.0.3_cer", "KEY $p{=}0.3$"), ("AK-all_cer", "independent AK-all")]
    fig, axes = plt.subplots(1, 5, figsize=(7.1, 2.4), sharex=True)
    for ax, (m, title) in zip(axes, metrics):
        for arch, off, mk in (("lstm", -0.12, "o"), ("transformer", 0.12, "s")):
            g = c2[(c2.arch == arch) & (c2.condition.isin(conds))].set_index("condition").loc[conds]
            ax.errorbar([i + off for i in range(len(conds))], g[f"{m}_mean"], yerr=g[f"{m}_sd"], color=ARCH_COL[arch], marker=mk, ls="none", capsize=1.5,
                        label=ARCH_NAME[arch])
        ax.set_xticks(range(len(conds)), conds, rotation=60, ha="right")
        ax.set_title(title)
        ax.margins(x=0.1)
    axes[0].set_ylabel("CER (%), mean $\\pm$ sd, 5 seeds")
    h, lab = axes[0].get_legend_handles_labels()
    fig.legend(h, lab, frameon=False, loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.08))
    save(fig, "fig_augmentation")


def heldout() -> None:
    c2 = pd.read_csv(S / "c2.csv")
    fig, axes = plt.subplots(1, 2, figsize=(3.45, 2.3), sharey=False)
    for ax, (op, held) in zip(axes, (("V-DROP", "A2-noVDROP"), ("GEM", "A2-noGEM"))):
        conds = ["A0", "A2", held]
        for arch, off, mk in (("lstm", -0.1, "o"), ("transformer", 0.1, "s")):
            g = c2[(c2.arch == arch)].set_index("condition").loc[conds]
            ax.errorbar([i + off for i in range(3)], g[f"{op}.0.3_cer_mean"], yerr=g[f"{op}.0.3_cer_sd"], color=ARCH_COL[arch], marker=mk, ls="none", capsize=2,
                        label=ARCH_NAME[arch])
        ax.set_xticks(range(3), ["A0", "A2", f"A2\nwithout\n{op}"], fontsize=6.5)
        ax.set_title(f"tested on {op} $p{{=}}0.3$")
        ax.margins(x=0.2)
    axes[0].set_ylabel("CER (%)")
    h, lab = axes[0].get_legend_handles_labels()
    fig.legend(h, lab, frameon=False, loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.07), fontsize=6.5)
    save(fig, "fig_heldout")


def tuning() -> None:
    rows = []
    for f in glob.glob(str(ROOT / "results/tune/*.json")):
        j = json.load(open(f))
        arch, size = j["config"]["arch"], j["config"]["name"].split("-")[1]
        rows.append((arch, size, j["dev"]["cer"]))
    d = pd.DataFrame(rows, columns=["arch", "size", "cer"])
    fig, ax = plt.subplots(figsize=(3.45, 2.4))
    pos = 0
    ticks, labels = [], []
    for arch in ("lstm", "transformer"):
        for size in ("1m", "3m", "8m"):
            v = d[(d.arch == arch) & (d["size"] == size)].cer.sort_values().tolist()
            xs = [pos + (i - len(v) / 2) * 0.03 for i in range(len(v))]
            ax.scatter(xs, v, s=7, color=ARCH_COL[arch], alpha=0.75, linewidths=0)
            ax.hlines(min(v), pos - 0.32, pos + 0.32, color="#222", lw=0.8)
            ticks.append(pos)
            labels.append(f"{'LSTM' if arch == 'lstm' else 'Trans.'}\n{size.upper()}")
            pos += 1
        pos += 0.4
    ax.set_xticks(ticks, labels)
    ax.set_ylabel("dev CER (%), beam 10")
    ax.set_ylim(top=12.5)
    ax.set_title("random search, 20 trials per model\n(bar = best; trials above 12.5% not shown)", fontsize=7)
    save(fig, "fig_tuning")


if __name__ == "__main__":
    noise_curves()
    architectures()
    augmentation()
    heldout()
    tuning()

# Get dialogism scores; make figure 4

from typing import List, Tuple, Dict, Any
import textacy
from latintools import preprocess
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.patches import Patch


def compute_dialogism_scores(
    doc, lex_dict: Dict[str, float], syn_dict: Dict[str, float]
) -> pd.DataFrame:
    """Compute dialogism scores for each token in the doc."""
    rows: List[Dict[str, Any]] = []
    for idx, token in enumerate(doc):
        if not token.is_punct and not token.is_space:
            lemma = token.lemma_.lower()
            lemma_score = lex_dict.get(lemma, 0)
            morphs = token.morph.to_dict()
            morphs_vals = [
                f"MORPH_{label.upper()}_{val.upper()}" for label, val in morphs.items()
            ]
            morphs_vals_scores = [syn_dict.get(mv, 0) for mv in morphs_vals]
            pos = token.pos_
            if pos:
                pos_label = f"POS_{pos.upper()}"
                morphs_vals.append(pos_label)
                morphs_vals_scores.append(syn_dict.get(pos_label, 0))
            morphs_vals_scores_mean = (
                sum(morphs_vals_scores) / len(morphs_vals_scores)
                if morphs_vals_scores
                else 0
            )
            dialogism_score = (lemma_score + morphs_vals_scores_mean) / 2
            rows.append(
                {
                    "idx": idx,
                    "token": token.text,
                    "lemma": token.lemma_,
                    "dialogism_score": dialogism_score,
                }
            )
    return pd.DataFrame(rows)


def plot_dialogism(
    df: pd.DataFrame,
    mean_dialogism: float,
    rolling_window: int,
    speech_ranges: List[Tuple[int, int]],
    apostrophe_ranges: List[Tuple[int, int]],
    outpath: str,
) -> None:
    """Plot rolling dialogism score with speech/apostrophe highlights."""
    dialogism_rolling_mean = (
        df["dialogism_score"].rolling(window=rolling_window, min_periods=1).mean()
    )
    plt.figure(figsize=(15, 5))
    plt.plot(
        df["idx"],
        dialogism_rolling_mean,
        color="black",
        label=f"Rolling Dialogism (window={rolling_window})",
    )
    for start, end in speech_ranges:
        plt.axvspan(
            start + rolling_window / 2,
            end + rolling_window / 2,
            alpha=0.1,
            color="grey",
        )
    for start, end in apostrophe_ranges:
        plt.axvspan(
            start + rolling_window / 2,
            end + rolling_window / 2,
            alpha=0.75,
            color="grey",
        )
    plt.axhline(
        y=mean_dialogism,
        color="grey",
        linestyle="--",
        label="Average dialogism",
    )
    legend_handles = [
        Patch(facecolor="grey", edgecolor="grey", alpha=0.1, label="Direct Speech"),
        Patch(facecolor="grey", edgecolor="grey", alpha=0.75, label="Apostrophe"),
    ]
    handles, _ = plt.gca().get_legend_handles_labels()
    handles += legend_handles
    plt.legend(handles=handles, loc="upper left")
    plt.xlim(0, df["idx"].max())
    plt.ylim(0.15, 0.40)
    plt.grid(color="lightgrey", linestyle="--", linewidth=0.5)
    plt.xlabel("Token Index", fontsize=12)
    plt.ylabel("Value", fontsize=12)
    plt.title("Measuring Dialogism in Lucan Bellum Civile 9", fontsize=18)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(outpath, dpi=300)


def main() -> None:
    la = textacy.load_spacy_lang("la_core_web_lg")
    with open("scripts/fig4/lucan9.txt") as f:
        text = f.read()
    text = preprocess(text, remove_lines=True)
    lex_df = pd.read_csv("lexicons/epic-speech-lexical.tsv", sep="\t", index_col=0)
    syn_df = pd.read_csv("lexicons/epic-speech-syntactic.tsv", sep="\t", index_col=0)
    lex_dict = dict(zip(lex_df["feature"], lex_df["log_odds_weighted_scaled"]))
    syn_dict = dict(zip(syn_df["feature"], syn_df["log_odds_weighted_scaled"]))
    doc = textacy.make_spacy_doc(text, lang=la)
    df = compute_dialogism_scores(doc, lex_dict, syn_dict)
    df.to_csv("scripts/fig4/lucan_9_idx.tsv", sep="\t", index=False)
    mean_dialogism = df["dialogism_score"].mean()
    print("\nMean dialogism:", mean_dialogism)
    rolling_window = 50
    speech_ranges = [
        (348, 627),
        (802, 949),
        (966, 1073),
        (1235, 1406),
        (1452, 1467),
        (1485, 1656),
        (1683, 1874),
        (2503, 2689),
        (3756, 3892),
        (4076, 4101),
        (5632, 5842),
        (6548, 6615),
        (6705, 6829),
        (7039, 7309),
    ]
    apostrophe_ranges = [
        (3528, 3573),
        (4001, 4025),
        (4822, 4867),
        (6483, 6528),
    ]
    plot_dialogism(
        df,
        mean_dialogism,
        rolling_window,
        speech_ranges,
        apostrophe_ranges,
        "figures/fig4.png",
    )


if __name__ == "__main__":
    main()

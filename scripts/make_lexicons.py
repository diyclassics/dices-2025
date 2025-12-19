import pandas as pd
from sklearn.preprocessing import MinMaxScaler


def main() -> None:
    # Load and filter lexical data
    df_lex = pd.read_csv("lexicons/fig2.tsv", sep="\t")
    df_lex = df_lex.dropna()
    df_lex = df_lex[df_lex["type"] == "speech"]

    # Load and filter syntactic data
    df_syn = pd.read_csv("lexicons/fig1.tsv", sep="\t")
    df_syn = df_syn.dropna()
    df_syn = df_syn[df_syn["type"] == "speech"]

    # Scale the 'log_odds_weighted' column
    scaler = MinMaxScaler()
    df_lex["log_odds_weighted_scaled"] = scaler.fit_transform(
        df_lex[["log_odds_weighted"]]
    )
    df_lex = df_lex.sort_values(by="log_odds_weighted_scaled", ascending=False)

    df_syn["log_odds_weighted_scaled"] = scaler.fit_transform(
        df_syn[["log_odds_weighted"]]
    )
    df_syn = df_syn.sort_values(by="log_odds_weighted_scaled", ascending=False)

    df_lex.to_csv("lexicons/epic-speech-lexical.tsv", sep="\t", index=False)
    df_syn.to_csv("lexicons/epic-speech-syntactic.tsv", sep="\t", index=False)


if __name__ == "__main__":
    main()

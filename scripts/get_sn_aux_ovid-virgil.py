import pandas as pd

# Load the DataFrame for lexical counts
df_lex = pd.read_pickle("data/dialogism_lex.pkl")

# Compute total words for Ovid epic and Virgil epic from df_lex
# Use sum of 'n' for all features as total words if 'total_words' column is missing
total_words = (
    df_lex[df_lex["genre"] == "epic"]
    .groupby(["author", "type"])["n"]
    .sum()
    .unstack(fill_value=0)
)

# Load the DataFrame for syntactic counts (contains POS_AUX)
df = pd.read_pickle("data/dialogism_syn.pkl")

# Filter for 'aux' feature
aux_df = df[(df["feature"] == "POS_AUX") & (df["genre"] == "epic")]

# Group by author and type, sum 'n' (raw counts)
aux_counts = aux_df.groupby(["author", "type"])["n"].sum().unstack(fill_value=0)

# Calculate per 100 words
aux_per_100 = (aux_counts / total_words) * 100

for author in ["ovid", "virgil"]:
    print(f"\n{author.capitalize()}:")
    for t in ["narrative", "speech"]:
        raw = aux_counts.loc[author, t] if t in aux_counts.columns else 0
        per_100 = aux_per_100.loc[author, t] if t in aux_per_100.columns else 0
        if raw == 0:
            print(f"{t.capitalize()} 'aux' count: 0 (no data found)")
        else:
            print(f"{t.capitalize()} 'aux' count: {raw} (per 100 words: {per_100:.2f})")

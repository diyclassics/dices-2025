# Use this code to build the feature set used for Figure 2 in chapter

import pandas as pd

# Load data
df = pd.read_pickle("data/dialogism_lex.pkl")

# Subset data
df = df[df["genre"] == "epic"]

# Make dataframe called df_tidy that is grouped by type and retains feature and count
df_tidy = df.groupby(["type", "feature"]).agg({"n": "sum"}).reset_index()
df_tidy = df_tidy[["type", "feature", "n"]]

# Set cutoff, if necessary
CUTOFF = 0
df_tidy = df_tidy[df_tidy["n"] >= CUTOFF]

# Save the tidy dataframe to a TSV file
df_tidy.to_csv("data/sn_tidylo_features_fig2.tsv", sep="\t", index=False)

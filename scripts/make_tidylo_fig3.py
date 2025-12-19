# Use this code to build the feature set used for Figure 3

import pandas as pd

# Load data
df = pd.read_pickle("data/dialogism_syn.pkl")

# Subset data
df = df[df["genre"].isin(["epic"])]

# Make dataframe called df_tidy that is grouped by type and retains feature and count
df_tidy = df.groupby(["author", "type", "feature"]).agg({"n": "sum"}).reset_index()
df_tidy = df_tidy[["author", "type", "feature", "n"]]

# Update author names
author_replace = {
    "lucan": "Lucan",
    "publius_papinius_statius": "Statius",
    "virgil": "Virgil",
    "publius_baebius_italicus": "Ilias Latina",
    "ovid": "Ovid",
    "silius_italicus": "Silius Italicus",
    "lucretius": "Lucretius",
    "gaius_valerius_flaccus": "Valerius Flaccus",
}

for k, v in author_replace.items():
    df_tidy["author"] = df_tidy["author"].replace(k, v)

# df_tidy = df_tidy.rename(columns={"author": "type"})

# Set cutoff, if necessary
CUTOFF = 0
df_tidy = df_tidy[df_tidy["n"] >= CUTOFF]

# Join contents of author and type into type column
df_tidy["type"] = df_tidy["author"] + "_" + df_tidy["type"]
df_tidy = df_tidy.drop(columns=["author"])

df_tidy.to_csv("data/sn_tidylo_features_fig3.tsv", sep="\t", index=False)

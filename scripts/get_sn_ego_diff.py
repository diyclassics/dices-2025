# For numbers reported in p. 191 n. 21

import pandas as pd

# Load the DataFrame from the pickle file
df = pd.read_pickle("data/dialogism_lex.pkl")

# Filter for rows where feature is 'ego'
ego_df = df[df["feature"] == "ego"]

# Group by 'type' (narrative/speech) and sum the counts
ego_counts = ego_df.groupby("type")["n"].sum()

print("Comparative count of 'ego':\n")
for t in ["speech", "narrative"]:
    print(f"{t.capitalize()} 'ego' count: {ego_counts.get(t, 0)}")

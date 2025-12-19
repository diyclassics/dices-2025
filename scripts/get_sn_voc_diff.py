import pandas as pd

# Load the DataFrame from the pickle file
df = pd.read_pickle("data/dialogism_syn.pkl")

# Filter for rows where feature is 'MORPH_CASE_VOC'
voc_df = df[df["feature"] == "MORPH_CASE_VOC"]

# Group by 'type' (narrative/speech) and sum the counts
voc_counts = voc_df.groupby("type")["n"].sum()

print("Comparative count of 'vocative':\n")
for t in ["speech", "narrative"]:
    print(f"{t.capitalize()} vocative count: {int(voc_counts.get(t, 0))}")

# To create the list in the appendix
import pandas as pd

# Path to the pickle file
tsv_path = "data/dialogism_syn.pkl"


# Read the pickle file
df = pd.read_pickle(tsv_path)

# Get the unique features, sort them alphabetically
features = sorted(df["feature"].unique())

# Print each feature on a new line
for feat in features:
    print(feat)

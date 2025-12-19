import glob
import pandas as pd
import textacy
from textacy import text_stats as ts
from natsort import natsorted
from tqdm import tqdm


def normalize_spacing(text):
    return " ".join(text.split())


HOLDOUT = "lucan"

files = natsorted(glob.glob("data/speech_texts/*.txt"))
files = [file for file in files if HOLDOUT not in file]

la = textacy.load_spacy_lang("la_core_web_lg")

data = {}
metadata = {}

for file in tqdm(files):
    with open(file) as f:
        text = f.read()
        text = normalize_spacing(text)

    doc = textacy.make_spacy_doc(text, lang=la)

    data_features = {}
    metadata_features = {}

    wordcount = ts.basics.n_words(doc)
    pos_counts = ts.counts.pos(doc)
    morph_counts = ts.counts.morph(doc)

    for item in pos_counts.items():
        data_features[f"POS_{item[0]}"] = item[1]

    for item in morph_counts.items():
        for item_ in item[1].items():
            data_features[f"MORPH_{item[0].upper()}_{item_[0].upper()}"] = item_[1]

    data[file] = data_features

    metadata_features["type"] = "speech" if "-speech" in file else "narrative"
    metadata_features["author"] = file.split("/")[-1].split("-")[0]
    metadata_features["genre"] = file.split("/")[-1].split("-")[2]

    metadata[file] = metadata_features

df = pd.DataFrame.from_dict(data, orient="index").fillna(0)
metadata_df = pd.DataFrame.from_dict(metadata, orient="index")

# transform df so that each header is a value in one column and its current value is a value in another column
df = df.reset_index()

df = df.melt(id_vars=["index"])
df = df.rename(columns={"index": "file", "variable": "feature", "value": "n"})
df = df.set_index("file")

# filter
df = df[df["feature"] != "POS_"]
df = df[df["feature"] != "POS_NUM"]
df = df[df["feature"] != "POS_SYM"]
df = df[df["feature"] != "POS_PUNCT"]
df = df[df["feature"] != "POS_X"]

# correct mistags of "MORPH_NUMBER_PLURAL" and "MORPH_VERBFORM_CONV"; small number
# of occurrences in the data that will be corrected with next release of LatinCy.

df["feature"] = df["feature"].replace(
    {"MORPH_NUMBER_PLURAL": "MORPH_NUMBER_PLUR"}, regex=True
)

df = df[~df["feature"].str.contains("CONV")]

# merge dfs on index
df = df.merge(metadata_df, left_index=True, right_index=True)

df = df[["feature", "n", "type", "author", "genre"]]

df.to_pickle("data/dialogism_syn.pkl")
df.to_csv("data/dialogism_syn.tsv", sep="\t", index=False)

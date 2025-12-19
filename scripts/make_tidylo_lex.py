import os.path
import glob
import pandas as pd
import textacy
from natsort import natsorted
from tqdm import tqdm
from sklearn.feature_extraction.text import CountVectorizer
from latintools import preprocess


def normalize_spacing(text):
    return " ".join(text.split())


HOLDOUT = "lucan"

files = natsorted(glob.glob("data/speech_texts/*.txt"))
files = [file for file in files if HOLDOUT not in file]

la = textacy.load_spacy_lang("la_core_web_lg")

metadata = {}

for file in tqdm(files):
    metadata_features = {}
    metadata_features["type"] = "speech" if "-speech" in file else "narrative"
    metadata_features["author"] = file.split("/")[-1].split("-")[0]
    metadata_features["genre"] = file.split("/")[-1].split("-")[2]
    metadata[file] = metadata_features

    output_file = f"data/speech_texts_lemmatized/{file.split('/')[-1]}"

    # check if output file already exists
    if os.path.exists(output_file):
        continue

    with open(file) as f:
        text = f.read()
        text = normalize_spacing(text)

    doc = textacy.make_spacy_doc(text, lang=la)
    lemmatized_text = " ".join(
        [
            token.lemma_
            for token in doc
            if token.lemma_.isalpha() and token.text != "que"
        ]
    )

    lemmatized_text = preprocess(lemmatized_text)

    with open(output_file, "w") as f:
        f.write(lemmatized_text)

metadata_df = pd.DataFrame.from_dict(metadata, orient="index")

lemmatized_texts = natsorted(glob.glob("data/speech_texts_lemmatized/*.txt"))
labels = [file.replace("_lemmatized", "") for file in lemmatized_texts]

# Create count vectorizer over lemmatized texts
print("Creating document-term matrix...")
CV = CountVectorizer(input="filename", token_pattern=r"(?u)\b\w+\b", max_features=50000)
dtm = CV.fit_transform(lemmatized_texts)

# Create a DataFrame from the document-term matrix
df = pd.DataFrame(dtm.toarray(), columns=CV.get_feature_names_out(), index=labels)
df = df.rename_axis("filename").reset_index()

# Melt the DataFrame to rows format
df = df.melt(id_vars=["filename"], var_name="feature", value_name="feature_count")
df = df.rename(columns={"filename": "file", "feature_count": "n"})
df = df.set_index("file")

# Merge with metadata
df = df.merge(metadata_df, left_index=True, right_index=True)

df = df[["feature", "n", "type", "author", "genre"]]

# Save dataframe to pickle and CSV
print("Saving dataframe...")
df.to_pickle("data/dialogism_lex.pkl")
df.to_csv("data/dialogism_lex.tsv", sep="\t", index=False)

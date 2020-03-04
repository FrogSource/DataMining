import re
from snorkel.labeling import *
import pandas as pd
import numpy as np
from IPython import display

train = pd.read_csv("tweets_train.csv")
test = pd.read_csv("tweets_test.csv")
LF_set = pd.read_csv("tweets_LF.csv")

test = test.replace({'positive': 1, 'negative': 0})
LF_set = LF_set.replace({'positive': 1, 'negative': 0})

# Define the label mappings for convenience
ABSTAIN = -1
NEGATIVE = 0
POSITIVE = 1

re_manmade_cc = r"\b(manmade|man-made|anthropological|natural)"
re_hoax = r"\b(hoax|scam|fraud)"
re_unscientific = r"\b(pseudoscience|unproven|no evidence)"


@labeling_function()
def lf_man_made(x):
    return POSITIVE if re.search(re_manmade_cc, x) else ABSTAIN


@labeling_function()
def lf_hoax(x):
    return POSITIVE if re.search(re_hoax, x) else ABSTAIN


@labeling_function()
def lf_unscientific(x):
    return POSITIVE if re.search(re_unscientific, x) else ABSTAIN


def make_Ls_matrix(data, LFs):
    noisy_labels = np.empty((len(data), len(LFs)))
    for i, row in data.iterrows():
        for j, lf in enumerate(LFs):
            noisy_labels[i][j] = lf(row['full_text'].lower())
    return noisy_labels


LFs = [lf_man_made, lf_hoax, lf_unscientific]


LF_matrix = make_Ls_matrix(LF_set, LFs)

Y_LF_set = np.array(LF_set['label'])

# Write LF summary to html file
Analysis = LFAnalysis(LF_matrix, LFs)
print(Analysis.label_coverage())
summary = Analysis.lf_summary(Y_LF_set)
html = summary.to_html()
output_file = open("output.html", "w")
output_file.write(html)
output_file.close()

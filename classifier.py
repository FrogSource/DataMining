import re
from sklearn.metrics import classification_report
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
re_impact = r"\b(consequences|impact)"
re_goals = r"\b(goals|targets)"


@labeling_function()
def lf_man_made(x):
    return POSITIVE if re.search(re_manmade_cc, x) else ABSTAIN


@labeling_function()
def lf_hoax(x):
    return POSITIVE if re.search(re_hoax, x) else ABSTAIN


@labeling_function()
def lf_unscientific(x):
    return POSITIVE if re.search(re_unscientific, x) else ABSTAIN


@labeling_function()
def lf_impact(x):
    return NEGATIVE if re.search(re_impact, x) else ABSTAIN


@labeling_function()
def lf_goals(x):
    return NEGATIVE if re.search(re_goals, x) else ABSTAIN


def make_Ls_matrix(data, LFs):
    noisy_labels = np.empty((len(data), len(LFs)), np.int8)
    for i, row in data.iterrows():
        for j, lf in enumerate(LFs):
            noisy_labels[i][j] = int(lf(row['full_text'].lower()))
    return noisy_labels


LFs = [lf_man_made, lf_hoax, lf_unscientific, lf_goals, lf_impact]


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

mlv = MajorityLabelVoter()
Y_train_majority_votes = mlv.predict(LF_matrix)
print(classification_report(Y_LF_set, Y_train_majority_votes))


Ls_train = make_Ls_matrix(train, LFs)

# You can tune the learning rate and class balance.
label_model = LabelModel(cardinality=2)
label_model.seed = 123
label_model.fit(Ls_train, n_epochs=2000, log_freq=1000,
                        lr=0.0001,
                        # class balance represents the distribution of samples in the training set
                        class_balance=np.array([0.7, 0.3]))

Y_train_label_model = label_model.predict(LF_matrix)

print(classification_report(Y_LF_set, Y_train_label_model))

# To use all information possible when we fit our classifier, we can # actually combine our hand-labeled LF set with our training set.
Y_train = label_model.predict(Ls_train) + Y_LF_set


import re
from snorkel.labeling import labeling_function
import pandas as pd

train = pd.read_csv("tweets_train.csv")
test = pd.read_csv("tweets_test.csv")
LF_set = pd.read_csv("tweets_LF.csv")

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

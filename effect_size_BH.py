import pandas as pd  
import numpy as np
from scipy.stats import ttest_ind, ttest_rel, pearsonr, spearmanr  
import matplotlib.pyplot as plt
import statsmodels.stats.multitest as multi

preYoon = "Pre-test: Yoon"
prePFT = "Pre-test: PFT"
postYoon = "Post-test: Yoon"
postPFT = "Post-test: PFT"

dataset = pd.read_csv('scores.csv')
vr_data = dataset[dataset["Training Type"] == "VR"]
paper_data = dataset[dataset["Training Type"] == "Paper"]

# Function below from https://machinelearningmastery.com/effect-size-measures-in-python/
# function to calculate Cohen's d for independent samples
def cohend(d1, d2):
	# calculate the size of samples
	n1, n2 = len(d1), len(d2)
	# calculate the variance of the samples
	s1, s2 = np.var(d1, ddof=1), np.var(d2, ddof=1)
	# calculate the pooled standard deviation
	s = np.sqrt(((n1 - 1) * s1 + (n2 - 1) * s2) / (n1 + n2 - 2))
	# calculate the means of the samples
	u1, u2 = np.mean(d1), np.mean(d2)
	# calculate the effect size
	return (u1 - u2) / s

yoon_pre_vr = np.array(vr_data[preYoon])
yoon_post_vr = np.array(vr_data[postYoon])
yoon_pre_paper = np.array(paper_data[preYoon])
yoon_post_paper = np.array(paper_data[postYoon])

pft_pre_vr = np.array(vr_data[prePFT])
pft_post_vr = np.array(vr_data[postPFT])
pft_pre_paper = np.array(paper_data[prePFT])
pft_post_paper = np.array(paper_data[postPFT])

# Calculate effect size
print("Yoon VR d:", cohend(yoon_post_vr, yoon_pre_vr))
print("Yoon paper d:", cohend(yoon_post_paper, yoon_pre_paper))
print("PFT VR d:", cohend(pft_post_vr, pft_pre_vr))
print("PFT paper d:", cohend(pft_post_paper, pft_pre_paper))

# Do BH multiple comparisons correction for all p-values
p_vals = pd.read_csv('p_vals.csv')
bh_test, corrected_p, _, _ = multi.multipletests(p_vals["p-vals"], method="fdr_bh")
p_vals["Corrected p"] = corrected_p
p_vals.to_csv("p_vals.csv", index=False)
print("Corrected p-vals:", corrected_p)


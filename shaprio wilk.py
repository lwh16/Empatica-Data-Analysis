from numpy.core.numeric import NaN
from scipy import stats
import pandas as pd
import numpy as np
import math

S = "SENDERS_SCR_Count_CSV.csv"
R = "RECEIVERS_SCR_Count_CSV.csv"


Send = pd.read_csv(S, skip_blank_lines = True)
Rec = pd.read_csv(R, skip_blank_lines = True)


RW = Rec["RW"].values
print(RW)
RWshap = stats.shapiro(RW)
print("RW = ")
print(RWshap)

RM = Rec["RM"].values
RMshap = stats.shapiro(RM)
print("RM = ")
print(RMshap)

SM = Send["SM"].values
SMshap = stats.shapiro(SM)
print("SM = ")
print(SMshap)

SV = Send["SV"].values
SVshap = stats.shapiro(SV)
print("SV = ")
print(SVshap)

SW = Send["SW"].values
SWshap = stats.shapiro(SW)
print("SW = ")
print(SWshap)

TTest = stats.ttest_ind(SW, RW, alternative='greater', equal_var=False)
print(TTest)
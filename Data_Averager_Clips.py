#Takes in a csv
import numpy as np
from numpy.core.numeric import NaN
from numpy.lib.polynomial import RankWarning
import pandas as pd
import datetime

name = "DB10_max_C_CSV.csv"
csvLoc = "Senders\\Images\\ConstantTimeFrame\\Outputs\\Analysis\\" + name


PDfile = pd.read_csv(csvLoc, skip_blank_lines = True)
PDfile.dropna(how="all", inplace=True)

averages = np.empty([10,10])

print(PDfile)

sum = 0
x = 0
y = 0
count = 0

current = 0

for col in PDfile.columns:
    try:
        current = int(col)
    except:
        continue
    
    for i in PDfile["clips"]:
        row = int(i)

        if (i == current):
            sum += PDfile[]
import numpy as np
from numpy.core.numeric import NaN
from numpy.lib.polynomial import RankWarning
import pandas as pd
import datetime

name = "8_Georgie"
EDAfile = "Recievers\\" + name + "\\" + "Empatica Data\\EDA.csv"
HRfile = "Recievers\\" + name + "\\" + "Empatica Data\\HR.csv"
IBIfile = "Recievers\\" + name + "\\" + "Empatica Data\\IBI.csv"
TEMPfile = "Recievers\\" + name + "\\" + "Empatica Data\\TEMP.csv"

combined = pd.read_csv("Empatica_Combiner.csv")

EDA = np.genfromtxt(EDAfile, delimiter=",", skip_header=0)
HR = np.genfromtxt(HRfile, delimiter=",", skip_header=0)
IBI = np.genfromtxt(IBIfile, delimiter=",", skip_header=0)
TEMP = np.genfromtxt(TEMPfile, delimiter=",", skip_header=0)

print(EDA[0])

startUNIXtime = HR[0] + 3600
#Heart Rate data starts 10s after eerything else, so void the first 10s of all
for i in range(42):
    EDA = np.delete(EDA,0)
    TEMP = np.delete(TEMP,0)

HR = np.delete(HR,[0,1])

for i in range(EDA.size):
    time = startUNIXtime + i*0.25

    if (i%4 == 0):
        HRval = HR[int(i/4)]
    try:
        row = {"Time" : time , "EDA" : EDA[i] , "HR" : HRval , "TEMP" : TEMP[i]}
        combined = combined.append(row, ignore_index=True)
    except:
        break


combined.to_csv("Recievers\\" + name + "\\Empatica Data\\" + name + "_EDA_HR_TEMP.csv")

#split = combined[combined["Time"] < 1620388958.25]

#print(split)


    

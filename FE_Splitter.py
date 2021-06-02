#Script to plot data with lines marking events
import matplotlib.pyplot as plt

import numpy as np
from numpy.core.numeric import NaN
from numpy.lib.polynomial import RankWarning
import pandas as pd
import datetime


ParticipantType = "Recievers"
dataType = "NVLPS_Data"

columns = ["EDA", "HR" , "TEMP"]

Rnames = ["1_Barty", "2_Rahman" , "3_Rhiannon", "4_Elvis" , "5_Ben L" , "6_Aida" , "7_Ben C" , "8_Georgie"]
Snames = ["Ahogho","Jess","Jordi","Marcus"]


for i in range(len(Rnames)):
    name = Rnames[i]
    print(name)

    UNIXfile = ParticipantType + "\\" + name + "\\" + name + "_UNIX.csv"
    E4file = ParticipantType + "\\" + name + "\\" + "Empatica Data\\NORM_" + name + "_EDA_HR_TEMP.csv"


    UNIX = pd.read_csv(UNIXfile, skip_blank_lines = True)
    UNIX.dropna(how="all", inplace=True)

    startTime = UNIX["startTime"].values
    print(startTime)

    E4 = pd.read_csv(E4file, skip_blank_lines = True)
    E4.dropna(how="all", inplace=True)

    Time = E4["Time"].values
    EDA = E4["TEMP"].values

    plt.plot(Time, EDA)
    plt.title(name)
    for i in range(len(startTime)):
        plt.axvline(startTime[i], 0, 1)
    plt.show()


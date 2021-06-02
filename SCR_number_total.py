#Feature extraction

import numpy as np
from numpy.core.numeric import NaN
from numpy.lib.polynomial import RankWarning
import pandas as pd
import datetime
import os
from scipy import signal
import glob
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

ParticipantType = "Senders"
dataType = "NVLPS_Data"

columns = ["EDA", "HR" , "TEMP"]

folders = ["DT_NFS_Data","DT_NVLPS_Data", "NFS_Data" , "NS_Data"]

preFix = ["LP_" , "VLP_" , "NF_" , "N_"]


Rnames = ["1_Barty", "2_Rahman" , "3_Rhiannon", "4_Elvis" , "5_Ben L" , "6_Aida" , "7_Ben C" , "8_Georgie"]
Snames = ["Ahogho","Jess","Jordi","Marcus"]

#Extracted_Features = pd.read_csv("Blank_Extracted_Features.csv")

df = pd.DataFrame(columns=["file","SCR"])

for i in range(len(Snames)):
    name = Snames[i]
    print(name)
    #accessing the name of this person

    #go into the segmented data and extract the filename
    fileLocation = ParticipantType + "\\" + name + "\\" + "DT_NS_Data\\"


    #iterate through the files there
    for filename in os.listdir(fileLocation):

        f = os.path.join(fileLocation, filename)

        PDfile = pd.read_csv(f)
        EDA = PDfile["EDA"].values

        peaks, _ = find_peaks(EDA)

        #the number of peaks
        SCRnumber = len(peaks)
        print(filename + " = " + str(SCRnumber))
        new_row = {"file" : filename , "SCR" : SCRnumber}
        df = df.append(new_row, ignore_index=True)

df.to_csv("SENDER_SCR_NUMBERS.csv")
#this script takes the data from each of the pandas frames and normalised the physiological columns
import pandas as pd
import os
import glob
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

name = "6_Aida"
ParticipantType = "Recievers"

UNIXfile = ParticipantType + "\\" + name + "\\" + name + "_UNIX.csv"
E4file = ParticipantType + "\\" + name + "\\" + "Empatica Data\\" + name + "_EDA_HR_TEMP.csv"

SegFiles = ParticipantType + "\\" + name + "\\" + "Empatica Data\\Segmented Data"

columns = ["EDA", "HR" , "TEMP"]

Rnames = ["1_Barty", "2_Rahman" , "3_Rhiannon", "4_Elvis" , "5_Ben L" , "6_Aida" , "7_Ben C" , "8_Georgie"]
Snames = ["Ahogho","Jess","Jordi","Marcus"]


for i in range(len(Snames)):
    name = Snames[i]
    print(name)
    directory = ParticipantType + "\\" + name + "\\" + "Empatica Data\\"
    file = directory + "NORM_" + name + "_EDA_HR_TEMP.csv"
    print(file)

    pdFile = pd.read_csv(file, skip_blank_lines = True)
    pdFile.dropna(how="all", inplace=True)
    print("Filtering all data for: " + name)

    for i in range(len(columns)):
            #what columns are working
            column = columns[i]

            if (column == "EDA"):
                sos = signal.butter(6, 0.08, 'low', analog=False, fs=4, output='sos')

            if (column == "TEMP"):
                sos = signal.butter(6, 0.08, 'low', analog=False, fs=4, output='sos')

            if (column == "HR"):
                sos = signal.butter(6, 0.08, 'low', analog=False, fs=4, output='sos')

            #extract the correct signal
            sig = pdFile[column].values

            filteredSig = signal.sosfilt(sos, sig)


            pdFile[column] = filteredSig

            print(pdFile)

    print("Saving data")
    pdFile.to_csv(ParticipantType + "\\" + name + "\\Empatica Data\\" + "VLP_NORM_" + name + "_EDA_HR_TEMP.csv")

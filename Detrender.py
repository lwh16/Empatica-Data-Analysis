#Removes the trend from visible data
import numpy as np
from numpy.core.numeric import NaN
from numpy.lib.polynomial import RankWarning
import pandas as pd
import datetime
import os
from scipy import signal

ParticipantType = "Senders"
dataType = "NVLPS_Data"

columns = ["EDA", "HR" , "TEMP"]

folders = ["NS_Data"]#["NFS_Data","NVLPS_Data"]

Rnames = ["1_Barty", "2_Rahman" , "3_Rhiannon", "4_Elvis" , "5_Ben L" , "6_Aida" , "7_Ben C" , "8_Georgie"]
Snames = ["Ahogho","Jess","Jordi","Marcus"]

for i in range(len(Snames)):
    name = Snames[i]
    print(name)
    os.mkdir(ParticipantType + "\\" + name + "\\Empatica Data\\DT_NS_Data")
    #accessing the name of this person
    for j in range(len(folders)):
        #accessing this folder
        folder = folders[j]

        #create the file location
        fileLocation = ParticipantType + "\\" + name + "\\" + "Empatica Data\\" + folder

        for filename in os.listdir(fileLocation):

            f = os.path.join(fileLocation, filename)

            #print(f)

            if os.path.isfile(f):
                FileToDT = pd.read_csv(f, skip_blank_lines = True)
                FileToDT.dropna(how="all", inplace=True)
                #print(FileToDT)

                #detrend all the columns
                for i in range(len(columns)):
                    column = columns[i]

                    sig = FileToDT[column].values

                    sig_DT = signal.detrend(sig)

                    FileToDT[column] = sig_DT

                #print(FileToDT)
                #resave the file in a new location
                newFileName = ParticipantType + "\\" + name + "\\" + "Empatica Data\\DT_NS_Data\\DT_" + folder + "_" + filename
                print(newFileName)
                FileToDT.to_csv(newFileName)


#this script takes session data and segments it into bins saving each as a new csv with the name indicating the parameters
#first row will also indicate the parameters

import numpy as np
from numpy.core.numeric import NaN
from numpy.lib.polynomial import RankWarning
import pandas as pd
import datetime
import glob

ParticipantType = "Recievers"

columns = ["EDA", "HR" , "TEMP"]

Rnames = ["1_Barty", "2_Rahman" , "3_Rhiannon", "4_Elvis" , "5_Ben L" , "6_Aida" , "7_Ben C" , "8_Georgie"]

for i in range(len(Rnames)):
    name = Rnames[i]
    print(name)
    directory = ParticipantType + "\\" + name + "\\" + "Empatica Data\\"
    files = glob.glob(directory + "*NORM_*")
    if (len(files) == 1):
        E4file = files[0]
    else:
        print("ERROR - there are either 2 or 0 EDA_HR_TEMP files in this directory")
        break



    UNIXfile = ParticipantType + "\\" + name + "\\" + name + "_UNIX.csv"

    UNIX = pd.read_csv(UNIXfile, skip_blank_lines = True)
    UNIX.dropna(how="all", inplace=True)

    E4 = pd.read_csv(E4file, skip_blank_lines = True)
    E4.dropna(how="all", inplace=True)

    segmented_blank = pd.read_csv("Segmented_Blank_R.csv")

    startTime = 0
    page = ""
    SorR = ""


    for index, row in UNIX.iterrows():
        print(index)
        print(row["page"])

        startTime = row["startTime"]
        length = row["length"]
        endTime = startTime + length
        page = row["page"]
        SorR = row["S/R"]

        #remove the first section
        E4 = E4[E4["Time"] >= startTime]

        #create a new segment for this run
        E4_segment = E4[E4["Time"] < endTime]

        #copy a new blank match
        E4_VAD_segment = segmented_blank

        #if washout do something different
        if (page == "Wash Out"):
            for index, E4row in E4_segment.iterrows():
                    new_row = {"Time" : E4row["Time"] , "Clip" : "" , "Page" : page , "S/R" : SorR , "EDA" : E4row["EDA"] , "HR" : E4row["HR"] ,"TEMP" : E4row["TEMP"]}
                    E4_VAD_segment = E4_VAD_segment.append(new_row, ignore_index=True)
                
            E4_VAD_segment.to_csv(ParticipantType + "\\" + name + "\\Empatica Data\\Segmented Data\\" + str(int(startTime)) + "_" + name + "," + "Wash Out" + "_NORM.csv")

        else:
            for index, E4row in E4_segment.iterrows():
                    new_row = {"Time" : E4row["Time"] , "Clip" : row["clip"] , "Page" : page , "S/R" : SorR , "EDA" : E4row["EDA"] , "HR" : E4row["HR"] ,"TEMP" : E4row["TEMP"] , "V" : row["V"], "A" : row["A"], "D" : row["D"], "C" : row["C"], "vis" : row["vis"]}
                    E4_VAD_segment = E4_VAD_segment.append(new_row, ignore_index=True)

            E4_VAD_segment.to_csv(ParticipantType + "\\" + name + "\\Empatica Data\\Segmented Data\\" + str(int(startTime)) + "_" + name + "," + page + "," + row["clip"] + "," + str(int(row["V"])) + ","  + str(int(row["A"])) + "," + str(int(row["D"])) + "," + str(int(row["vis"])) + "_NORM.csv")
                
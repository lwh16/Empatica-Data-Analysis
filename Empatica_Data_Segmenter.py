#this script takes session data and segments it into bins saving each as a new csv with the name indicating the parameters
#first row will also indicate the parameters

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
    E4file = ParticipantType + "\\" + name + "\\" + "Empatica Data\\VLP_NORM_" + name + "_EDA_HR_TEMP.csv"

    UNIX = pd.read_csv(UNIXfile, skip_blank_lines = True)
    UNIX.dropna(how="all", inplace=True)

    E4 = pd.read_csv(E4file, skip_blank_lines = True)
    E4.dropna(how="all", inplace=True)

    segmented_blank = pd.read_csv("Segmented_Blank.csv")

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
                
            E4_VAD_segment.to_csv(ParticipantType + "\\" + name + "\\Empatica Data\\" + dataType + "\\" + str(int(startTime)) + "_" + name + "," + "Wash Out" + ".csv")

        else:
            for index, E4row in E4_segment.iterrows():
                    new_row = {"Time" : E4row["Time"] , "Clip" : row["clip"] , "Page" : page , "S/R" : SorR , "EDA" : E4row["EDA"] , "HR" : E4row["HR"] ,"TEMP" : E4row["TEMP"] , "V" : row["V"], "A" : row["A"], "D" : row["D"], "C" : row["C"]}
                    E4_VAD_segment = E4_VAD_segment.append(new_row, ignore_index=True)

            E4_VAD_segment.to_csv(ParticipantType + "\\" + name + "\\Empatica Data\\" + dataType + "\\" + str(int(startTime)) + "_" + name + "," + page + "," + row["clip"] + "," + str(int(row["V"])) + ","  + str(int(row["A"])) + "," + str(int(row["D"])) + ".csv")
                
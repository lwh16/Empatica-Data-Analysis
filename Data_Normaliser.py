#this script takes the data from each of the pandas frames and normalised the physiological columns
import pandas as pd
import os
import glob

name = "6_Aida"
ParticipantType = "Recievers"

UNIXfile = ParticipantType + "\\" + name + "\\" + name + "_UNIX.csv"
E4file = ParticipantType + "\\" + name + "\\" + "Empatica Data\\" + name + "_EDA_HR_TEMP.csv"

SegFiles = ParticipantType + "\\" + name + "\\" + "Empatica Data\\Segmented Data"

columns = ["EDA", "HR" , "TEMP"]

Rnames = ["1_Barty", "2_Rahman" , "3_Rhiannon", "4_Elvis" , "5_Ben L" , "6_Aida" , "7_Ben C" , "8_Georgie"]
Snames = ["Ahogho","Jess","Jordi","Marcus"]

for i in range(len(Rnames)):
    name = Rnames[i]
    print(name)
    directory = ParticipantType + "\\" + name + "\\" + "Empatica Data\\"
    
    file = directory + name + "_EDA_HR_TEMP.csv"

    pdFile = pd.read_csv(file, skip_blank_lines = True)
    pdFile.dropna(how="all", inplace=True)

    #now need to remove the time segments that are when the person isn't watching the videos
    #remove the top and tail
    UNIXfile = ParticipantType + "\\" + name + "\\" + name + "_UNIX.csv"

    UNIX = pd.read_csv(UNIXfile, skip_blank_lines = True)
    UNIX.dropna(how="all", inplace=True)

    #get the first row
    firstRow = UNIX.iloc[[0]]
    lastRow = UNIX.iloc[[-1]]

    #get the UNIX cutoff points (with 5 second errors)
    start = firstRow["startTime"].values[0] - 5
    end = lastRow["startTime"].values[0] + lastRow["length"].values[0] + 5

    print(start, end)

    #now segment the original pandas fram with this values
    pdFile = pdFile[pdFile["Time"] >= start]
    pdFile = pdFile[pdFile["Time"] < end]



    print("Normalising all data for: " + name)
    for i in range(len(columns)):
            column = columns[i]
            pdFile[column] = (pdFile[column] - pdFile[column].min()) / (pdFile[column].max() - pdFile[column].min())

    print("Saving data")
    pdFile.to_csv(ParticipantType + "\\" + name + "\\Empatica Data\\" + "NORM_" + name + "_EDA_HR_TEMP.csv")

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

Extracted_Features = pd.read_csv("Blank_Extracted_Features.csv")

for i in range(len(Snames)):
    name = Snames[i]
    print(name)
    #accessing the name of this person

    #go into the segmented data and extract the filename
    fileLocation = ParticipantType + "\\" + name + "\\" + "Empatica Data\\NS_Data"

    #iterate through the files there
    for filename in os.listdir(fileLocation):

        f = os.path.join(fileLocation, filename)

        fileLocations = []

        if os.path.isfile(f):
            #now you know the file exists in NS_Data - access the same file in the others
            for j in range(len(folders)):
                #accessing this folder
                folder = folders[j]
                otherFileLocation = ParticipantType + "\\" + name + "\\" + "Empatica Data\\" + folder
                
                for file in glob.glob(otherFileLocation + "//*" + filename + "*"):
                    fileLocations.append(file)

        
        print(fileLocations)

        new_row = {"Page" : filename , "SorR" : ParticipantType}

        #access the basic info
        try:
            VADfile = pd.read_csv(f, skip_blank_lines = True)
            new_row["V"] = VADfile["V"].values[1]
            new_row["A"] = VADfile["A"].values[1]
            new_row["D"] = VADfile["D"].values[1]
            new_row["C"] = VADfile["C"].values[1]
            new_row["Clip"] = VADfile["Clip"].values[1]
            new_row["Time"] = VADfile["Time"].values[1]
            new_row["Name"] = name
        except:
            #if this doesn't work, then you've reach marcus - so fuck that
            break
        print(len(fileLocations))
        for k in range(len(fileLocations)):
            #this is the data
            print(k)
            try:
                typeOfData = folders[k]
            except:
                break

            if ((typeOfData == "DT_NFS_Data") or (typeOfData == "DT_NVLPS_Data") or (typeOfData == "NS_Data")):
                #this means you need to extract the SCR data from this files
                print(fileLocations[k])
                PDfile = pd.read_csv(fileLocations[k], skip_blank_lines = True)
                PDfile.dropna(how="all", inplace=True)

                for m in range(len(columns)):
                    #access the column individually
                    column = columns[m]
                    sig = PDfile[column].values

                    #now add these new values to the row
                    nameCode = preFix[k] + "SCR_" + column + "_"

                    peaks, _ = find_peaks(sig)

                    #the number of peaks
                    SCRnumber = len(peaks)
                    new_row[nameCode + "NUM_PEAKS"] = SCRnumber


                    #the amplitude of the peaks
                    peakAmps = []
                    for l in range(len(peaks)):
                        peakAmps.append(sig[peaks[l]])
                    
                    #the mean amplitude
                    meanAmp = np.mean(peakAmps)
                    new_row[nameCode + "MEAN_PEAK_AMP"] = meanAmp
                    
                    if (SCRnumber > 0):
                        #max amplitude
                        maxAmp = np.amax(peakAmps)
                        new_row[nameCode + "MAX_PEAK_AMP"] = maxAmp
                    else:
                        new_row[nameCode + "MAX_PEAK_AMP"] = ""


            if ((typeOfData == "NS_Data") or (typeOfData == "NFS_Data")):
                #this means the feature extraction is standard
                #load the data into a pandas frame
                print(fileLocations[k])
                PDfile = pd.read_csv(fileLocations[k], skip_blank_lines = True)
                PDfile.dropna(how="all", inplace=True)

                for m in range(len(columns)):
                    #access the column individually
                    column = columns[m]
                    sig = PDfile[column].values

                    #now add these new values to the row
                    nameCode = preFix[k] + column + "_"

                    #extract the features
                    minimum = np.amin(sig)
                    #new_row[nameCode + "MIN"] = minimum

                    maximum = np.amax(sig)
                    #new_row[nameCode + "MAX"] = maximum
                    
                    mean = np.mean(sig)
                    #new_row[nameCode + "MEAN"] = mean

                    std = np.std(sig)
                    #new_row[nameCode + "STD"] = std

                    var = np.var(sig)
                    #new_row[nameCode + "VAR"] = var

                    rms = np.sqrt(np.mean(sig**2))
                    #new_row[nameCode + "RMS"] = rms

                    #Means of the absolute values of differences
                    FirstArrayEnd = np.delete(sig,[0])
                    FirstArrayStart = np.delete(sig,[-1])
                    mAbsValFirstDiff = np.mean(FirstArrayEnd - FirstArrayStart)
                    #new_row[nameCode + "MAV1stD"] = mAbsValFirstDiff

                    SecondArrayEnd = np.delete(sig,[0,1])
                    SecondArrayStart = np.delete(sig,[-1,-2])
                    mAbsValSecondDiff = np.mean(SecondArrayEnd - SecondArrayStart)
                    #new_row[nameCode + "MAV2ndD"] = mAbsValSecondDiff

        try:
            new_row["SCR_RATIO_EDA"] = new_row["VLP_SCR_EDA_NUM_PEAKS"] / new_row["LP_SCR_EDA_NUM_PEAKS"]
        except:
            new_row["SCR_RATIO_EDA"] = ""
        try:
            new_row["SCR_RATIO_HR"] = new_row["VLP_SCR_HR_NUM_PEAKS"] / new_row["LP_SCR_HR_NUM_PEAKS"]
        except:
            new_row["SCR_RATIO_HR"] = ""
        try:
            new_row["SCR_RATIO_TEMP"] = new_row["VLP_SCR_TEMP_NUM_PEAKS"] / new_row["LP_SCR_TEMP_NUM_PEAKS"]
        except:
            new_row["SCR_RATIO_TEMP"] = ""

        #now add this row to the pd file
        Extracted_Features = Extracted_Features.append(new_row, ignore_index=True)
        print("New row added to the file....")

#send this to a file
Extracted_Features.to_csv(ParticipantType + "\\" + ParticipantType + "_Feature_Extracted_Data_rework" + ".csv")
                
        









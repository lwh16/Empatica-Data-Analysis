#Crop the images exported from matlab
import glob
from PIL import Image
import os

ParticipantType = "Senders"

columns = ["EDA", "HR" , "TEMP"]

Rnames = ["1_Barty", "2_Rahman" , "3_Rhiannon", "4_Elvis" , "5_Ben L" , "6_Aida" , "7_Ben C" , "8_Georgie"]
Snames = ["Ahogho","Jess","Jordi","Marcus"]
DataTypes = ["MEXH", "SYM6" , "DB10", "MEYER"]


testLoc = ParticipantType + "\\Images\\" + DataTypes[0] + "\\EDA\\"

for i in range(len(DataTypes)):

    #for j in range(len(columns)):

    folderLoc = ParticipantType + "\\Images\\ConstantTimeFrame\\" + DataTypes[i] + "\\DT_NS_Data\\EDA\\"

    if (0 == 0):
        os.mkdir(folderLoc + "\\Wash Out")
        os.mkdir(folderLoc + "\\Action")


    for filename in os.listdir(folderLoc):
        if ((filename == "Wash Out") or (filename == "Action")):
            pass
        else:
            f = os.path.join(folderLoc, filename)
            if ("Wash Out" in filename):
                print(filename)
                os.rename(f,(folderLoc + "\\Wash Out\\" + filename))
            else:
                print(filename)
                os.rename(f,(folderLoc + "\\Action\\" + filename))
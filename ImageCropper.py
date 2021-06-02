#Crop the images exported from matlab
import glob
from PIL import Image
import os

ParticipantType = "Recievers"

columns = ["EDA", "HR" , "TEMP"]

Rnames = ["1_Barty", "2_Rahman" , "3_Rhiannon", "4_Elvis" , "5_Ben L" , "6_Aida" , "7_Ben C" , "8_Georgie"]
Snames = ["Ahogho","Jess","Jordi","Marcus"]
DataTypes = ["DT_NS_Data"]


#testLoc = ParticipantType + "\\Images\\" + DataTypes[0] + "\\EDA\\"

for i in range(len(DataTypes)):

    for j in range(len(columns)):

        folderLoc = ParticipantType + "\\Images\\" + DataTypes[i] + "\\" + columns[j]

        os.mkdir(folderLoc + "\\Cropped")

        for filename in os.listdir(folderLoc):
            if (filename == "Cropped"):
                pass
            else:
                f = os.path.join(folderLoc, filename)

                im = Image.open(f)
                print(filename)
                print(im.size)
                im1 = im.crop((186,62,1522,1124))
                
                im1.save(folderLoc + "\\Cropped\\" + columns[j] + "_" + filename)
import numpy as np
from numpy.core.numeric import NaN
from numpy.lib.polynomial import RankWarning
import pandas as pd
import datetime

name = "Ahogho"
oldFile = "Senders\\" + name + "\\" + name +"_rawCSV.csv"

data = pd.read_csv(oldFile, skip_blank_lines = True)
data.dropna(how="all", inplace=True)

day = 7

new_data = pd.read_csv("Blank_Time_Log.csv")

for index, row in data.iterrows():

    if (row["page"] == "5_Wash_Out"):

        if (row["action"] == "open"):
            startTime = row["time"]
            startTimeVals = startTime.split(":")
            startUNIXstamp = (datetime.datetime(2021,5,day,int(startTimeVals[0]),int(startTimeVals[1]),int(startTimeVals[2])) - datetime.datetime(1970,1,1,0,0,0)).total_seconds()
            print(startUNIXstamp, startTime)


        if (row["action"] == "next"):
            endTime = row["time"]
            endTimeVals = endTime.split(":")
            endUNIXstamp = (datetime.datetime(2021,5,day,int(endTimeVals[0]),int(endTimeVals[1]),int(endTimeVals[2])) - datetime.datetime(1970,1,1,0,0,0)).total_seconds()
            print("WashOut End ", endUNIXstamp, endTime)
            duration = endUNIXstamp - startUNIXstamp
            new_row = {"startTime":startUNIXstamp , "length" : duration , "page" : "Wash Out" , "clip" : "", "S/R" : "S" , "W/T" : "", "V" : NaN , "A" : NaN , "D" : NaN , "C" : NaN}
            new_data = new_data.append(new_row, ignore_index=True)



    if (row["page"] == "6_Video"):

        if (row["action"] == "Video Start"):
            #take the clip value
            clip = row["val1"]
            startTime = row["time"]
            startTimeVals = startTime.split(":")
            startUNIXstamp = (datetime.datetime(2021,5,day,int(startTimeVals[0]),int(startTimeVals[1]),int(startTimeVals[2])) - datetime.datetime(1970,1,1,0,0,0)).total_seconds()
            print("Video start: ", startUNIXstamp, startTime)
        
        if (row["action"] == "Video Ended"):
            endTime = row["time"]
            endTimeVals = endTime.split(":")
            endUNIXstamp = (datetime.datetime(2021,5,day,int(endTimeVals[0]),int(endTimeVals[1]),int(endTimeVals[2])) - datetime.datetime(1970,1,1,0,0,0)).total_seconds()
            print("Video End ", endUNIXstamp, endTime)
            



    if (row["page"] == "7_Self_Report"):

        if (row["action"] == "7_Self_Report"):
            V = row["val2"]
            A = row["val3"]
            D = row["val4"]
            new_row = {"startTime":startUNIXstamp , "length" : 0 , "page" : "Video" , "clip" : clip, "S/R" : "S" , "W/T" : "W", "V" : NaN , "A" : NaN , "D" : NaN , "C" : NaN}



    if (row["page"] == "8_Write_Message"):

        if (row["action"] == "open"):
            MessageStartTime = row["time"]
            startTimeVals = MessageStartTime.split(":")
            MessageStartUNIXstamp = (datetime.datetime(2021,5,day,int(startTimeVals[0]),int(startTimeVals[1]),int(startTimeVals[2])) - datetime.datetime(1970,1,1,0,0,0)).total_seconds()
            print("Message start: ", MessageStartUNIXstamp, MessageStartTime)

        if (row["action"] == "8_Write_Message"):
            MessageEndTime = row["time"]
            endTimeVals = MessageEndTime.split(":")
            MessageEndUNIXstamp = (datetime.datetime(2021,5,day,int(endTimeVals[0]),int(endTimeVals[1]),int(endTimeVals[2])) - datetime.datetime(1970,1,1,0,0,0)).total_seconds()
            print("Message End ", MessageEndUNIXstamp, MessageEndTime)


    if (row["page"] == "9_Confidence"):
        if (row["action"] == "9_Confidence"):
            C = row["val2"]

            VideoDuration = endUNIXstamp - startUNIXstamp
            video_new_row = {"startTime":startUNIXstamp , "length" : VideoDuration , "page" : "Video" , "clip" : clip, "S/R" : "S" , "W/T" : "W", "V" : V , "A" : A , "D" : D , "C" : C}
            new_data = new_data.append(video_new_row, ignore_index=True)

            MessageDuration = MessageEndUNIXstamp - MessageStartUNIXstamp
            message_new_row = {"startTime":MessageStartUNIXstamp , "length" : MessageDuration , "page" : "Message" , "clip" : clip, "S/R" : "S" , "W/T" : "T", "V" : V , "A" : A , "D" : D , "C" : C}
            new_data = new_data.append(message_new_row, ignore_index=True)



#pd.set_option("display.max_rows", None, "display.max_columns", None)
print(new_data)
new_data.to_csv(name + "_UNIX.csv")
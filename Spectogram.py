import pandas as pd
import numpy as np
import os
import scipy
from scipy import signal
from scipy.fft import fftshift
import matplotlib.pyplot as plt

name = "Jordi"
ParticipantType = "Senders"

UNIXfile = ParticipantType + "\\" + name + "\\" + name + "_UNIX.csv"
E4file = ParticipantType + "\\" + name + "\\" + "Empatica Data\\" + name + "_EDA_HR_TEMP.csv"

NormFiles = ParticipantType + "\\" + name + "\\" + "Empatica Data\\Segmented Data"

columns = ["EDA", "HR" , "TEMP"]

fs = 4

print(NormFiles)

for filename in os.listdir(NormFiles):

    f = os.path.join(NormFiles, filename)
    print(filename)
    if os.path.isfile(f):
        FileToSpec = pd.read_csv(f, skip_blank_lines = True)
        FileToSpec.dropna(how="all", inplace=True)
        #print(FileToSpec)
        #now iterate through the columns that need to be normalised
        EDA = FileToSpec["EDA"].values

        EDA = np.array(EDA)
        print(EDA)
        print(filename + " = " + str(EDA.shape))

        fs = 4

        f, t, Sxx = signal.spectrogram(EDA, fs)
        print("f")
        print(f)
        print("t")
        print(t)
        print("Sxx")
        print(Sxx)
        print("plotting")
        plt.pcolormesh(t, f, Sxx, shading='gouraud')
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
        plt.title(filename)
        plt.show()
        
        
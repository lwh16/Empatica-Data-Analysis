#Feature Extraction NN

import torch
from torchvision import transforms, datasets
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import time
import pandas as pd
import numpy as np

ParticipantType = "Recievers"

Xdata = pd.read_csv(ParticipantType + "\\Recievers_X_Data.csv")
Ydata = pd.read_csv(ParticipantType + "\\Recievers_Y_Data.csv")

TestY = (Ydata[36:54])

print(Ydata)



#distingish between wash out and message reading
#make the labels only the difference between the two
Ydata = Ydata["Page"].values
Y = []
for i in range(len(Ydata)):
    if ("Wash" in Ydata[i]):
        Y.append(int(0))

    else:
        Y.append(int(1))

X = Xdata.values

for i in range(18):
    Y = np.delete(Y, (36), axis=0)
    X = np.delete(X, (36), axis=0)

for j in range(len(Ydata)):
    print(Ydata[j])

print(len(Y))

X = Xdata.values

xInput = len(X[0])
print(xInput)

xT = torch.Tensor(X)
yT = torch.Tensor(Y)
yT = yT.type(torch.LongTensor)
print(xT)
print(yT)


dataset = torch.utils.data.TensorDataset(xT, yT)
print(dataset[2])
trainset = torch.utils.data.DataLoader(dataset, shuffle = True)
print("here")
print(trainset)


class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(78, 50)
        self.fc2 = nn.Linear(50,2)
        self.fc3 = nn.Linear(64,64)
        self.fc4 = nn.Linear(64,2)

    def forward(self, x):
        x = torch.sigmoid(self.fc1(x))
        #x = torch.sigmoid(self.fc2(x))
        #x = torch.sigmoid(self.fc3(x))
        x = self.fc2(x)

        return F.softmax(x, dim = 1)

net = Net()
t1 = time.time()
print(t1)
optimizer = optim.Adam(net.parameters(), lr = 0.001)
print("7")
Epochs = 100

for epoch in range(Epochs):
    for data in trainset:
        X, y = data
        #print(X)
        #print(y)
        #print(type(y))
        net.zero_grad()
        output = net.forward(X)

        loss = F.nll_loss(output, y)
        loss.backward()
        optimizer.step()

print("8")
total = 0
correct = 0
with torch.no_grad():
    for data in trainset:
        X,y = data
        output = net.forward(X)
        for idx, i in enumerate(output):
            if torch.argmax(i) == y[idx]:
                correct += 1
            total += 1

print("Accuracy: ", round(correct/total,3))
print(time.time() - t1)

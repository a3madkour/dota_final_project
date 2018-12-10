#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import svm
from parseData import readHeroes
import torch
import torch.nn as nn
import torchvision 
import torchvision.transforms as transforms


# In[5]:


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu') 


# In[6]:


def plotHeroUsage(Y,N):
    heroes = Y['hero_picked'].unique()
    counts = []
    for hero in heroes:
        counts.append(len(Y[Y['hero_picked'] == hero]))
    counts = np.array(counts)
    heroes = heroes[counts.argsort()[-N:]]
    counts = counts[counts.argsort()[-N:]]
    print(counts[-1]/len(Y))
    y_pos = np.arange(len(heroes))
    plt.bar(y_pos,counts, align='center', alpha=0.5)
    plt.xticks(y_pos,heroes)
    plt.ylabel('counts')
    plt.title('Hero usage')
    plt.show()


# In[7]:


class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size) 
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, num_classes)  
    
    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out


# In[8]:


def toHeroID(Y):
    hero_ids = []
    for y in Y:
        if np.argwhere(y==1).size <= 0:
            hero_ids.append(0)
        else:
            hero_ids.append(np.argwhere(y==1)[0][0] +1)
    return np.array(hero_ids) 


# In[11]:


data = pd.read_csv('40813418_22_rolesRep_all_X.csv')
Y = pd.read_csv('40813418_22_simpleRep_all_Y.csv')
skip_ban = False
if ('banned_hero1'not in data.columns):
    skip_ban = True
heroes =  readHeroes()
num_heroes = int(list(heroes.keys())[-1])
data =  data.dropna(1,'all')


# In[12]:


plotHeroUsage(Y,10)


# In[13]:


X = data.drop(columns=['match_id','version','start_time'])
X = X.fillna(0)
# allies = np.zeros((X.shape[0],num_heroes))
# enemies = np.zeros((X.shape[0],num_heroes))
# if not skip_ban:
#     banned = np.zeros((X.shape[0],num_heroes))
# output = np.zeros((Y.shape[0],num_heroes))
# for i,row in X.iterrows():
#     allies[i,int(row['ally_hero1'])-1] = 1
#     allies[i,int(row['ally_hero2'])-1] = 1
#     allies[i,int(row['ally_hero3'])-1] = 1
#     allies[i,int(row['ally_hero4'])-1] = 1
#     enemies[i,int(row['enemy_team1'])-1] = 1
#     enemies[i,int(row['enemy_team2'])-1] = 1
#     enemies[i,int(row['enemy_team3'])-1] = 1
#     enemies[i,int(row['enemy_team4'])-1] = 1
#     enemies[i,int(row['enemy_team5'])-1] = 1
#     if not skip_ban:
#         if 'banned_hero1' in row:
#             banned[i,int(row['banned_hero1'])-1] = 1
#         if 'banned_hero2' in row:
#             banned[i,int(row['banned_hero2'])-1] = 1
#         if 'banned_hero3' in row:
#             banned[i,int(row['banned_hero3'])-1] = 1
#         if 'banned_hero4' in row:
#             banned[i,int(row['banned_hero4'])-1] = 1
#         if 'banned_hero5' in row:
#             banned[i,int(row['banned_hero5'])-1] = 1
#         if 'banned_hero6' in row:
#             banned[i,int(row['banned_hero6'])-1] = 1
#         if 'banned_hero7' in row:
#             banned[i,int(row['banned_hero7'])-1] = 1
#         if 'banned_hero8' in row:
#             banned[i,int(row['banned_hero8'])-1] = 1
#         if 'banned_hero9' in row:
#             banned[i,int(row['banned_hero9'])-1] = 1
#         if 'banned_hero10' in row:
#             banned[i,int(row['banned_hero10'])-1] = 1
#         if 'banned_hero11' in row:
#             banned[i,int(row['banned_hero11'])-1] = 1
#         if 'banned_hero12' in row:
#             banned[i,int(row['banned_hero12'])-1] = 1
#     hero_picked = Y['hero_picked'][i]
#     hero_picked = Y['hero_picked'][i]
#     output[i,hero_picked-1] = 1


# In[14]:


X_train, X_test, y_train, y_test = train_test_split(X,Y)


# In[15]:


clf = RandomForestClassifier(n_estimators=100)
rf = clf.fit(X_train,y_train)


# In[16]:


prediction = rf.predict(X_test)
ground_truth = np.array(y_test).flatten()
np.sum(prediction == ground_truth) / len(ground_truth)


# In[17]:


clf = svm.SVC(decision_function_shape='ovo')
svm_model = clf.fit(X_train,y_train)


# In[18]:


prediction = svm_model.predict(X_test)
ground_truth = np.array(y_test).flatten()
np.sum(prediction == ground_truth) / len(ground_truth)


# In[ ]:


# if not skip_ban:
#     X = np.concatenate((allies,enemies,banned),1)
# else:
#     X = np.concatenate((allies,enemies),1)
    
# Y = output
# X_train, X_test, y_train, y_test = train_test_split(X,Y)


# In[26]:


input_size = X_train.shape[1]
# actual_ids = toHeroID(y_train)-1
actual_ids = np.array(y_train['hero_picked']) -1
# output_size = y_train.shape[1]
output_size = num_heroes
hidden_size = 5
num_epochs = 100000
batch_size = 100
learning_rate = 0.001
# log_model = nn.Linear(input_size,output_size)
# might need a sigmoid ^
nn_model = NeuralNet(input_size,hidden_size,output_size)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(nn_model.parameters(), lr = learning_rate)
for epoch in range(num_epochs):
    # Convert numpy arrays to torch tensors
    inputs = torch.from_numpy(np.array(X_train,dtype=np.float32))
    targets = torch.from_numpy(np.array(actual_ids,dtype=np.int64))

    # Forward pass
    outputs = nn_model(inputs)
    loss = criterion(outputs.squeeze(), targets)
    
    # Backward and optimize
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    if (epoch+1) % 5 == 0:
        print ('Epoch [{}/{}], Loss: {:.4f}'.format(epoch+1, num_epochs, loss.item()))


# In[27]:


prediction = nn_model(torch.from_numpy(np.array(X_test,dtype=np.float32))).detach().numpy()


# In[28]:


# labels = np.argmax(y_test,axis=1)+1
labels = np.array(y_test).flatten()
sum((np.argmax(prediction,axis=1)+1) == labels )/ len(labels)


# In[29]:


clf = RandomForestClassifier(n_estimators=100)
rf = clf.fit(X_train,y_train)


# In[30]:


prediction = rf.predict(X_test)
sum((np.argmax(prediction,axis=1)+1) == labels )/ len(labels)


# In[ ]:





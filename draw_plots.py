#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from parseData import readHeroes



# In[2]:


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu') 


# In[3]:


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
    plt.title(player_id+ ' Hero usage')
    plt.savefig('plots/'+player_id+'_hero_use.png')
    plt.show()



# In[5]:


def toHeroID(Y):
    hero_ids = []
    for y in Y:
        if np.argwhere(y==1).size <= 0:
            hero_ids.append(0)
        else:
            hero_ids.append(np.argwhere(y==1)[0][0] +1)
    return np.array(hero_ids) 


# In[29]:


player_id = '87278757'

# player_id = '34505203'
# player_id = '82262664'
# player_id = '106863163'
data = pd.read_csv('csvs/'+player_id+'_2_simpleRep_all_X.csv')
Y = pd.read_csv('csvs/'+player_id+'_2_simpleRep_all_Y.csv')
skip_ban = False
if ('banned_hero1'not in data.columns):
    skip_ban = True
heroes =  readHeroes()
num_heroes = int(list(heroes.keys())[-1])
data =  data.dropna(1,'all')


# In[40]:


player_id = '87278757'
data_87 = [0.2117318788031655,0.5432470494267008,0.6602242750995786,0.8881199356811804,0.9359649399375729,0.8331336507235867,0.2783785772088575,0.8972317684522496,0.9981608180681233,0.985291799350506,0.9924803733013842,0.9940673245683177,0.995748862334605,0.9959590545553909,0.9963689293859235,0.9971203665752331,0.9974671837395298,0.9978034912927872,0.9981818372902019,0.9984130487330664,0.9985654380931361,0.9985654380931361,0.998628495759372,0.998628495759372,0.998628495759372,0.998628495759372,0.998628495759372,0.998628495759372,0.998628495759372,0.9986600245924898,0.9986600245924898,0.9986600245924898,0.9986600245924898,0.9986600245924898,0.9986600245924898,0.9986600245924898,0.9986600245924898,0.9986600245924898,0.9986600245924898,0.9986600245924898,0.9986600245924898,0.9986600245924898,0.9986600245924898,0.9986600245924898,0.9986600245924898,0.9986600245924898,0.9986600245924898,0.9986600245924898,0.9986600245924898,0.9986600245924898]
y_pos = np.arange(len(data_87))
plt.plot(y_pos,data_87)
plt.ylabel('Performance')
plt.xlabel('Epoch')
plt.title(player_id +' LSTM' )
plt.savefig('plots/'+player_id +'_lstm.png' )


# In[30]:


version_types = data['version'].drop_duplicates()
version_counts = []
for version in version_types:
    version_counts.append(len(data[data['version'] == version]))
print(version_counts)
y_pos = np.arange(len(version_types))
plt.bar(y_pos,version_counts, align='center', alpha=0.5)
plt.xticks(y_pos,version_types)
plt.ylabel('counts')
plt.savefig('plots/'+player_id+'_versions_played.png')
plt.title(player_id+ ' Hero usage')



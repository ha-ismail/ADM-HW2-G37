#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

#pd.set_option('display.mpl_style', 'default') # Make the graphs a bit prettier
plt.rcParams['figure.figsize'] = (15, 5)

# read taxi data for Jan 2018
data='yellow_tripdata_2018-01.csv'
yt_data = pd.read_csv(data)

# read zone lookup table
zones = 'taxi_zone_lookup.csv'
zonesLookup = pd.read_csv(zones)


# Merge the data with taxi zones table (taking only data we need for the QR#2)
yt_data_merged= yt_data[['tpep_pickup_datetime','passenger_count','PULocationID']].merge(zonesLookup[['LocationID','Borough']],how='inner', left_on='PULocationID', right_on='LocationID')

yt_data_merged


# In[56]:


#del yt_data

qr2 = yt_data_merged[['tpep_pickup_datetime','passenger_count','Borough']]
# Get the hour from the pickup time column
#yt_qr1['tpep_pickup_datetime']=yt_qr1['tpep_pickup_datetime'].apply(lambda x: pd.core.tools.datetimes.to_datetime(x).hour)
#yt_qr1


# In[57]:


qr2


# In[58]:


from datetime import datetime
# Getting the hour from the pickup time
qr2.iloc[:,0] = qr2.iloc[:,0].apply(lambda x: pd.to_datetime(x).hour)


# In[59]:



qr2


# In[60]:


qr2[['tpep_pickup_datetime','passenger_count']].groupby('tpep_pickup_datetime').sum()


# In[69]:


fig, ax = plt.subplots(figsize=(15,7))
# Modify the x-axis to show numbers between 0-23
plt.xticks(list(range(24)))
qr2[['tpep_pickup_datetime','passenger_count']].groupby('tpep_pickup_datetime').sum().plot(ax=ax,kind="line")


# In[ ]:


'''
    Visualizing the number of passenger per hour in NY, we notice:
    the peak of number of passengers is at 18, it decreases at 4-5 morning, 
    and start increasing sharply until 8 (workers and students time), 
    after that it has a normal increase un til it reaches the peak at 18 
    and then starts decreasing until reaching the lowest at 4am.
    
'''


# In[71]:


# Group by time slots and Borough and calculate the mean of passengers
qr2[['tpep_pickup_datetime','passenger_count','Borough']].groupby(['tpep_pickup_datetime','Borough'])['passenger_count'].sum()
#qr2[['tpep_pickup_datetime','passenger_count','Borough']].groupby(['Borough','tpep_pickup_datetime']).['passenger_count'].sum()


# In[72]:


fig, ax = plt.subplots(figsize=(15,7))
# Modify the x-axis to show numbers between 0-23
plt.xticks(list(range(24)))
qr2[['tpep_pickup_datetime','passenger_count','Borough']].groupby(['tpep_pickup_datetime','Borough'])['passenger_count'].sum().unstack().plot(ax=ax)
#qr2[['tpep_pickup_datetime','passenger_count','Borough']].groupby(['tpep_pickup_datetime','Borough'])['passenger_count'].mean().unstack().plot(ax=ax)


# In[ ]:


''' THE BELOW COMMENTS ARE OLD! (USED FOR mean INSTEAD OF sum)
    We notice the differences among the boroughs in term of most passengers per slot (time of pickup)
    - Bronx: the average of passengers has a small peak at 13 (from 12 tp 15)
    - Brooklyn: the average is somehow stable, with a tiny peak at 7
    - EWR: the average of passengers varies per time, it has peaks at midnight, 4, and 12
    - Manhattan: the average is somehow stable with tiny increase from midnight until 4
    - Queens: the average is somehow stable
    - Staten Island: the average of passengers varies sharply, it has peaks at 1, 8, 13, 15, 23 and the top peak at 17 (we notice some missed data at 6)
    


# In[ ]:


'''
    The above Analysis was only for Jan 2018, in order to get the full image of the whole period provided,
    We need to do the same steps for each month and get the 
'''


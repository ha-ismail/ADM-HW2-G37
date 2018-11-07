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
rq1_data= yt_data[['tpep_pickup_datetime','PULocationID']].merge(zonesLookup[['LocationID','Borough']],how='inner', left_on='PULocationID', right_on='LocationID')

rq1_data


# In[2]:


#del yt_data

qr1 = rq1_data[['tpep_pickup_datetime','Borough']]
qr1


# In[3]:


from datetime import datetime
# Getting the day from the pickup time
qr1.iloc[:,0] = qr1.iloc[:,0].apply(lambda x: pd.to_datetime(x).day)
qr1


# In[12]:


qr1[['tpep_pickup_datetime','Borough']].groupby('tpep_pickup_datetime').size()


# In[15]:


fig, ax = plt.subplots(figsize=(15,7))
# Modify the x-axis to show numbers between 0-23
plt.xticks(list(range(32)))
qr1[['tpep_pickup_datetime','Borough']].groupby('tpep_pickup_datetime').size().plot(ax=ax,kind="line")


# In[ ]:


'''
    Visualizing the number of trips per day in Jan 2018 in NY, we notice:
    - the peak of number of trips is on 26, 19 and 12 (Fridays)
    - the lowest days in number of trips are generally Sun and Mon
    - (*) We notice a weird drop down on 4th Jan
    
'''


# In[16]:


# Group by day and Borough and calculate the number of trips for each day
qr1[['tpep_pickup_datetime','Borough']].groupby(['tpep_pickup_datetime','Borough'])['tpep_pickup_datetime'].size()


# In[17]:


fig, ax = plt.subplots(figsize=(15,7))
# Modify the x-axis to show numbers between 0-23
plt.xticks(list(range(32)))
qr1[['tpep_pickup_datetime','Borough']].groupby(['tpep_pickup_datetime','Borough'])['tpep_pickup_datetime'].size().unstack().plot(ax=ax)


# In[18]:


'''
    We notice that trips recorded in Manhattan during January are far more than any other borough
'''


# In[20]:


qr1_jan = qr1[['tpep_pickup_datetime','Borough']].groupby(['tpep_pickup_datetime','Borough'])['tpep_pickup_datetime'].size().unstack()
qr1_jan


# In[21]:


# Daily average of trips by Borough during Jan 2018
qr1_jan_average = qr1_jan.mean(axis=0)
qr1_jan_average


# In[ ]:


'''
    We need to calculate the same avaerage for each month, then combine and analyze
'''


# In[22]:


# read taxi data for Feb 2018
data='yellow_tripdata_2018-02.csv'
yt_data_2 = pd.read_csv(data)


# Merge the data with taxi zones table (taking only data we need for the QR#2)
rq1_data_2= yt_data_2[['tpep_pickup_datetime','PULocationID']].merge(zonesLookup[['LocationID','Borough']],how='inner', left_on='PULocationID', right_on='LocationID')

rq1_data_2


# In[23]:


qr1_2 = rq1_data_2[['tpep_pickup_datetime','Borough']]
qr1_2


# In[24]:


# Getting the day from the pickup time
qr1_2.iloc[:,0] = qr1_2.iloc[:,0].apply(lambda x: pd.to_datetime(x).day)
qr1_2


# In[26]:


# Group by day and Borough and calculate the number of trips for each day
qr1_feb = qr1_2[['tpep_pickup_datetime','Borough']].groupby(['tpep_pickup_datetime','Borough'])['tpep_pickup_datetime'].size().unstack()
qr1_feb_average = qr1_feb.mean(axis=0)
qr1_feb_average


# In[ ]:





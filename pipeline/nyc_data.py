#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm

year = 2019 
month = 10

pg_user = 'root'
pg_pass = 'root'
pg_host = 'localhost'
pg_db   = 'ny_taxi'
pg_port = 5432
# In[2]:


prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
url = f'{prefix}/yellow_tripdata_{year}-{month}.csv.gz'
url


# In[3]:


df = pd.read_csv(url)


# In[4]:


len(df)


# In[5]:


df.dtypes


# In[6]:


df.shape


# In[7]:


dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

df = pd.read_csv(
    url,
    nrows=100,
    dtype=dtype,
    parse_dates=parse_dates
)


# In[8]:


df.dtypes


# In[9]:


get_ipython().system('uv add sqlalchemy "psycopg[binary,pool]"')


# In[10]:



engine = create_engine('postgresql+psycopg://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')


# In[11]:


df.head(0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')


# In[12]:


print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))


# In[13]:


df_iter = pd.read_csv(
    url, 
    dtype = dtype, 
    parse_dates = parse_dates, 
    iterator = True, 
    chunksize = 100000,
)


# In[14]:


df = next(df_iter)


# In[15]:


df.head()


# In[16]:


get_ipython().system('uv add tqdm')


# In[17]:





# In[18]:


for df_chunk in tqdm(df_iter):
    df_chunk.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')


# In[ ]:





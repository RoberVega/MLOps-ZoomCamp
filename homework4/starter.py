
import pickle
import pandas as pd



with open('model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)

categorical = ['PULocationID', 'DOLocationID']

def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df





df = read_data('https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-02.parquet')


dicts = df[categorical].to_dict(orient='records')
X_val = dv.transform(dicts)
y_pred = model.predict(X_val)






df['ride_id'] = f'{2022:04d}/{2:02d}_' + df.index.astype('str')
df


# In[50]:


import numpy as np
df['ride_id'].shape
df_result = pd.DataFrame(df['ride_id'].values, columns=['ride_id'])
df_result['y_pred']=y_pred
df_result


# In[51]:


df_result.to_parquet(
    'predictions.parquet',
    engine='pyarrow',
    compression=None,
    index=False
)


# In[ ]:





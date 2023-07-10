import pandas as pd
from datetime import datetime
import batch 

def dt(hour, minute, second=0):
    return datetime(2022, 1, 1, hour, minute, second)


def test_prepare_data():
    
    data = [
        (None, None, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2), dt(1, 10)),
        (1, 2, dt(2, 2), dt(2, 3)),
        (None, 1, dt(1, 2, 0), dt(1, 2, 50)),
        (2, 3, dt(1, 2, 0), dt(1, 2, 59)),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),     
    ]

    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df = pd.DataFrame(data, columns=columns)

    categoricals = ['PULocationID', 'DOLocationID']

    actual_dict = batch.prepare_data(df, categoricals).to_dict()
    expected_dict = {'PULocationID': {0: '-1', 1: '1', 2: '1'},
                    'DOLocationID': {0: '-1', 1: '-1', 2: '2'},
                    'tpep_pickup_datetime': {0: dt(1, 2, 0),
                    1: dt(1, 2, 0),
                    2: dt(2, 2, 0)},
                    'tpep_dropoff_datetime': {0: dt(1, 10, 0),
                    1: dt(1, 10, 0),
                    2: dt(2, 3, 0)},
                    'duration': {0: 8.0, 1: 8.0, 2: 1.0}}
    
    assert actual_dict == expected_dict


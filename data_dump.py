import pymongo
import pandas as pd
import json

from sensor.config import mongo_client
#client = pymongo.MongoClient("mongodb://localhost:27017/neurolabDB")

database_name = 'aps_database'
collection_name = 'collection_name'
data_file_path = '/config/workspace/aps_failure_training_set1.csv'

if __name__=="__main__":
    df = pd.read_csv(data_file_path)
    print(f'rows and columns: {df.shape}')

    #convert the data frame to the json so that we can dump these records in to the mongo db

    df.reset_index(drop=True, inplace=True) # dropping the index given previously and resetting it
    json_record = list((json.loads(df.T.to_json()).values()))
    print(json_record[0])

    #insert the converted json record in to the mongo db 
    mongo_client[database_name][collection_name].insert_many(json_record)


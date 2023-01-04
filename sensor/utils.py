import pandas as pd
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.config import mongo_client
import sys, os
import yaml
import numpy as np
import dill

def get_collection_as_dataframe(database_name:str, collection_name:str)->pd.DataFrame:

    '''
    Description: This function return collection as dataframe 
    =========================================================
    Parameters are:
    data base name of str type
    collection name of str type
    ==========================================================
    this function returns the pandas dataframe and hence mentioned "->pd.DataFrame"
    '''

    try:
        logging.info(f"Reading data from database: {database_name} and collection:{collection_name}")
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        logging.info(f"Found columns:{df.columns}")

        if "_id" in df.columns:
            logging.info(f'Dropping the column: _id')
            df = df.drop("_id", axis = 1)
        logging.info(f'Rows and column in data frame: {df.shape}')
        return df

    except Exception as e:
        raise SensorException(e,sys)

#to save the report in to the yaml format    
def write_yaml_file(file_path, data:dict):
    try:
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir, exist_ok=True)
        with open(file_path, 'w') as file_writer:
            yaml.dump(data, file_writer)
    except Exception as e:
        raise SensorException(e, sys)
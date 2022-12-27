from sensor import utils
from sensor.entity import config_entity
from sensor.entity import artifact_entity
from sensor.exception import SensorException
from sensor.logger import logging
import os, sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


class data_ingestion:
    def __init__(self, data_ingestion_config:data_ingestion_config):
        try:
            logging.info(f"{'>>'*20} Data Ingestion {'<<'*20}")
            self.data_ingestion_config= data_ingestion_config
        except Exception as e:
            raise SensorException(e, sys)
            
    def initiate_data_ingestion(self)->artifact_entity.DataIngestionArtifact:
        try:
            loggin.info(f"Exporting collection data as pandas Dataframe")
            #Exporting collection data as pandas data frame
            df:pd.Dataframe = utils.get_collection_as_dataframe(database_name=self.data_ingestion_config.database_name , collection_name=self.data_ingestion_config.collection_name)
            
            logging.info("save data in the feature store")

            #replace na with NaN
            df.replace(to_replace='na', Value = np.NAN, inplace=True)

            #save data in the feature store
            logging.info("Create feature store folder if folder not available ")
            #create feature store folder if not available
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir, exist_ok=True)
            logging.info("Save df to feature store folder")
            #save df to feature store folder
            df.to_csv(path_or_buf= self.data_ingestion_config.feature_store_file_path, index=False, header= True)

            logging.info("Split the data set in to train and test")
            #split the data set into train and test set
            train_df, test_df = train_test_split(df,test_size=self.data_ingestion_config.test_size, random_state=42)

            logging.info("Create data set directory folder if not available ") 
            #create data set directory folder
            dataset_dir = os.path.dirname(self.data_ingestion_config.train_file_path) 
            os.makedirs(dataset_dir, exist_ok = True) 

            logging.info("Save df to feature store folder")
            #save data frame to feature store folder
            train_df.to_csv(path_or_buf=self.data_ingestion_config.train_file_path, index=False, header=True)
            test_df.to_csv(path_or_buf=self.data_ingestion_config.test_file_path, index=False, header=True)

            #Prepare the artifact

            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                feature_store_file_path = self.data_ingestion_config.feature_store_file_path, 
                train_file_path=self.data_ingestion_config.train_file_path,
                test_file_path=self.data_ingestion_config.test_file_path)

            logging.info(f"Data ingestion artifact:{data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise SensorException(error_message=e, error_detail=sys)
    




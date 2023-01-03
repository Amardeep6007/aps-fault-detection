from sensor.entity import artifact_entity,config_entity
from sensor.exception import SensorException
from sensor.logger import logging
from scipy.stats import ks_2samp
from typing import Optional # There is chance that the drop_missing_values_columns may return Null value and hence importing Optional from typing
import sys, os
import pandas as pd


class DataValidation:
    
    def __init__(self, data_validation_config:config_entity.DataIngestionConfig):
        try:
            logging.info(f'{">>"*20} Data Validation {"<<"*20}')
            self.data_validation_config = data_validation_config
        except Exception as e:
            raise SensorException(e, sys)

    

    def drop_missing_values_columns(self, df:pd.DataFrame, threshold:float=0.3)->Optional[pd.DataFrame]:
        """
        This funciton  will drop the column that contains missing values count more than specific threshold

        df: accept pandas data frame 
        threshold: percentage criteria to drop the column
        ================================================================================
        returns the pandas data frame if atleast one column is available after missing column drop else none
        """
        try:
            #selecting the column names which has null values
            null_report = df.isna().sum() / df.shape[0]
            drop_column_names = null_report[null_report > 0.3].index
            df.drop(list(drop_column_names), axis=1, inplace= True)

            if len(df.columns)>0:
                return None
            else:
                return df
        except Exception as e:
            raise SensorException(e, sys)

    def is_required_columns_exist(self,)->bool: #check whether all the column are present in the data set is present or not 
        try:
            pass
        except Exception as e:
            raise SensorException(e, sys)

    def __initiate_data_validation(self)->artifact_entity.DataValidationArtifact:
        pass

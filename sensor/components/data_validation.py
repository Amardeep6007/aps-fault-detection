from sensor.entity import artifact_entity,config_entity
from sensor.exception import SensorException
from sensor.logger import logging
from scipy.stats import ks_2samp
from typing import Optional # There is chance that the drop_missing_values_columns may return Null value and hence importing Optional from typing
import sys, os
import pandas as pd
from sensor import utils
import numpy as np 




class DataValidation:
    
    def __init__(self,
                     data_validation_config:config_entity.DataIngestionConfig,
                     data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f'{">>"*20} Data Validation {"<<"*20}')
            self.data_validation_config = data_validation_config
            self.validation_error = dict()
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise SensorException(e, sys)

    

    def drop_missing_values_columns(self, df:pd.DataFrame)->Optional[pd.DataFrame]:
        """
        This funciton  will drop the column that contains missing values count more than specific threshold

        df: accept pandas data frame 
        threshold: percentage criteria to drop the column
        ================================================================================
        returns the pandas data frame if atleast one column is available after missing column drop else none
        """
        try:
            threshold = self.data_validation_config.missing_threshold
            #selecting the column names which has null values
            null_report = df.isna().sum() / df.shape[0]
            drop_column_names = null_report[null_report > threshold].index
            self.validation_error["dropped column"] = drop_column_names
            df.drop(list(drop_column_names), axis=1, inplace= True)

            if len(df.columns)>0:
                return None
            else:
                return df
        except Exception as e:
            raise SensorException(e, sys)

    def is_required_columns_exist(self,base_df:pd.DataFrame, current_df:pd.DataFrame)->bool: #check whether all the column are present in the data set is present or not 
        try:
            base_columns = base_df.columns
            current_columns = current_df.columns

            missing_columns = []
            for base_column in base_columns:
                if base_column not in current_columns:
                    missing_columns.append(base_column)

            if len(missing_columns) > 0:
                self.validation_error["Missing Columns "] = missing_columns
                return False
            return True
            
        except Exception as e:
            raise SensorException(e, sys)
    
    def data_drift(self, base_df:pd.DataFrame, current_df:pd.DataFrame):
        try:
            drift_report = dict()


            base_columns = base_df.columns
            current_columns = current_df.columns

            for base_column in base_columns:
                base_data, current_data = base_df[base_column], current_df[base_column]
                #Null Hypothesis is that column from both the data set has same distribution
                same_distribution = ks_2samp(base_data, current_data)

                if same_distribution.pvalue > 0.05: 
                    #we are accepting the null hypothesis
                    drift_report[base_column] = {
                        "pvalues":same_distribution.pvalue,
                        "same_distribution": True
                    }
                    #same distribution

                else:
                    drift_report[base_column] = {
                        "pvalues":same_distribution.pvalue,
                        "same_distribution": False
                    }
                    #different distribution

        except Exception as e:
            raise SensorException(e, sys)

    def initiate_data_validation(self)->artifact_entity.DataValidationArtifact:
        try:
            base_df = pd.read_csv(self.data_validation_config.base_file_path)
            base_df.replace({"na":np.NAN}, inplace =True)
            #base data frame has NA as null 
            base_df = self.drop_missing_values_columns(df=base_df) 

        except Exception as e:
            raise SensorException(e, sys)

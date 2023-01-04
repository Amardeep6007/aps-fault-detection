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

    

    def drop_missing_values_columns(self, df:pd.DataFrame, report_key_name:str)->Optional[pd.DataFrame]:
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
            logging.info(f"selecting the column names which has null values count above to {threshold}")
            drop_column_names = null_report[null_report > threshold].index

            logging.info(f"column to drop: {drop_column_names}")

            self.validation_error[report_key_name] = drop_column_names
            df.drop(list(drop_column_names), axis=1, inplace= True)

            if len(df.columns)>0:
                return None
            else:
                return df
        except Exception as e:
            raise SensorException(e, sys)

    def is_required_columns_exist(self,base_df:pd.DataFrame, current_df:pd.DataFrame, report_key_name:str)->bool: #check whether all the column are present in the data set is present or not 
        try:
            base_columns = base_df.columns
            current_columns = current_df.columns

            missing_columns = []
            for base_column in base_columns:
                if base_column not in current_columns:
                    logging.info(f"column:[{base} is not available] ")
                    missing_columns.append(base_column)

            if len(missing_columns) > 0:
                self.validation_error[report_key_name] = missing_columns
                return False
            return True
            
        except Exception as e:
            raise SensorException(e, sys)
    
    def data_drift(self, base_df:pd.DataFrame, current_df:pd.DataFrame, report_key_name:str):
        try:
            drift_report = dict()


            base_columns = base_df.columns
            current_columns = current_df.columns

            for base_column in base_columns:
                base_data, current_data = base_df[base_column], current_df[base_column]
                #Null Hypothesis is that column from both the data set has same distribution
                logging.info(f"Hypothesis {base_column}: {base_data.dtype}, {current_data.dtype} ")
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
            self.validation_error[report_key_name] =drift_report    
        except Exception as e:
            raise SensorException(e, sys)

    def initiate_data_validation(self)->artifact_entity.DataValidationArtifact:
        try:
            logging.info(f"reading the base data frame")
            base_df = pd.read_csv(self.data_validation_config.base_file_path)
            base_df.replace({"na":np.NAN}, inplace =True)
            logging.info(f"Repalce the na values in base df")
            #base data frame has NA as null 
            logging.info(f"Drop null value column from base data frame")
            base_df = self.drop_missing_values_columns(df=base_df, report_key_name="missing_values_within_base_dataset") 

            logging.info("Reading the train data frame")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            logging.info("Reading the test data frame")
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            logging.info("Drop the null values from the train data frame")
            train_df = self.drop_missing_values_columns(df= train_df, report_key_name="missing_values_within_train_dataset")
            logging.info("Drop the null value from the test data frame ")
            test_df = self.drop_missing_values_columns(df= test_df, report_key_name="missing_values_within_test_dataset")

            exclude_columns=['class']
            base_df= utils.convert_columns_to_float(df=base_df, exclude_columns=exclude_columns)
            train_df= utils.convert_columns_to_float(df=train_df, exclude_columns=exclude_columns)
            test_df= utils.convert_columns_to_float(df=test_df, exclude_columns=exclude_columns)

            logging.info("Is all required column is present in train data frame")
            train_df_column_status = self.is_required_columns_exist(base_df=base_df, current_df=train_df, report_key_name="missing_columns_within_train_dataset")
            logging.info("Is all required column is present in test data frame")
            test_df_column_status = self.is_required_columns_exist(base_df=base_df, current_df=test_df, report_key_name="missing_columns_within_test_dataset")

            if train_df_column_status is True:
                logging.info("As all the column are available in train df, hence detecting the data drift in the train data frame")
                self.data_drift(base_df =base_df, current_df=train_df, report_key_name="data_drift_within_train_dataset")
            if test_df_column_status is True:
                logging.info("As all the column are available in test df , hence detecting the data drift in the test data frame")
                self.data_drift(base_df=base_df, current_df=test_df, report_key_name="data_drift_within_test_dataset")

            #write the report
            logging.info("Writing report in yaml file ")
            utils.write_yaml_file(file_path = self.data_validation_config.report_file_path, data=self.validation_error)
            
            data_validation_artifact = artifact_entity.DataValidationArtifact(report_file_path=self.data_validation_config.report_file_path)
            logging.info(f"Data Validation artifact :{data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise SensorException(e, sys)

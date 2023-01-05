from sensor import utils
from sensor.entity import artifact_entity, config_entity
from sensor.exception import SensorException
from sensor.logger import logging
from sklearn.preprocessing import Pipeline, LabelEncoder

from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler

import pandas as pd 
import numpy as np 
import os, sys


class DataTransformation:
    def __init__(self,data_transformation_config:config_entity.DataTransformationConfig, 
                      data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact

        except Exception as e:
            raise SensorException(e, sys)    

    @classmethod # we created class method decorator because we wanted to make this below method avilable to all the object of the class 
    def get_data_transformer_object(cls)->Pipeline:
        try:
            simple_imputer = SimpleImputer(strategy = "constant", fill_value = 0) #simple imputer will impute the missing values in the data set
            robust_scaler = RobustScaler() #robustscaler will handler the outliers 

            pipeline = Pipeline(steps=[
                ('Imputer', simple_imputer),
                ('RobustScaler', robust_scaler)
            ])
            return pipeline
        except Exception as e:
            raise SensorException(e, sys)

    def initiate_data_transformation(self, )->artifact_entity.DataTransformationArtifact:
        try:
            #reading the training and testing file
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df =pd.read_csv(self.data_ingestion_artifact.test_file_path)

            #selecting the input feature for train and test data frame 
            input_feature_train_df = train_df.drop(TARGET_COLUMN, axis=1)
            input_feature_test_df = test_df.drop(TARGET_COLUMN,axis=1)
                
            #selecting the target feature for train and test data frame    
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_test_df = test_df[TARGET_COLUMN]

            label_encoder = LabelEncoder()
            label_encoder.fit(target_feature_train_df)

            #transformation on target column
            target_feature_train_array = label_encoder.transform(target_feature_train_df)
            target_feature_test_array = label_encoder.transform(target_feature_test_df)

            transformation_pipeline = DataTransformation.get_data_transformer_object()
            transformation_pipeline.fit(input_feature_train_df)

            #transformation input feature
            input_feature_train_array = transformation_pipeline.transform(input_feature_train_df)
            input_feature_test_array =  transformation_pipeline.transform(input_feature_test_df)

            
            


        except Exception as e:
            raise SensorException(e, sys)


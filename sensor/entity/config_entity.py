from sensor.logger import logging
from sensor.exception import SensorException
from datetime import datetime
import os, sys


FILE_NAME = 'sensor.csv'
TRAIN_FILE_NAME= 'train.csv'
TEST_FILE_NAME = 'test.csv'
TRANSFORMER_OBJECT_FILE_NAME = 'transfomer.pkl'
TARGET_ENCODER_OBJECT_FILE_NAME = 'target_encoder.pkl'
MODEL_FILE_NAME = "model.pkl"



class Training_PipelineConfig:
    def __init__(self):
        try:
            self.artifact_dir = os.path.join(os.getcwd(), "artifact",f"{datetime.now().strftime('%m%d%Y_%H%M%S')}")
        except Exception as e:
            raise SensorException(e, sys)

class DataIngestionConfig:
    def __init__(self, training_PipelineConfig:Training_PipelineConfig):
        try:
            self.database_name = 'aps_database'
            self.collection_name = 'collection_name'
            self.data_ingestion_dir = os.path.join(training_PipelineConfig.artifact_dir, 'data_ingestion')
            self.feature_store_file_path = os.path.join(self.data_ingestion_dir, 'feature_Store', FILE_NAME)
            self.train_file_path = os.path.join(self.data_ingestion_dir, 'dataset', TRAIN_FILE_NAME)
            self.test_file_path = os.path.join(self.data_ingestion_dir, 'dataset', TEST_FILE_NAME)
            self.test_size = 0.2
        except Exception as e:
            raise SensorException(e, sys)

    def to_dict(self,)->dict:
        try:
            return self.__dict__
        except Exception as e:
            raise SensorException(e, sys)

class DataValidationConfig:

    def __init__(self, training_PipelineConfig=Training_PipelineConfig()):
        self.data_validation_dir = os.path.join(training_PipelineConfig.artifact_dir, "data_validation")
        self.report_file_path = os.path.join(self.data_validation_dir, "report.yaml")
        self.missing_threshold:float = 0.20
        self.base_file_path = os.path.join("aps_failure_training_set1.csv")



class DataTransformationConfig:

    def __init__(self, training_PipelineConfig = Training_PipelineConfig()):
        self.data_transformation_dir = os.path.join(training_PipelineConfig.artifact_dir, "data_transformation")
        self.transform_object_path = os.path.join(self.data_transformation_dir, "transformer", TRANSFORMER_OBJECT_FILE_NAME)   
        self.transformed_train_path = os.path.join(self.data_transformation_dir, "transformed", TRAIN_FILE_NAME.replace("csv", "npz"))
        self.transformed_test_path = os.path.join(self.data_transformation_dir, "transformed", TEST_FILE_NAME.replace("csv", "npz"))
        self.target_encoder_path = os.path.join(self.data_transformation_dir, "target_encoder", TARGET_ENCODER_OBJECT_FILE_NAME) #here we are doing label encoding for the target column , i.e for pos = 1 and neg =0 


class ModelTrainerConfig:
    def __init__(self, training_PipelineConfig:Training_PipelineConfig):
        self.model_trainer_dir = os.path.join(training_PipelineConfig.artifact_dir, "model_trainer")
        self.model_path = os.path.join(self.model_trainer_dir, "model", MODEL_FILE_NAME)
        self.expected_score = 0.70
        self.overfitting_threshold = 0.10


class ModelEvaluationConfig:
    def __init__(self, training_PipelineConfig :Training_PipelineConfig):
        self.change_threshold = 0.01 #if my trained model is going to perform better by 1 percent (0.1) then we can accept the newly trained model
        
class ModelPusherConfig:
    def __init__(self, training_PipelineConfig:Training_PipelineConfig):
        self.model_pusher_dir = os.path.join(training_PipelineConfig.artifact_dir, "model_pusher")
        self.push_model_dir = os.path.join("saved_models") #here we are creating the saved_models folder outside of the artifact dir
        self.pusher_model_dir = os.path.join(self.push_model_dir, "saved_models") #we also want to store the saved_models folder in the model_pusher folder under the artifact directory in each run of the program/code
        
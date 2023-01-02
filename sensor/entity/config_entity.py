from sensor.logger import logging
from sensor.exception import SensorException
from datetime import datetime
import os, sys


FILE_NAME = 'sensor.csv'
TRAIN_FILE_NAME= 'train.csv'
TEST_FILE_NAME = 'test.csv'

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
class DataValidationConfig:...
class DataTransformationConfig:...
class ModelTrainerConfig:...
class ModelEvaluationConfig:...
class ModelPusherConfig:...
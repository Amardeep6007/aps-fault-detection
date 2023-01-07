from sensor.predictor import ModelResolver
from sensor.entity import config_entity, artifact_entity
from sensor.exception import SensorException
from sensor.logger import logging
import os, sys
import pandas as pd 
from sensor.config import TARGET_COLUMN
from sensor.utils import load_object
from sklearn.metrics import f1_score

class ModelEvaluation:
    def __init__(self, data_ingestion_artifact:artifact_entity.DataIngestionArtifact,
                        model_eval_config:config_entity.ModelEvaluationConfig,
                        data_transformation_artifact:artifact_entity.DataTransformationArtifact,
                        model_trainer_artifact:artifact_entity.ModelTrainerArtifact):
        
        try:
            logging.info(f'{'>>'*20} Model Evaluation {'<<'*20}')
            self.model_eval_config= model_eval_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact = model_trainer_artifact
            
            self.model_resolver = ModelResolver()
        except Exception as e:
            raise SensorException(e, sys)
        
    def initiate_model_evaluation()->artifact_entity.ModelEvaluationArtifact:
        try:
            #if saved_models folder has model present in it then we will comapare which model is best ,
            # i.e currently trained model or model that is currently present in the production(model from the saved_models folder)

        except Exception as e:
            raise SensorException(e, sys)

#from sensor.logger import logging
#from sensor.exception import SensorException
#import sys, os

#def test_loggingAndException():
#     try:
#          logging.info("starting the test_loggingAndException")
#          res = 3/0
#          print(res)
#          logging.info("Stopping the test_loggingAndException")
#     except Exception as e:
#          logging.debug("Stopping the test_loggingAndException")
#          raise SensorException(e, sys)

#if __name__=="__main__":
#     try:
#          test_loggingAndException()
#     except Exception as e:
#          print(e)


#from sensor.utils import get_collection_as_dataframe
#import sys, os


#if __name__=='__main__':
#     try:
#          get_collection_as_dataframe(database_name = "aps_database", collection_name="collection_name")
#     except Exception as e:
#          print(e)

from sensor.logger import logging
from sensor.exception import SensorException
from sensor.utils import get_collection_as_dataframe
import sys, os
from sensor.entity.config_entity import DataIngestionConfig
from sensor.entity import config_entity
from sensor.components import data_ingestion
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
from sensor.components.model_trainer import ModelTrainer
import numpy as np
from sensor.components.model_evaluation import ModelEvaluation


if __name__=='__main__':
     try:
          training_PipelineConfig = config_entity.Training_PipelineConfig()
          #data Ingestion
          data_ingestion_config = config_entity.DataIngestionConfig(training_PipelineConfig=training_PipelineConfig)
          print(data_ingestion_config.to_dict())

          data_ingestion = DataIngestion(data_ingestion_config =data_ingestion_config)
          data_ingestion_artifact=data_ingestion.initiate_data_ingestion()


          #data Validation
          data_validation_config = config_entity.DataValidationConfig(training_PipelineConfig=training_PipelineConfig)
          data_validation = DataValidation(data_validation_config=data_validation_config, 
                         data_ingestion_artifact=data_ingestion_artifact)
          data_validation_artifact = data_validation.initiate_data_validation()
     

          #data Transformation
          data_transformation_config = config_entity.DataTransformationConfig(training_PipelineConfig=training_PipelineConfig)
          data_transformation = DataTransformation(data_transformation_config=data_transformation_config, 
                                                  data_ingestion_artifact=data_ingestion_artifact)
          data_transformation_artifact = data_transformation.initiate_data_transformation()     

          #model trainer
          model_trainer_config = config_entity.ModelTrainerConfig(training_PipelineConfig=training_PipelineConfig)
          model_trainer = ModelTrainer(model_trainer_config=model_trainer_config ,
                          data_transformation_artifact=data_transformation_artifact)
          model_trainer_artifact = model_trainer.initiate_model_trainer()

          #model Evaluation
          model_eval_config = config_entity.ModelEvaluationConfig(training_PipelineConfig= training_PipelineConfig)
          model_eval = ModelEvaluation(data_ingestion_artifact = data_ingestion_artifact, 
                                        model_eval_config = model_eval_config,
                                        data_transformation_artifact = data_transformation_artifact,
                                        model_trainer_artifact = model_trainer_artifact)
          model_eval_artifact = model_eval.initiate_model_evaluation()     
     except Exception as e:
          print(e)
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

if __name__=='__main__':
     try:
          training_PipelineConfig = config_entity.Training_PipelineConfig()
          data_ingestion_config = config_entity.DataIngestionConfig(training_PipelineConfig=training_PipelineConfig)
          print(data_ingestion_config.to_dict())

          data_ingestion = DataIngestion(data_ingestion_config =data_ingestion_config)
          data_ingestion_artifact=data_ingestion.initiate_data_ingestion()


          data_validation_config = config_entity.DataValidationConfig(training_PipelineConfig=training_PipelineConfig)
          data_validation = DataValidation(data_validation_config=data_validation_config, 
                         data_ingestion_artifact=data_ingestion_artifact)
          data_validation_artifact = data_validation.initiate_data_validation()
     

     except Exception as e:
          print(e)
from sensor.predictor import ModelResolver
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.entity.config_entity import ModelPusherConfig
from sensor.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact, ModelPusherArtifact
from sensor.utils import load_object, save_object
import os,sys



class ModelPusher:
    def __init__(self, model_pusher_config:ModelPusherConfig,
                        data_transformation_artifact:DataTransformationArtifact,
                        model_trainer_artifact:ModelTrainerArtifact):
        try:
            pass
        except Exception as e:
            raise SensorException(e, sys)
    
    def initiate_model_pusher(self,)->ModelPusherArtifact:
        try:
            #load all the objects

            #save in model pusher dir

            #save in saved_models dir
        

        except Exception as e:
            raise SensorException(e, sys)

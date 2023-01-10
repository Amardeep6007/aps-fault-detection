from sensor.predictor import ModelResolver
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.entity.config_entity import ModelPusherConfig, ModelEvaluationConfig
from sensor.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact, ModelPusherArtifact, ModelEvaluationArtifact
from sensor.utils import load_object, save_object
import os,sys




class ModelPusher:
    def __init__(self, model_pusher_config:ModelPusherConfig,
                        data_transformation_artifact:DataTransformationArtifact,
                        model_trainer_artifact:ModelTrainerArtifact):
        try:
            logging.info(f"{'>>'*20} Model Pusher {'<<'*20}")
            self.model_pusher_config=model_pusher_config
            self.data_transformation_artifact=data_transformation_artifact
            self.model_trainer_artifact=model_trainer_artifact
            self.model_resolver = ModelResolver(model_registry=self.model_pusher_config.saved_model_dir)
        
        except Exception as e:
            raise SensorException(e, sys)
    
    def initiate_model_pusher(self,)->ModelPusherArtifact:
        try:
            #load all the objects
            logging.info(f"Loading transformer ,model and target encoder")
            transformer = load_object(file_path=self.data_transformation_artifact.transform_object_path) #loading the transformer.pkl file
            model = load_object(file_path=self.model_trainer_artifact.model_path) #loading the model.pkl file
            target_encoder = load_object(file_path=self.data_transformation_artifact.target_encoder_path) #loading the target_encoder.pkl file

            #save in model pusher dir inside of the artifact folder
            logging.info(f"saving the model to model pusher dir")
            save_object(file_path=self.model_pusher_config.pusher_transformer_path, obj=transformer)
            save_object(file_path=self.model_pusher_config.pusher_target_encoder_path , obj=target_encoder)
            save_object(file_path=self.model_pusher_config.pusher_model_path, obj=model)

            #save in saved_models dir outside of artifact folder
            logging.info(f"Saving the model to saved_models dir")
            transformer_path = self.model_resolver.get_latest_save_transformer_path()
            model_path = self.model_resolver.get_latest_save_model_path()
            target_encoder_path = self.model_resolver.get_latest_save_target_encoder_path()

            save_object(file_path= transformer_path, obj = transformer)
            save_object(file_path=model_path, obj=model)
            save_object(file_path=target_encoder_path, obj=target_encoder)

            model_pusher_artifact = ModelPusherArtifact(pusher_model_dir =self.model_pusher_config.pusher_model_dir,
                                saved_model_dir=self.model_pusher_config.saved_model_dir)
            logging.info(f"Model Pusher artifact:{model_pusher_artifact}")
            return model_pusher_artifact
        except Exception as e:
            raise SensorException(e, sys)

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
            logging.info(f"{'>>'*20} Model Evaluation {'<<'*20}")
            self.model_eval_config= model_eval_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact = model_trainer_artifact
            self.model_resolver = ModelResolver()
        except Exception as e:  
            raise SensorException(e, sys)
        
    def initiate_model_evaluation(self)->artifact_entity.ModelEvaluationArtifact:
        try:
            #if saved_models folder has model present in it then we will comapare which model is best ,
            # i.e currently trained model or model that is currently present in the production(model from the saved_models folder)

            logging.info("if saved model folder has model then we will compare "
            "which model is best trained or the model from saved model folder")
            latest_dir_path = self.model_resolver.get_latest_dir_path()
            if latest_dir_path==None:
                model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,
                                                                              improved_accuracy=None)
                logging.info(f"Model evaluation artifact: {model_eval_artifact}")
                return model_eval_artifact   

            #finding the location of transformer, model, and target encoder path
            logging.info(f"finding the location of transformer, model, and target encoder path")
            model_path = self.model_resolver.get_latest_save_model_path()
            transformer_path = self.model_resolver.get_latest_transformer_path()
            target_encoder_path = self.model_resolver.get_latest_transformer_path()

            #loading the previouly trained transformer, target_encoder, model object
            logging.info(f"loading the previouly trained transformer, target_encoder, model object")
            transformer = load_object(file_path=transformer_path) #getting the previously transformer.pkl file here
            target_encoder = load_object(file_path=target_encoder_path) #getting the previously target_encoder.pkl file here
            model = load_object(file_path=model_path) #getting the previously trained model.pkl file here

            #loading the currently tranined transformer, target_encoder, model objects
            logging.info(f"loading the currently tranined transformer, target_encoder, model objects")
            current_transformer = load_object(file_path=self.data_transformation_artifact.transform_object_path) #getting the currently trained transformer.pkl file 
            current_target_encoder= load_object(file_path=self.data_transformation_artifact.target_encoder_path) #getting the currently trained target_encoder.pkl file
            current_model = load_object(file_path=self.model_trainer_artifact.model_path) #gettting the currently trained model.pkl file

            #now we need to compare both currently trained model and previously trained model based on the accuracy score    
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path) 
            target_df = test_df[TARGET_COLUMN] #selecting the target column from the test data frame
            y_true = target_encoder.transform(target_df)

            #accuracy using previously trained model
            logging.info(f"finding the accuracy using previously trained model")
            input_arr = transformer.transform(test_df)
            y_pred = model.predict(input_arr)
            print(f'Prediction using the previously trained model: {target_encoder.inverse_transform(y_pred[:5])}')
            previous_model_score = f1_score(y_true=y_true, y_pred=y_pred)#calculating the f1_score for previoiusly trained model
            logging.info(f"accuracy using previously trained model is : {previous_model_score}")

            #accuracy using currently trained model.
            logging.info(f"Finding the accuracy using currently trained model")
            input_arr = current_transformer.transform(test_df) #transforming the test data frame using the currently trained transformer.pkl file
            y_pred = current_model.predict(input_arr) #prediction using the currently trained model.pkl file
            y_true = current_target_encoder.transform(target_df) #transforming the target column using the currently trained target_encoder.pkl file
            print(f'Prediction using currently trained model: {current_target_encoder.inverse_transform()} ')
            current_model_score = f1_score(y_true=y_true, y_pred=y_pred) #calculating the f1_score for currently trained model
            logging.info(f"accuracy using currently trained model is : {current_model_score}")

            if current_model_score < previous_model_score:
                logging.info(f"Current trained model is not better than previously trained model(i.e currently deployed model)")
                raise Exception(f"Current trained model is not better than previously trained model(i.e currently deployed model)")
            model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted = True,
                                                    improved_accuracy = (current_model_score - previous_model_score)) #here comparison is getting done
            
            logging.info(f"Model Evaluation artifact i.e model is evaluated with {improved_accuracy} improved accuracy ")
            return model_eval_artifact
        except Exception as e:
            raise SensorException(e, sys)

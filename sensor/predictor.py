#the task of this file is to read the latest model from the saved_models folder and make the predictions
#the place where we save the model is called as model registry
#from the saved_models folder (ideally the model registry) we need to pick the latest model folder

import os
from sensor.entity.config_entity import TRANSFORMER_OBJECT_FILE_NAME, MODEL_FILE_NAME, TARGET_ENCODER_OBJECT_FILE_NAME
from glob import glob # this will return all the files that we have inside the folder


#the below class helps us to get the location of , saved_models path and inside this latest model, transformer and target_encoder folder
class ModelResolver:

    def __init__(self, model_registry:str = 'saved_models', 
                        transformer_dir_name= 'transformer',
                        target_encoder_dir_name= 'target_encoder',
                        model_dir_name= 'model'):
        self.model_registry = model_registry
        self.transformer_model_dir = transformer_dir_name
        self.target_encoder_dir_name = target_encoder_dir_name
        self.model_dir_name = model_dir_name

    #steps on how the below function works
    #steps to get the latest dir/folder path:
    #step1: from a particular folder extract all the folder 
    #step2: now pick the latest model, i.e model that has the highest number mentioned as the folder name and first convert the name of the folder from string to integer
    def get_latest_dir_path(self): #fetch the latest folder name 
        try:
            dir_names = os.listdir(self.model_registry) #extract all the file name 
            dir_names = list(map(int, dir_names)) #convert the names from string to integer
            latest_folder_name = max(dir_names) #highest integer is the latest folder as newest model will get the highest number folder 
            return os.path.join(self.model_registry, f'{latest_folder_name}')
        except Exception as e:
            raise e

    def get_latest_model_path(): # from the latest folder name fetch the latest model path
        try:
            latest_dir = self.get_latest_dir_path()
            return os.path.join(latest_dir, self.model_dir_name, MODEL_FILE_NAME)
        except Exception as e:
            raise e
    def get_latest_transformer_path(): #from the latest folder name fetch the latest transformer path
        try:
            latest_dir = self.get_latest_dir_path()
            return os.path.join(latest_dir,self.transformer_dir_name, TRANSFORMER_OBJECT_FILE_NAME)

        except Exception as e:
            raise e
    def get_latest_target_encoder_path(): #from the latest folder name fetch the latest target encoder path
        try:
            latest_dir = self.get_latest_dir_path()
            return os.path.join(latest_dir, self.target_encoder_dir_name, TARGET_ENCODER_OBJECT_FILE_NAME)

        except Exception as e:
            raise e
        
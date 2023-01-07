#the task of this file is to read the latest model from the saved_models folder and make the predictions
#the place where we save the model is called as model registry
#from the saved_models folder (ideally the model registry) we need to pick the latest model folder

import os
from sensor.entity.config_entity import TRANSFORMER_OBJECT_FILE_NAME, MODEL_FILE_NAME, TARGET_ENCODER_OBJECT_FILE_NAME

class ModelResolver:

    def __init__(self, model_registry:str = 'saved_models'):
        self.model_registry = model_registry

    #steps on how the below function works
    #steps to get the latest dir/folder path:
    #step1: from a particular folder extract all the folder 
    #step2: now pick the latest model, i.e model that has the highest number mentioned as the folder name and first convert the name of the folder from string to integer
    def get_latest_dir_path(self):
        try:
            dir_names = os.listdir(self.model_registry) #extract all the file name 
            dir_names = list(map(int, dir_names)) #convert the names from string to integer
            latest_folder_name = max(dir_names) #highest integer is the latest folder
            return os.path.join(self.model_registry, f'{latest_folder_name}')
        except Exception as e:
            raise e

    def get_latest_model_path():
        pass
    def get_latest_transformer_path():...
    def get_latest_target_encoder_path():...
        
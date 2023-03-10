from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    feature_store_file_path:str
    train_file_path:str
    test_file_path:str

@dataclass    
class DataValidationArtifact:
    report_file_path:str
    
@dataclass    
class DataTransformationArtifact:
    transform_object_path:str
    transformed_train_path:str
    transformed_test_path:str
    target_encoder_path:str

""" @dataclass
class ClassifiactionMetricArtifact:
    f1_score:float
    precision_score:float
    recall_score:float  """

@dataclass    
class ModelTrainerArtifact:
    model_path:str 
    f1_train_score:float 
    f1_test_score:float
    
@dataclass
class ModelEvaluationArtifact:
    is_model_accepted:bool 
    improved_accuracy:float 
    #best_model_path:str 
    #trained_model_path:str 
    #trained_model_metric_artifact: ClassifiactionMetricArtifact 
    #best_model_metric_artifact: ClassifiactionMetricArtifact
        
@dataclass    
class ModelPusherArtifact:
    pusher_model_dir:str 
    saved_model_dir:str 
    

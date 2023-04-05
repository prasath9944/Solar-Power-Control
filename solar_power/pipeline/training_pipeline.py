from solar_power.components.data_ingestion import DataIngestion
from solar_power.components.data_validation import DataValidation
from solar_power.components.data_transformation import DataTransformation
from solar_power.components.model_pusher import ModelPusher
from solar_power.components.model_evaluation import ModelEvaluation
from solar_power.components.model_trainer import ModelTrainer
from solar_power.entity import config_entity
from solar_power.exception import SolarException
from solar_power.entity import artifact_entity 
from solar_power.logger import logging
import os,sys

def start_training_pipeline()->bool:
    try:
        training_pipeline_config = config_entity.TrainingPipelineConfig()
        #data ingestion
        logging.info(f"Started the Data Ingestion Componenet")
        data_ingestion_config  = config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()  
        print(data_ingestion_artifact)
        
        # Data Validation
        logging.info(f"Started the Data Validation Componenet")
        data_validation_config=config_entity.DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_validation=DataValidation(data_validation_config=data_validation_config,data_ingestion_artifact=data_ingestion_artifact)
        data_validation_artifact=data_validation.initiate_data_validation()
        
        # Data Transformation
        logging.info(f"Started the Data Transformation Componenet")
        data_transformation_config=config_entity.DataTransformationConfig(training_pipeline_config=training_pipeline_config)
        data_transformation=DataTransformation(data_transformation_config=data_transformation_config,data_ingestion_artifact=data_ingestion_artifact)
        data_transformation_artifact=data_transformation.initiate_data_transformation()
        
        #Model Trainer
        logging.info(f"Started the Model Trainer Componenet")
        model_trainer_config=config_entity.ModelTrainerConfig(training_pipeline_config=training_pipeline_config)
        model_trainer=ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact=model_trainer.initiate_model_trainer()
        
        # Model Evaluation
        logging.info(f"Started the Model Evaluation Componenet")
        model_evaluation_config=config_entity.ModelEvaluationConfig(training_pipeline_config=training_pipeline_config)
        model_evaluation=ModelEvaluation(model_eval_config=model_evaluation_config,data_ingestion_artifact=data_ingestion_artifact,data_transformation_artifact=data_transformation_artifact,model_trainer_artifact=model_trainer_artifact)
        model_evaluation_artifact=model_evaluation.initiate_model_evaluation()
        
        # Model Pusher
        logging.info(f"Started the Model Pusher Componenet")
        model_pusher_config=config_entity.ModelPusherConfig(training_pipeline_config=training_pipeline_config)
        model_pusher=ModelPusher(model_pusher_config=model_pusher_config,data_transformation_artifact=data_transformation_artifact,model_trainer_artifact=model_trainer_artifact)
        model_pusher_artifact=model_pusher.initiate_model_pusher()
        
        return True
    except Exception as e:
        raise SolarException(e,sys)

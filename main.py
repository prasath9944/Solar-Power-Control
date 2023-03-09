from solar_power.components.data_ingestion import DataIngestion
from solar_power.entity import config_entity
from solar_power.exception import SolarException
from solar_power.entity import artifact_entity 
import os,sys

if __name__=="__main__":
    training_pipeline_config = config_entity.TrainingPipelineConfig()
    #data ingestion
    data_ingestion_config  = config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
    data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
    data_ingestion_artifact = data_ingestion.initiate_data_ingestion()  
    print(data_ingestion_artifact)

import os,sys
from solar_power.logger import logging
from solar_power.exception import SolarException
from datetime import datetime


FILE_NAME = "solar.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"

class TrainingPipelineConfig:
    def __init__(self) -> None:
        try:
            self.artifact_dir=os.path.join(os.getcwd(),"artifact",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}")
        except Exception as e:
            raise SolarException(e,sys)
        
        
class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig) -> None:
        try:
            self.database_name="solar"
            self.collection_name="solarpower"
            self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir , "data_ingestion")
            self.feature_store_file_path = os.path.join(self.data_ingestion_dir,"feature_store",FILE_NAME)
            self.train_file_path = os.path.join(self.data_ingestion_dir,"dataset",TRAIN_FILE_NAME)
            self.test_file_path = os.path.join(self.data_ingestion_dir,"dataset",TEST_FILE_NAME)
            self.test_size = 0.2
            
        except Exception as e:
            raise SolarException(e,sys)
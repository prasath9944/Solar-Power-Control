from solar_power.entity import artifact_entity,config_entity
from solar_power.exception import SolarException
from solar_power.logger import logging
from typing import Optional
import os,sys 
from sklearn.pipeline import Pipeline
import pandas as pd
from solar_power import utils
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from solar_power.config import TARGET_COLUMN



class DataTransformation:


    def __init__(self,data_transformation_config:config_entity.DataTransformationConfig,
                    data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20} Data Transformation {'<<'*20}")
            self.data_transformation_config=data_transformation_config
            self.data_ingestion_artifact=data_ingestion_artifact
        except Exception as e:
            raise SolarException(e, sys)


    @classmethod
    def get_data_transformer_object(cls)->Pipeline:
        try:
            
            
            logging.info(f"Simple Imputer with Constant strategy")
            simple_imputer = SimpleImputer(strategy='constant', fill_value=0)
            standard_scaler =  StandardScaler()
            pipeline = Pipeline(steps=[
                    ('Imputer',simple_imputer),
                    ('StandardScaler',standard_scaler)
                ])
            logging.info(f"Pipeline consists of Imputer and robust scalar: {pipeline}")
            return pipeline
        except Exception as e:
            raise SolarException(e, sys)


    def initiate_data_transformation(self,) -> artifact_entity.DataTransformationArtifact:
        try:
            logging.info("reading training and testing file")
            #reading training and testing file
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            
            logging.info(f"selecting input feature for train and test dataframe")
            #selecting input feature for train and test dataframe
            input_feature_train_df=train_df.drop(TARGET_COLUMN,axis=1)
            input_feature_test_df=test_df.drop(TARGET_COLUMN,axis=1)
            
            boolean_feature=[i for i in input_feature_train_df.columns if input_feature_train_df[i].dtype=='bool']

            logging.info(f"Converting the boolean feature into numerical features in train and test dataframe")
            input_feature_train_df=utils.convert_boolean_toNumerical(df=input_feature_train_df,boolean_features=boolean_feature)
            input_feature_test_df=utils.convert_boolean_toNumerical(df=input_feature_test_df,boolean_features=boolean_feature)
            
            
            logging.info(f"selecting target feature for train and test dataframe")
            #selecting target feature for train and test dataframe
            logging.info("selecting target feature for train and test dataframe")
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_test_df = test_df[TARGET_COLUMN]

            #transformation on target columns
            logging.info(f"transformation on target columns")

            target_feature_train_arr=np.array(target_feature_train_df)
            target_feature_test_arr=np.array(target_feature_test_df)
            logging.info(f"Transformation object")
            transformation_pipleine = DataTransformation.get_data_transformer_object()
            transformation_pipleine.fit(input_feature_train_df)

            #transforming input features
            logging.info(f"transforming input features")
            input_feature_train_arr = transformation_pipleine.transform(input_feature_train_df)
            logging.info(f"Transformed the input_train_arr")
            input_feature_test_arr = transformation_pipleine.transform(input_feature_test_df)
            logging.info(f"Transformed the input_test_arr")

            logging.info(f"target_feature_train_arr shape: {target_feature_train_arr.shape}")
            logging.info(f"target_feature_test_arr shape: {target_feature_test_arr.shape}")
            logging.info(f"Transformed the input_train_arr and input_test_arr")


            #target encoder
            logging.info(f"target encoder")
            train_arr = np.c_[input_feature_train_arr, target_feature_train_arr ]
            test_arr = np.c_[input_feature_test_arr, target_feature_test_arr]

            logging.info(f"train arr : {train_arr[1]}")
            logging.info(f"test arr : {test_arr[1]}")
            #save numpy array
            logging.info(f"save transformed train array")
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_path,
                                        array=train_arr)

            logging.info(f"saving the transformed test array")
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_path,
                                        array=test_arr)

            logging.info(f"saving the transformer object")
            utils.save_object(file_path=self.data_transformation_config.transform_object_path,
             obj=transformation_pipleine)

             


            logging.info(f"Data Transformation artifact")
            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transform_object_path=self.data_transformation_config.transform_object_path,
                transformed_train_path = self.data_transformation_config.transformed_train_path,
                transformed_test_path = self.data_transformation_config.transformed_test_path
            )

            logging.info(f"Data transformation object {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise SolarException(e, sys)
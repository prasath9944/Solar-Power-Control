from solar_power.predictor import ModelResolver
from solar_power.entity import config_entity,artifact_entity
from solar_power.exception import SolarException
from solar_power.logger import logging
from solar_power.utils import load_object
from sklearn.metrics import explained_variance_score
import pandas  as pd
import sys,os
from solar_power import utils
from solar_power.config import TARGET_COLUMN
class ModelEvaluation:

    def __init__(self,
        model_eval_config:config_entity.ModelEvaluationConfig,
        data_ingestion_artifact:artifact_entity.DataIngestionArtifact,
        data_transformation_artifact:artifact_entity.DataTransformationArtifact,
        model_trainer_artifact:artifact_entity.ModelTrainerArtifact      
        ):
        try:
            logging.info(f"{'>>'*20}  Model Evaluation {'<<'*20}")
            self.model_eval_config=model_eval_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_transformation_artifact=data_transformation_artifact
            self.model_trainer_artifact=model_trainer_artifact
            self.model_resolver = ModelResolver()

            
        except Exception as e:
            raise SolarException(e,sys)



    def initiate_model_evaluation(self)->artifact_entity.ModelEvaluationArtifact:
        try:
            #if saved model folder has model the we will compare 
            #which model is best trained or the model from saved model folder

            logging.info("if saved model folder has model the we will compare "
            "which model is best trained or the model from saved model folder")
            latest_dir_path = self.model_resolver.get_latest_dir_path()
            if latest_dir_path==None:
                model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,
                improved_accuracy=None)
                logging.info(f"Model evaluation artifact: {model_eval_artifact}")
                return model_eval_artifact


            #Finding location of transformer model and target encoder
            logging.info("Finding location of transformer model and target encoder")
            transformer_path = self.model_resolver.get_latest_transformer_path()
            model_path = self.model_resolver.get_latest_model_path()
            # target_encoder_path = self.model_resolver.get_latest_target_encoder_path()

            logging.info("Previous trained objects of transformer, model and target encoder")
            #Previous trained  objects
            transformer = load_object(file_path=transformer_path)
            model = load_object(file_path=model_path)
            # target_encoder = load_object(file_path=target_encoder_path)

            

            logging.info("Currently trained model objects")
            #Currently trained model objects
            current_transformer = load_object(file_path=self.data_transformation_artifact.transform_object_path)
            current_model  = load_object(file_path=self.model_trainer_artifact.model_path)
            # current_target_encoder = load_object(file_path=self.data_transformation_artifact.target_encoder_path)

            


            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            logging.info(f"test_df Columns: {test_df.columns}")
            target_df = test_df[TARGET_COLUMN]
            y_true=target_df
            # y_true =target_encoder.transform(target_df)
            # accuracy using previous trained model
            
            input_feature_name = list(transformer.feature_names_in_)
            test_df=test_df[input_feature_name]
            logging.info(f"Transformed feature name are {input_feature_name}")

            boolean_features=[feature for feature in test_df if test_df[feature].dtype=='bool']
            logging.info(f"Categorical feature in test_df:{boolean_features}")

            test_df=utils.convert_boolean_toNumerical(df=test_df, boolean_features=boolean_features)
                
            input_arr =transformer.transform(test_df)
            y_pred = model.predict(input_arr)
            print(f"Prediction using previous model: {y_pred[:5]}")
            previous_model_score = explained_variance_score(y_true=y_true, y_pred=y_pred)
            logging.info(f"Accuracy using previous trained model: {previous_model_score}")
           
            # accuracy using current trained model
            input_feature_name = list(current_transformer.feature_names_in_)
            input_arr =current_transformer.transform(test_df[input_feature_name])
            y_pred = current_model.predict(input_arr)
            # y_true =current_target_encoder.transform(target_df)
            print(f"Prediction using trained model: {y_pred[:5]}")
            current_model_score = explained_variance_score(y_true=y_true, y_pred=y_pred)
            logging.info(f"Accuracy using current trained model: {current_model_score}")
            if current_model_score<=previous_model_score:
                logging.info(f"Current trained model is not better than previous model")
                raise Exception("Current trained model is not better than previous model")

            model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,
            improved_accuracy=current_model_score-previous_model_score)
            logging.info(f"Model eval artifact: {model_eval_artifact}")
            return model_eval_artifact


        except Exception as e:
            raise SolarException(e, sys)
from solar_power.entity import artifact_entity,config_entity
from solar_power.exception import SolarException
from solar_power.logger import logging
from typing import Optional
from sklearn.metrics import explained_variance_score
import os,sys 
from sklearn.ensemble import RandomForestRegressor
from solar_power import utils


class ModelTrainer:


    def __init__(self,model_trainer_config:config_entity.ModelTrainerConfig,
                data_transformation_artifact:artifact_entity.DataTransformationArtifact
                ):
        try:
            logging.info(f"{'>>'*20} Model Trainer {'<<'*20}")
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact

        except Exception as e:
            raise SolarException(e, sys)

    def fine_tune(self):
        try:
            #Wite code for Grid Search CV
            pass
            

        except Exception as e:
            raise SolarException(e, sys)

    def train_model(self,x,y):
        try:
            rfg =  RandomForestRegressor()
            rfg.fit(x,y)
            return rfg
        except Exception as e:
            raise SolarException(e, sys)


    def initiate_model_trainer(self,)->artifact_entity.ModelTrainerArtifact:
        try:
            logging.info(f"Loading train and test array.")
            train_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_path)
            logging.info(f"Train_arr shaps:{train_arr.shape}")
            test_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_path)
            logging.info(f"test arr shape :{test_arr.shape}")

            logging.info(f"Splitting input and target feature from both train and test arr.")
            x_train,y_train = train_arr[:,:-1],train_arr[:,-1]
            x_test,y_test = test_arr[:,:-1],test_arr[:,-1]

            logging.info(f"Train the model")
            model = self.train_model(x=x_train,y=y_train)

            logging.info(f"Calculating EVS_train_score train score")
            yhat_train = model.predict(x_train)
            EVS_train_score=(explained_variance_score(y_true=y_train,y_pred=yhat_train)*100)
            logging.info(f"The train score accuracy is {EVS_train_score}")

            logging.info(f"Calculating EVS_train_score test score")
            yhat_test = model.predict(x_test)
            EVS_test_score=(explained_variance_score(y_true=y_test,y_pred=yhat_test)*100)
            logging.info(f"The test score accuracy is {EVS_test_score}")
            
            logging.info(f"train score:{EVS_train_score} and tests score {EVS_test_score}")
            #check for overfitting or underfiiting or expected score
            logging.info(f"Checking if our model is underfitting or not")
            if EVS_test_score<self.model_trainer_config.expected_score:
                raise Exception(f"Model is not good as it is not able to give \
                expected accuracy: {self.model_trainer_config.expected_score}: model actual score: {EVS_test_score}")

            logging.info(f"Checking if our model is overfiiting or not")
            diff = abs(EVS_train_score-EVS_test_score)
            logging.info(F"The difference between the train and test score is {diff}")

            if diff>self.model_trainer_config.overfitting_threshold:
                raise Exception(f"Train and test score diff: {diff} is more than overfitting threshold {self.model_trainer_config.overfitting_threshold}")

            #save the trained model
            logging.info(f"Saving mode object")
            utils.save_object(file_path=self.model_trainer_config.model_path, obj=model)

            #prepare artifact
            logging.info(f"Prepare the artifact")
            model_trainer_artifact  = artifact_entity.ModelTrainerArtifact(model_path=self.model_trainer_config.model_path,EVS_train_score=EVS_train_score, EVS_test_score=EVS_test_score)
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise SolarException(e, sys)
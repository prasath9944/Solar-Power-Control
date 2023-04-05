import pymongo
import pandas as pd
import json
from dataclasses import dataclass
# Provide the mongodb localhost url to connect python to mongodb.
import os

@dataclass
class EnvironmentVariable:
    mongo_db_url:str = "mongodb+srv://prasathk:Luci1108@cluster0.n634yqn.mongodb.net/?retryWrites=true&w=majority"






env_var = EnvironmentVariable()
mongo_client = pymongo.MongoClient(env_var.mongo_db_url)
TARGET_COLUMN = "Power Generated"

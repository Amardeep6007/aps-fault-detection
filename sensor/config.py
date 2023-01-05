import pymongo 
import pandas as pd
import json
import os
from dataclasses import dataclass


@dataclass
class EnvironmentVariables():
    mongo_db_url:str = os.getenv("MONGO_DB_URL")

#mongoDB localhost url to connect python to mongodb 
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/neurolabDB")

env_var = EnvironmentVariables()
pymongo.MongoClient(env_var.mongo_db_url)
TARGET_COLUMN = "class"


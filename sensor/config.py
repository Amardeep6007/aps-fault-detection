import pymongo 
import pandas as pd
import json
import os
from dataclasses import dataclass


@dataclass
class EnvironmentVariables():
    mongo_db_url:str = os.getenv("MONGO_DB_URL")
    aws_access_key_id:str = os.getenv("AWS_ACCESS_KEY_ID")
    aws_access_secret_key:str = os.getenv("AWS_SECRET_ACCESS_KEY")

#mongoDB localhost url to connect python to mongodb 
#mongo_client = pymongo.MongoClient("mongodb+srv://amar:Amar6007@cluster0.s0catd9.mongodb.net/?retryWrites=true&w=majority")

env_var = EnvironmentVariables()
mongo_client = pymongo.MongoClient(env_var.mongo_db_url)
TARGET_COLUMN = "class"


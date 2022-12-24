from sensor import utils
from sensor.entity import config_entity
from sensor.entity import artifact_entity
from sensor.exception import SensorException
from sensor.logger import logging
import os, sys
import pandas as pd
import numpy as np


class data_ingestion:
    def __init__(self, data_ingestion_config:data_ingestion_config):
        try:
            logging.info(f"{'>>'*20} Data Ingestion {'<<'*20}")
            self.data_ingestion_config= data_ingestion_config
        except Exception as e:
            raise SensorException(e, sys)
            
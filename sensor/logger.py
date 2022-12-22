import logging
import os
from datetime import datetime


#log file name
#we are creating the file name based on the date time stamp
#everytime we are excuting the code then the logs will be stored in new file which are created with this below code
LOG_FILE_NAME = f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.log"

#log directory
#here we are defining the directory in which the log file will be mentioned
#here we are creating the "logs" folder inside the current working directory
LOG_FILE_DIR = os.path.join(os.getcwd(),"logs")

#create folder if not available
os.makedirs(LOG_FILE_DIR,exist_ok=True)

#now everything which is required to create a full file path is available, hence doing the same
#log file path
LOG_FILE_PATH = os.path.join(LOG_FILE_DIR,LOG_FILE_NAME)

#Now doing the basic configuration for the loggin system for our project usinf basicConfig()    
logging.basicConfig(
    filename=LOG_FILE_PATH, #specifying in which file we are creating the log
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s", #specifying the logging message format how it will be displayed in the output terminal
    level=logging.INFO, #specifying the logging level #there are total 5 levels in the logging system
)
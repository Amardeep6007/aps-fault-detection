#the below code ensures that all the environment variables mentioned in the .env file is read and installed whenever we are running the main code  
#we are writing the below code in the __init__() of the sensor and hence whenever we are going to call the sensor then automatically these below code will be read
from dotenv import load_dotenv
print(f'Loading the environment variable form .env file ')
load_dotenv()
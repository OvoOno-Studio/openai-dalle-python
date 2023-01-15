import os
from dotenv import load_dotenv

load_dotenv()

APIKey = os.getenv('API_KEY') 
InfuraKey = os.getenv('INFURA_KEY')
dbPW = os.getenv('DB_PASSWORD')
SecretKey = os.urandom(32) 
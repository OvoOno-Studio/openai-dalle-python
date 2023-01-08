import os
from dotenv import load_dotenv

load_dotenv()

APIKey = os.getenv('API_KEY') 
InfuraKey = os.getenv('INFURA_KEY')
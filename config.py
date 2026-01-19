import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-12345')
    
    SERPAPI_KEY = os.getenv('SERPAPI_KEY')
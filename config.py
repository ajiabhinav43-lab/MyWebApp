import os
from dotenv import load_dotenv

# Load the .env file into environment variables
load_dotenv()

class Config:
    # Flask session security key
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-dev-key-change-in-prod')

    # SQLAlchemy database URI
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        '"mysql+pymysql://admin:Abhi_2026@mywebapp-db.cfm6sao8erum.ap-south-1.rds.amazonaws.com/myappdb'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # AWS S3 configuration
    AWS_ACCESS_KEY_ID     = os.getenv('AWS_ACCESS_KEY')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRETS_ACCESS_KEY')
    AWS_REGION            = os.getenv('AWS_REGION', 'ap-south-1')
    S3_BUCKET_NAME        = os.getenv('S3_BUCKET_NAME', 'myapp-media-uploads')

    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024   # max upload size: 16 MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'pdf'}

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

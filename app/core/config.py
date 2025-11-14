import os
from dotenv import load_dotenv

load_dotenv()

SECRET_ACCESS_TOKEN = os.getenv("SECRET_ACCESS_TOKEN")
EMAIL_ADDRESS = os.getenv("EMAIL")
PASSWORD_SECRET_KEY = os.getenv("PASSWORD_SECRET_KEY")
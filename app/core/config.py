import os
from dotenv import load_dotenv

load_dotenv()

SECRET_ACCESS_TOKEN = os.getenv("SECRET_ACCESS_TOKEN")

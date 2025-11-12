import os
from dotenv import load_dotenv

# load env
load_dotenv()

SECRET_ACCESS_TOKEN = os.environ.get("SECRET_ACCESS_TOKEN")
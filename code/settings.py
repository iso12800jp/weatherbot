import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

CK = os.environ.get("CONSUMER_KEY")
CS = os.environ.get("CONSUMER_SECRET")
ATK = os.environ.get("ACCESS_TOKEN_KEY")
ATS = os.environ.get("ACCESS_TOKEN_SECRET")
import os

from dotenv import load_dotenv

if os.getenv("ENV") != "DOCKER":
    load_dotenv("../.env.local")

    assert os.getenv("ENV") == "LOCAL"

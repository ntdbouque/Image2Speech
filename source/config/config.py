import os
from dotenv import load_dotenv
from openai import OpenAI

def get_openai_client():
    """
    Loads the environment variables and returns the OpenAI client.
    """
    load_dotenv(override=True)
    return OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

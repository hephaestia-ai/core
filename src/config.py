import os
from google.cloud import bigquery
from openai import OpenAI

# Load environment variables from .env file

class ConfigBigQuery:
    def __init__(self):
        import google.auth # type: ignore
        self.credentials, self.project_id = google.auth.default()
        self.client = bigquery.Client(project=self.project_id, credentials=self.credentials)

class ConfigOpenAI:
    def __init__(self):
        self.open_ai_api_key = os.getenv('OPENAI_API_KEY')
        self.client = OpenAI(api_key=self.open_ai_api_key)

if __name__=="__main__":
    ConfigBigQuery()
    ConfigOpenAI()
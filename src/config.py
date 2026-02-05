import os

try:

    MONGO_DEFAULT_URL = os.getenv("MONGO_DEFAULT_URL")
    MONGO_DATA_URL = os.getenv("MONGO_DATA_URL")
    OPENAI_KEY = os.getenv("OPENAI_KEY")
    DESCRIPTION_SIZE = 3000
    OPENSEARCH_USERNAME = os.getenv("OPENSEARCH_USERNAME")
    OPENSEARCH_PASSWORD = os.getenv("OPENSEARCH_PASSWORD")

except KeyError as e:
    raise EnvironmentError(f"Missing required environment variable: {e.args[0]}")

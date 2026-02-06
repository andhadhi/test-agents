import os
import logging

logger = logging.getLogger(__name__)

try:

    MONGO_DEFAULT_URL = os.getenv("MONGO_DEFAULT_URL")
    MONGO_DATA_URL = os.getenv("MONGO_DATA_URL")
    OPENAI_KEY = os.getenv("OPENAI_KEY")
    DESCRIPTION_SIZE = 3000
    OPENSEARCH_USERNAME = os.getenv("OPENSEARCH_USERNAME")
    OPENSEARCH_PASSWORD = os.getenv("OPENSEARCH_PASSWORD")

    logger.info(
        "Config loaded: MONGO_DEFAULT_URL=%s, MONGO_DATA_URL=%s, OPENAI_KEY=%s, OPENSEARCH_USERNAME=%s, OPENSEARCH_PASSWORD=%s",
        "set" if MONGO_DEFAULT_URL else "missing",
        "set" if MONGO_DATA_URL else "missing",
        "set" if OPENAI_KEY else "missing",
        "set" if OPENSEARCH_USERNAME else "missing",
        "set" if OPENSEARCH_PASSWORD else "missing",
    )
except KeyError as e:
    logger.error("Missing required environment variable: %s", e.args[0])
    raise EnvironmentError(f"Missing required environment variable: {e.args[0]}")

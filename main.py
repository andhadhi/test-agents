import asyncio
import logging
import sys

# Configure logging first so all modules get this format (timestamp, level, module, message)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stdout,
    force=True,
)
logger = logging.getLogger(__name__)

from src.pipeline import Pipeline

if __name__ == "__main__":
    logger.info("Starting pipeline (main.py)")
    obj = Pipeline()
    toolkit_article_id = "63241638417ca879fd2f76d0"
    logger.info("Running pipeline for toolkit_article_id=%s", toolkit_article_id)
    asyncio.run(obj.run(toolkit_article_id))
    logger.info("Pipeline finished (main.py)")

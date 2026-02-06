import logging
import tiktoken

logger = logging.getLogger(__name__)


def count_tokens(text: str, model: str = "text-embedding-3-large") -> int:
    encoding = tiktoken.get_encoding("cl100k_base")
    n = len(encoding.encode(text))
    logger.debug("count_tokens: model=%s, tokens=%d", model, n)
    return n
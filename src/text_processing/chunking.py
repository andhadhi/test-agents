import logging
import spacy
import tiktoken
from math import floor

logger = logging.getLogger(__name__)
nlp = spacy.load("en_core_web_sm")


def splitter(text: str, max_tokens: int = 4000, overlap_tokens: int = None):
    logger.debug("splitter: text_len=%d, max_tokens=%d", len(text), max_tokens)
    if overlap_tokens is None:
        overlap_tokens = floor(max_tokens * 0.2)
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
    if not sentences:
        logger.debug("splitter: no sentences, returning []")
        return []
    enc = tiktoken.encoding_for_model("gpt-4o")
    token_counts = [len(enc.encode(s)) for s in sentences]
    chunks = []
    start = 0
    while start < len(sentences):
        end = start
        token_acc = 0
        while end < len(sentences):
            tok_count = token_counts[end]
            if token_acc + tok_count <= max_tokens:
                token_acc += tok_count
                end += 1
            else:
                break
        if end == start:
            sent = sentences[start]
            chunks.append({
                "search_content": sent,
                "exact_content": sent
            })
            start += 1
            continue
        overlap_count = 0
        overlap_acc = 0
        i = start - 1
        while i >= 0:
            tok_count = token_counts[i]
            if overlap_acc + tok_count <= overlap_tokens:
                overlap_acc += tok_count
                overlap_count += 1
                i -= 1
            else:
                break
        if start == 0:
            search_sents = sentences[start:end]
            exact_sents = sentences[start:end]
        else:
            search_sents = sentences[start - overlap_count:end]
            exact_sents = sentences[start:end]
        chunks.append({
            "search_content": " ".join(search_sents),
            "exact_content": " ".join(exact_sents)
        })
        start = end
    logger.debug("splitter: produced %d chunks", len(chunks))
    return chunks

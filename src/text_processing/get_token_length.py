import tiktoken

def count_tokens(text: str, model: str = "text-embedding-3-large") -> int:
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))
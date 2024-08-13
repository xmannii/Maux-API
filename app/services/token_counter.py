import tiktoken


# Supported models
SUPPORTED_MODELS = {
    "gpt-4o": "o200k_base",
    "gpt-4": "cl100k_base",
    "gpt-3.5-turbo": "cl100k_base",
    "gpt-3.5": "cl100k_base",
    "gpt-35-turbo": "cl100k_base",
    "text-embedding-ada-002": "cl100k_base",
    "text-embedding-3-small": "cl100k_base",
    "text-embedding-3-large": "cl100k_base",
}

def count_tokens(content: str, model: str = "gpt-3.5-turbo") -> int:
    if model not in SUPPORTED_MODELS:
        raise ValueError(f"Unsupported model: {model}")
    
    encoding_name = SUPPORTED_MODELS[model]
    encoding = tiktoken.get_encoding(encoding_name)
    tokens = encoding.encode(content)
    num_tokens = len(tokens)
    return num_tokens


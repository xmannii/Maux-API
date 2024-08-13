import os
import tempfile
from sentence_transformers import SentenceTransformer

def get_model_path(model_name: str) -> str:
    model_cache_dir = os.path.join(tempfile.gettempdir(), "sentence_transformer_cache")
    os.makedirs(model_cache_dir, exist_ok=True)
    
    model_path = os.path.join(model_cache_dir, model_name)
    
    if not os.path.exists(model_path):
        print(f"Downloading model {model_name} and saving to {model_path}")
        model = SentenceTransformer(model_name, trust_remote_code=True)
        model.save(model_path)
        print("Model saved successfully")
    else:
        print(f"Model loaded from cache: {model_path}")
    
    return model_path
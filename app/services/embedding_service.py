from sentence_transformers import SentenceTransformer
from app.utils.model_utils import get_model_path

class EmbeddingService:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model = self._load_model()

    def _load_model(self):
        model_path = get_model_path(self.model_name)
        return SentenceTransformer(model_path, trust_remote_code=True)

    def get_embedding(self, text: str):
        return self.model.encode([text])[0]
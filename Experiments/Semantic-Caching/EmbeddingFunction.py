
from sentence_transformers import SentenceTransformer
from chromadb import EmbeddingFunction, Documents, Embeddings


class MyEmbeddingFunction(EmbeddingFunction):
    def __init__(self):
        self.model = SentenceTransformer("nomic-ai/nomic-embed-text-v1.5")

    def __call__(self, input: Documents) -> Embeddings:
        return self.model.encode(input)
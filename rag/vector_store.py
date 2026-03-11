import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        # embedding dimension of all-MiniLM-L6-v2 is 384
        self.index = faiss.IndexFlatL2(384)
        self.documents = []

    def add_documents(self, docs):
        embeddings = self.model.encode(docs)
        self.index.add(np.array(embeddings).astype('float32'))
        self.documents.extend(docs)

    def search(self, query, top_k=1):
        if self.index.ntotal == 0:
            return []
            
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(np.array(query_embedding).astype('float32'), top_k)
        
        results = []
        for i in range(top_k):
            idx = indices[0][i]
            if idx != -1 and idx < len(self.documents):
                results.append(self.documents[idx])
                
        return results

# Initialize with base rules
def initialize_knowledge_base():
    store = VectorStore()
    base_rules = [
        "Crowd larger than 5 people may indicate suspicious gathering.",
        "Person remaining more than 2 minutes near entrance is loitering.",
        "Entrance allowed only for staff after 9PM."
    ]
    store.add_documents(base_rules)
    return store

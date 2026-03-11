from rag.vector_store import initialize_knowledge_base

class KnowledgeBase:
    def __init__(self):
        self.store = initialize_knowledge_base()
        
    def query_policy(self, event_name, risk_context=""):
        query = f"What is the system policy for {event_name}? {risk_context}"
        results = self.store.search(query, top_k=1)
        if results:
            return results[0]
        return "No specific policy found for this event."

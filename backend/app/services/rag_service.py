from typing import List, Dict
from app.services.embeddings_service import top_k
from app.services.kb_service import load_kb

def retrieve_roles(query: str, k: int = 5) -> List[Dict]:
    df = load_kb()
    records = df.to_dict(orient='records')
    idxs = top_k(query, k)
    return [records[i] for i in idxs]


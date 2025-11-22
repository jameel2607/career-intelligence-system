from typing import List, Dict, Optional
import os
import numpy as np
from pathlib import Path
from app.services.kb_service import load_kb
from app.core.config import settings

_kb_texts: Optional[List[str]] = None
_embeddings: Optional[np.ndarray] = None
_faiss_index = None
_faiss_available = False
_st_available = False

try:
    import faiss
    _faiss_available = True
    print("✅ FAISS available")
except Exception as e:
    _faiss_available = False
    print(f"⚠️ FAISS not available: {e}")

try:
    from sentence_transformers import SentenceTransformer
    _st_available = True
    print("✅ SentenceTransformers available")
except Exception as e:
    _st_available = False
    print(f"⚠️ SentenceTransformers not available: {e}")

# Alternative: Use transformers directly if sentence-transformers fails
try:
    from transformers import AutoTokenizer, AutoModel
    import torch
    _transformers_available = True
    print("✅ HuggingFace Transformers available")
except Exception as e:
    _transformers_available = False
    print(f"⚠️ HuggingFace Transformers not available: {e}")

def _row_text(row: Dict) -> str:
    """Extract comprehensive text from row for RAG embedding"""
    # Map your actual column names to text extraction
    text_parts = []
    
    # Core job information
    job_role = str(row.get('Job Role', row.get('job_role', '')))
    job_family = str(row.get('Job Family', row.get('job_family', '')))
    cluster = str(row.get('Cluster', row.get('cluster', '')))
    level = str(row.get('Level', row.get('level', '')))
    
    # Skills (most important for RAG)
    tech_skills = str(row.get('Technical Skills', row.get('technical_skills', '')))
    soft_skills = str(row.get('Soft Skills', row.get('soft_skills', '')))
    domain_skills = str(row.get('Domain / Functional Skills', row.get('domain_skills', '')))
    
    # Additional context
    description = str(row.get('Job Description Summary', row.get('description', '')))
    qualifications = str(row.get('Qualifications / Degrees', row.get('qualifications', '')))
    experience = str(row.get('Experience Range', row.get('experience_range', '')))
    
    # Combine all relevant text for comprehensive RAG search
    text_parts = [
        job_role, job_family, cluster, level,
        tech_skills, soft_skills, domain_skills,
        description, qualifications, experience
    ]
    
    # Filter out empty strings and join
    meaningful_parts = [part.strip() for part in text_parts if part.strip() and part.strip().lower() != 'nan']
    return ' '.join(meaningful_parts).lower()

def ensure_kb_texts():
    global _kb_texts
    if _kb_texts is None:
        df = load_kb()
        _kb_texts = [_row_text(rec) for rec in df.to_dict(orient='records')]

def _emb_dir() -> Path:
    base = Path(__file__).resolve().parents[3]
    p = base / settings.EMBEDDINGS_DIR
    p.mkdir(parents=True, exist_ok=True)
    return p

def build_index():
    global _embeddings, _faiss_index
    ensure_kb_texts()
    
    if not _kb_texts:
        print("⚠️ No knowledge base texts available")
        return
    
    print(f"🔄 Building embeddings for {len(_kb_texts)} entries...")
    
    # Try SentenceTransformers first
    if _st_available:
        try:
            print(f"📊 Using SentenceTransformers model: {settings.EMBEDDING_MODEL}")
            model = SentenceTransformer(settings.EMBEDDING_MODEL)
            
            # Process in batches for large datasets (optimized for 1000+ records)
            batch_size = 50 if len(_kb_texts) > 500 else 100  # Smaller batches for large datasets
            all_embeddings = []
            
            print(f"📊 Processing {len(_kb_texts)} entries in batches of {batch_size}")
            
            for i in range(0, len(_kb_texts), batch_size):
                batch = _kb_texts[i:i + batch_size]
                batch_embeddings = model.encode(batch, convert_to_numpy=True, show_progress_bar=False)
                all_embeddings.append(batch_embeddings)
                
                batch_num = i//batch_size + 1
                total_batches = (len(_kb_texts) + batch_size - 1)//batch_size
                progress = (batch_num / total_batches) * 100
                print(f"✅ Processed batch {batch_num}/{total_batches} ({progress:.1f}%)")
            
            _embeddings = np.vstack(all_embeddings)
            print(f"💾 Saved embeddings: {_embeddings.shape}")
            
            # Build FAISS index if available
            if _faiss_available:
                try:
                    _faiss_index = faiss.IndexFlatIP(_embeddings.shape[1])
                    _faiss_index.add(_embeddings.astype('float32'))
                    print(f"🔍 FAISS index built with {_embeddings.shape[0]} vectors")
                except Exception as e:
                    print(f"⚠️ FAISS index creation failed: {e}")
            
            # Save to disk
            try:
                emb_dir = _emb_dir()
                emb_dir.mkdir(parents=True, exist_ok=True)
                np.save(emb_dir / "embeddings.npy", _embeddings)
                
                if _faiss_available and _faiss_index:
                    faiss.write_index(_faiss_index, str(emb_dir / "faiss_index.bin"))
                
                print("✅ Embeddings saved to disk")
            except Exception as e:
                print(f"⚠️ Failed to save embeddings: {e}")
            
        except Exception as e:
            print(f"❌ SentenceTransformers failed: {e}")
            _embeddings = None
    
    # Fallback to HuggingFace Transformers
    elif _transformers_available:
        try:
            print("📊 Using HuggingFace Transformers as fallback")
            tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
            model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
            
            all_embeddings = []
            batch_size = 50  # Smaller batches for raw transformers
            
            for i in range(0, len(_kb_texts), batch_size):
                batch = _kb_texts[i:i + batch_size]
                
                # Tokenize and encode
                inputs = tokenizer(batch, padding=True, truncation=True, return_tensors='pt', max_length=512)
                
                with torch.no_grad():
                    outputs = model(**inputs)
                    # Use mean pooling
                    embeddings = outputs.last_hidden_state.mean(dim=1).numpy()
                    all_embeddings.append(embeddings)
                
                print(f"✅ Processed batch {i//batch_size + 1}/{(len(_kb_texts) + batch_size - 1)//batch_size}")
            
            _embeddings = np.vstack(all_embeddings)
            print(f"💾 Saved embeddings: {_embeddings.shape}")
            
            # Build FAISS index if available
            if _faiss_available:
                try:
                    _faiss_index = faiss.IndexFlatIP(_embeddings.shape[1])
                    _faiss_index.add(_embeddings.astype('float32'))
                    print(f"🔍 FAISS index built with {_embeddings.shape[0]} vectors")
                except Exception as e:
                    print(f"⚠️ FAISS index creation failed: {e}")
            
            # Save to disk
            try:
                emb_dir = _emb_dir()
                emb_dir.mkdir(parents=True, exist_ok=True)
                np.save(emb_dir / "embeddings.npy", _embeddings)
                
                if _faiss_available and _faiss_index:
                    faiss.write_index(_faiss_index, str(emb_dir / "faiss_index.bin"))
                
                print("✅ Embeddings saved to disk")
            except Exception as e:
                print(f"⚠️ Failed to save embeddings: {e}")
            
        except Exception as e:
            print(f"❌ HuggingFace Transformers failed: {e}")
            _embeddings = None
    
    else:
        print("❌ No embedding models available")
        _embeddings = None

def naive_similarity(a: str, b: str) -> float:
    sa = set(a.split())
    sb = set(b.split())
    inter = len(sa & sb)
    return inter / max(1, len(sa))

def top_k(query: str, k: int = 5) -> List[int]:
    ensure_kb_texts()
    if _faiss_index is not None and _embeddings is not None and _st_available:
        model = SentenceTransformer(getattr(settings, 'EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2'))
        qv = model.encode([query], convert_to_numpy=True).astype('float32')
        scores, idxs = _faiss_index.search(qv, k)
        return list(idxs[0])
    q = query.lower()
    sims = [(i, naive_similarity(q, _kb_texts[i])) for i in range(len(_kb_texts))]
    sims.sort(key=lambda x: x[1], reverse=True)
    return [i for i, _ in sims[:k]]

import pandas as pd
from typing import List, Dict
from app.core.config import settings
from pathlib import Path

_kb_cache = None

def load_kb() -> pd.DataFrame:
    global _kb_cache
    if _kb_cache is None:
        # Try multiple possible paths
        base = Path(__file__).resolve().parents[3]
        
        # Primary path (where upload saves)
        upload_path = base / "backend" / "knowledge_base" / "career_intelligence_kb.xlsx"
        
        # Secondary path (original config)
        config_path = base / settings.KB_FILE_PATH
        
        # Try paths in order
        paths_to_try = [upload_path, config_path]
        
        _kb_cache = None
        for path in paths_to_try:
            try:
                _kb_cache = pd.read_excel(path)
                # Clean NaN values for JSON serialization
                _kb_cache = _kb_cache.fillna('')
                print(f"✅ Loaded {len(_kb_cache)} entries from {path}")
                break
            except Exception as e:
                print(f"⚠️ No KB file found at {path}, error: {e}")
                continue
        
        # If no file found, return empty DataFrame
        if _kb_cache is None:
            print("⚠️ No KB file found in any location, returning empty DataFrame")
            _kb_cache = pd.DataFrame(columns=[
                'job_role', 'job_family', 'cluster', 'level', 'technical_skills', 'soft_skills', 'domain_skills',
                'experience_range', 'job_index', 'description', 
                'average_salary', 'sources'
            ])
    return _kb_cache

def reset_kb_cache():
    global _kb_cache
    _kb_cache = None

def search_roles(query: str, limit: int = 5) -> List[Dict]:
    """Enhanced search function optimized for your Excel structure"""
    df = load_kb()
    if len(df) == 0:
        return []
    
    q = str(query).lower()
    
    # Priority search in most relevant columns for your data structure
    priority_columns = [
        'Job Role', 'Technical Skills', 'Soft Skills', 'Domain / Functional Skills',
        'Job Description Summary', 'Job Family', 'Cluster', 'Qualifications / Degrees'
    ]
    
    # Start with high-priority column search
    mask = False
    for col in priority_columns:
        if col in df.columns:
            try:
                col_mask = df[col].astype(str).str.lower().str.contains(q, na=False)
                mask = mask | col_mask
            except Exception:
                continue
    
    # If no results in priority columns, search all columns
    if not mask.any():
        for col in df.columns:
            if col not in priority_columns:
                try:
                    col_mask = df[col].astype(str).str.lower().str.contains(q, na=False)
                    mask = mask | col_mask
                except Exception:
                    continue
    
    # Get results and ensure proper column mapping
    results = df[mask].head(limit).to_dict(orient='records')
    
    # Standardize column names for frontend compatibility
    standardized_results = []
    for result in results:
        standardized = {
            'job_role': result.get('Job Role', ''),
            'job_family': result.get('Job Family', ''),
            'cluster': result.get('Cluster', ''),
            'level': result.get('Level', ''),
            'technical_skills': result.get('Technical Skills', ''),
            'soft_skills': result.get('Soft Skills', ''),
            'domain_skills': result.get('Domain / Functional Skills', ''),
            'experience_range': result.get('Experience Range', ''),
            'job_index': result.get('Job Index / ID', ''),
            'description': result.get('Job Description Summary', ''),
            'average_salary': result.get('Average Salary (India / Global)', ''),
            'sources': result.get('Primary Data Sources (with URLs)', ''),
            'qualifications': result.get('Qualifications / Degrees', '')
        }
        # Keep original data as well
        standardized.update(result)
        standardized_results.append(standardized)
    
    return standardized_results

def delete_kb_entry(entry_id: int) -> bool:
    """Delete a knowledge base entry by index and save to file"""
    global _kb_cache
    try:
        df = load_kb()
        if entry_id < 0 or entry_id >= len(df):
            return False
        
        # Remove the entry
        df = df.drop(df.index[entry_id]).reset_index(drop=True)
        
        # Save back to file if it's not mock data
        base = Path(__file__).resolve().parents[3]
        path = base / settings.KB_FILE_PATH
        if path.exists():
            df.to_excel(path, index=False)
        
        # Update cache
        _kb_cache = df
        return True
    except Exception:
        return False

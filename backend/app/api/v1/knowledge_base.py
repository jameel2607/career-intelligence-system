from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from app.services.kb_service import search_roles, reset_kb_cache, load_kb, delete_kb_entry
from app.services.embeddings_service import build_index

router = APIRouter()

class KBQuery(BaseModel):
    query: str
    limit: int = 5

@router.post('/search')
def kb_search(data: KBQuery):
    results = search_roles(data.query, data.limit)
    return {'results': results, 'count': len(results)}

@router.post('/refresh')
def kb_refresh():
    build_index()
    return {'refreshed': True}

@router.delete('/clear')
def kb_clear():
    """Clear all knowledge base data"""
    from app.core.config import settings
    from pathlib import Path
    try:
        base = Path(__file__).resolve().parents[3]
        kb_file = base / settings.KB_FILE_PATH
        emb_dir = base / settings.EMBEDDINGS_DIR
        
        # Remove KB file if exists
        if kb_file.exists():
            kb_file.unlink()
            
        # Remove embeddings
        if emb_dir.exists():
            for f in emb_dir.glob('*.npy'):
                f.unlink()
                
        # Reset cache
        reset_kb_cache()
        
        return {'cleared': True, 'message': 'Knowledge base cleared successfully'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/all')
def kb_get_all():
    """Get all knowledge base entries"""
    df = load_kb()
    return df.to_dict(orient='records')

@router.delete('/entry/{entry_id}')
def kb_delete_entry(entry_id: int):
    """Delete a specific knowledge base entry by index"""
    try:
        result = delete_kb_entry(entry_id)
        if result:
            build_index()  # Rebuild embeddings after deletion
            return {'deleted': True, 'entry_id': entry_id}
        else:
            raise HTTPException(status_code=404, detail="Entry not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/upload')
async def kb_upload(file: UploadFile = File(...)):
    from app.core.config import settings
    from pathlib import Path
    import pandas as pd
    from app.services.kb_service import reset_kb_cache, load_kb
    from app.services.embeddings_service import build_index
    
    # Validate file type
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Only Excel files (.xlsx, .xls) are allowed")
    
    print(f"📤 Starting upload of {file.filename}")
    
    # Reset cache before upload
    reset_kb_cache()
    
    # Setup paths
    base = Path(__file__).resolve().parents[3]
    dest = base / settings.KB_FILE_PATH
    dest.parent.mkdir(parents=True, exist_ok=True)
    
    # Read and validate content
    content = await file.read()
    print(f"📁 File size: {len(content)} bytes")
    
    # Save file
    with open(dest, 'wb') as f:
        f.write(content)
    
    # Ensure file is accessible for load_kb function
    # Both upload and load should use the same path calculation
    load_dest = dest  # Use the same destination
    print(f"📋 File saved to: {dest}")
    print(f"📋 File exists: {dest.exists()}")
    
    # Verify the file can be read
    try:
        test_read = pd.read_excel(dest)
        print(f"✅ File verification: {len(test_read)} rows readable")
    except Exception as e:
        print(f"❌ File verification failed: {e}")
    
    # Validate Excel content
    try:
        df = pd.read_excel(dest)
        row_count = len(df)
        col_count = len(df.columns)
        print(f"✅ Excel validation: {row_count} rows, {col_count} columns")
        print(f"📋 Columns found: {list(df.columns)}")
        
        # Check if DataFrame is empty
        if row_count == 0:
            raise HTTPException(status_code=400, detail="Excel file is empty")
        
        # Provide feedback for large datasets
        if row_count > 500:
            print(f"📊 Large dataset detected ({row_count} rows)")
            print(f"⏱️ Estimated processing time: {row_count // 50 * 2}-{row_count // 50 * 4} seconds")
        elif row_count > 100:
            print(f"📊 Medium dataset detected ({row_count} rows)")
            print(f"⏱️ Estimated processing time: {row_count // 100 * 5}-{row_count // 100 * 10} seconds")
        
        # More flexible column checking - look for any job-related column
        job_columns = [col for col in df.columns if any(keyword in col.lower() for keyword in ['job', 'role', 'title', 'position'])]
        if not job_columns:
            print(f"⚠️ No job-related columns found. Available columns: {list(df.columns)}")
            # Don't fail - just proceed with available data
        else:
            print(f"✅ Found job-related columns: {job_columns}")
        
        # Check for any data issues
        print(f"📊 Sample data preview:")
        print(df.head(2).to_string())
        
    except pd.errors.EmptyDataError:
        print(f"❌ Excel file is empty or corrupted")
        raise HTTPException(status_code=400, detail="Excel file is empty or corrupted")
    except Exception as e:
        print(f"❌ Excel validation failed: {str(e)}")
        print(f"❌ Error type: {type(e).__name__}")
        import traceback
        print(f"❌ Full traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=f"Invalid Excel file: {str(e)}")
    
    # Reset cache to load new data
    reset_kb_cache()
    print(f"🔄 Cache reset, loading new data...")
    
    # Force reload by clearing embeddings cache too
    import app.services.embeddings_service as emb_service
    emb_service._kb_texts = None
    emb_service._embeddings = None
    emb_service._faiss_index = None
    
    # Verify data is loaded
    test_df = load_kb()
    print(f"✅ Verified: {len(test_df)} entries loaded")
    
    if len(test_df) == 0:
        print(f"❌ No data loaded! File path issue detected.")
        print(f"   Upload path: {dest}")
        print(f"   Load path calculation issue - checking alternative paths...")
        
        # Try alternative path
        alt_path = Path(__file__).resolve().parents[2] / "knowledge_base" / "career_intelligence_kb.xlsx"
        alt_path.parent.mkdir(parents=True, exist_ok=True)
        import shutil
        shutil.copy2(dest, alt_path)
        print(f"   Copied to alternative path: {alt_path}")
        
        # Reset cache again and try loading
        reset_kb_cache()
        test_df = load_kb()
        print(f"✅ After alternative copy: {len(test_df)} entries loaded")
    
    # Build embeddings for RAG
    print(f"🔄 Building embeddings for {row_count} entries...")
    try:
        build_index()
        print(f"✅ Embeddings built successfully")
    except Exception as e:
        print(f"⚠️ Embedding build failed: {e}")
        # Don't fail the upload, just warn
    
    return {
        'upload_id': 'kb', 
        'size': len(content),
        'rows': row_count,
        'columns': col_count,
        'filename': file.filename
    }

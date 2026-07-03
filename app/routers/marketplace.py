import json
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from app.core.db import get_db_connection
from app.core.dependencies import require_seller
from app.schemas.assets import AssetCreate

router = APIRouter(tags=["Asset Marketplace Core"])

@router.post("/assets", status_code=status.HTTP_201_CREATED)
def create_mining_asset(payload: AssetCreate, current_user: dict = Depends(require_seller)):
    """نشر أصل تعديني جديد في قاعدة البيانات الموحدة."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    images_str = json.dumps(payload.images_urls)
    specs_str = json.dumps(payload.specific_specs)
    
    cursor.execute('''
        INSERT INTO mining_assets (
            title, description, main_category, sub_category, price, currency, 
            is_negotiable, owner_id, state_province, locality, coordinates, 
            images_urls, specific_specs
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        payload.title, payload.description, payload.main_category, payload.sub_category,
        payload.price, payload.currency, int(payload.is_negotiable), current_user["id"],
        payload.state_province, payload.locality, payload.coordinates, images_str, specs_str
    ))
    
    asset_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {
        "message": "🔒 تم تسجيل أصل التعدين بنجاح وهو الآن في مرحلة (Pending Review) للاعتماد الإداري",
        "asset_id": asset_id
    }

@router.get("/assets")
def list_mining_assets(main_category: Optional[str] = None):
    """استعراض السوق بالكامل والتصفية الذكية."""
    conn = get_db_connection()
    query = "SELECT * FROM mining_assets"
    
    cursor = conn.execute(query)
    rows = cursor.fetchall()
    conn.close()
    
    results = []
    for row in rows:
        item = dict(row)
        try:
            item["images_urls"] = json.loads(item["images_urls"]) if item["images_urls"] else []
            item["specific_specs"] = json.loads(item["specific_specs"]) if item["specific_specs"] else {}
        except Exception:
            item["images_urls"] = []
            item["specific_specs"] = {}
        item["is_negotiable"] = bool(item["is_negotiable"])
        results.append(item)
        
    return results

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
from core.osint import search_profiles, generate_usernames
from core.database import init_db, seed_db, search_local_breaches
import dicttoxml
import json
import asyncio
import hashlib

app = FastAPI(title="Breacherr API", version="1.0.0")

@app.on_event("startup")
async def startup_event():
    init_db()
    seed_db()

# Allow CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

def get_gravatar_url(email: str):
    email_hash = hashlib.md5(email.lower().strip().encode('utf-8')).hexdigest()
    return f"https://www.gravatar.com/avatar/{email_hash}?d=identicon&s=200"

@app.get("/")
async def root():
    return {"message": "Breacherr API is running!"}

class SearchRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    dob: Optional[str] = None

@app.post("/api/search")
async def search_endpoint(request: SearchRequest):
    # This is now a wrapper for compatibility
    results = {"profiles": [], "breaches": []}
    
    if request.first_name or request.last_name or request.email:
        full_name = f"{request.first_name or ''} {request.last_name or ''}".strip()
        results["breaches"].extend(search_local_breaches(name=full_name if request.first_name else None, email=request.email))
        
        if request.email:
            avatar = get_gravatar_url(request.email)
            for b in results["breaches"]:
                b["Avatar"] = avatar

    usernames = []
    if request.username: 
        usernames.append({"username": request.username, "score": 99})
    
    if request.first_name and request.last_name:
        generated = generate_usernames(request.first_name, request.last_name, request.dob)
        usernames.extend(generated[:10])
    
    # Simple deduplication by username
    seen = set()
    unique_usernames = []
    for u in usernames:
        if u["username"] not in seen:
            unique_usernames.append(u)
            seen.add(u["username"])

    for un_data in unique_usernames:
        async for profile in search_profiles(un_data):
            if profile["status"] == "Found":
                results["profiles"].append(profile)
                
    return results

@app.get("/api/search/stream")
async def search_stream(
    first_name: Optional[str] = None, 
    last_name: Optional[str] = None, 
    username: Optional[str] = None, 
    email: Optional[str] = None, 
    dob: Optional[str] = None
):
    async def event_generator():
        yield json.dumps({"type": "progress", "value": 5, "message": "Инициализиране..."}) + "\n"
        
        all_breaches = []
        all_profiles = []
        
        # 1. Breaches
        yield json.dumps({"type": "progress", "value": 15, "message": "Търсене в бази данни с изтичания..."}) + "\n"
        
        full_name = f"{first_name or ''} {last_name or ''}".strip()
        all_breaches = search_local_breaches(name=full_name if first_name else None, email=email)
        
        # Add gravatar to EACH breach based on its own email
        for b in all_breaches:
            if b.get("Email"):
                b["Avatar"] = get_gravatar_url(b["Email"])

        yield json.dumps({"type": "breaches", "data": all_breaches}) + "\n"
        yield json.dumps({"type": "progress", "value": 30, "message": "Анализ на откритите течове..."}) + "\n"

        # 2. OSINT
        usernames = []
        if username: 
            usernames.append({"username": username, "score": 99})
            
        if first_name and last_name:
            generated = generate_usernames(first_name, last_name, dob)
            usernames.extend(generated[:8]) 
            
        seen = set()
        unique_usernames = []
        for u in usernames:
            if u["username"] not in seen:
                unique_usernames.append(u)
                seen.add(u["username"])
        
        # Fixed platform count
        PLATFORM_COUNT = 25
        total_checks = len(unique_usernames) * PLATFORM_COUNT
        completed = 0
        
        yield json.dumps({"type": "progress", "value": 40, "message": f"Сканиране на социални мрежи за {len(unique_usernames)} вариации..."}) + "\n"
        
        for un_data in unique_usernames:
            async for profile in search_profiles(un_data):
                completed += 1
                progress = 40 + int((completed / total_checks) * 55)
                if profile["status"] == "Found":
                    all_profiles.append(profile)
                    yield json.dumps({"type": "profile", "data": profile}) + "\n"
                
                if completed % 10 == 0:
                    yield json.dumps({"type": "progress", "value": min(progress, 95), "message": f"Проверка на профили... ({completed}/{total_checks})"}) + "\n"

        yield json.dumps({"type": "progress", "value": 100, "message": "Търсенето завърши успешно!"}) + "\n"
        yield json.dumps({"type": "done", "profiles": all_profiles, "breaches": all_breaches}) + "\n"

    return StreamingResponse(event_generator(), media_type="application/x-ndjson")

@app.post("/api/export")
async def export_endpoint(request: SearchRequest, format: str = "json"):
    results = await search_endpoint(request)
    if format.lower() == "xml":
        xml_bytes = dicttoxml.dicttoxml(results, custom_root='breacherr_report', attr_type=False)
        return {"data": xml_bytes.decode('utf-8'), "format": "xml"}
    return {"data": json.dumps(results, indent=4), "format": "json"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

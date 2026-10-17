from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

app = FastAPI()

# السماح للموقع (Netlify) بالاتصال بالسيرفر
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/web-audit")
def web_audit(req: Request):
    # جلب الـ IP الحقيقي للزائر (حتى لو كان خلف Proxy مثل Render)
    forwarded_for = req.headers.get("x-forwarded-for")
    if forwarded_for:
        client_ip = forwarded_for.split(",")[0].strip()
    else:
        client_ip = req.client.host if req.client else "Unknown"
    
    # طباعة الـ IP في السجلات (Logs) لكي تراها في Render
    print(f"🔥 WEB CLIENT - Visited from IP: {client_ip}")
    
    return {"status": "success", "verified_ip": client_ip}

if __name__ == "__main__":
    # هذا الجزء مهم جداً ليعمل السيرفر على Render
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

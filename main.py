from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
import os
import jwt
import json

# === CONFIGURATION JWT ===
SECRET_KEY = "votre_clé_secrète_très_longue"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# === FICHIERS & DOSSIERS ===
REPORTS_DIR = "reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

with open("backend/users.json", "r") as f:
    users = json.load(f)

# === INIT FASTAPI ===
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# === MODÈLES ===
class Token(BaseModel):
    access_token: str
    token_type: str

# === FONCTIONS D’AUTHENTIFICATION ===
def authenticate_user(username: str, password: str):
    user = users.get(username)
    if not user or user["password"] != password:
        return None
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token invalide")

# === ROUTE DE LOGIN ===
@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Identifiants incorrects")
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

# === ROUTE PROTÉGÉE TEST ===
@app.get("/protected")
async def protected_route(current_user=Depends(get_current_user)):
    return {"message": f"Bienvenue {current_user['sub']}, accès autorisé !"}

# === HOMEPAGE PUBLIQUE ===
@app.get("/")
def home():
    return {
        "message": "Bienvenue sur l’API ShadowSec AI 👋",
        "status": "🟢 En ligne",
        "endpoints": ["/token", "/scan", "/reports", "/summaries"]
    }

# === ROUTE DE SCAN (protégée) ===
@app.post("/scan")
async def launch_scan(current_user=Depends(get_current_user)):
    now = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"rapport_shadowsec_{now}.txt"
    report_path = os.path.join(REPORTS_DIR, filename)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"""ShadowSec AI Report - {now}

[Simulé] Scan Nmap : PORT 80/tcp ouvert (Apache)
[Simulé] Vulnérabilités SQLi : détectées
[Simulé] Vulnérabilités XSS : détectées
""")
    return {"message": "Scan lancé et rapport généré."}

# === ROUTE POUR VOIR LES RAPPORTS (protégée) ===
@app.get("/reports")
async def list_reports(current_user=Depends(get_current_user)):
    files = os.listdir(REPORTS_DIR)
    return [{"filename": f} for f in files if f.endswith(".txt")]

@app.get("/reports/{filename}")
async def get_report(filename: str, current_user=Depends(get_current_user)):
    filepath = os.path.join(REPORTS_DIR, filename)
    return FileResponse(filepath, media_type="text/plain", filename=filename)

# === PARSEUR DE RÉSUMÉ ===
def parse_report_summary(filename):
    filepath = os.path.join(REPORTS_DIR, filename)
    if not os.path.exists(filepath):
        return {"filename": filename, "summary": ["Rapport introuvable."]}
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    summary = []
    if "SQLi" in content:
        summary.append("SQLi détectée")
    if "XSS" in content:
        summary.append("XSS détectée")
    if "PORT" in content.upper():
        summary.append("Ports ouverts détectés")
    if "nginx" in content.lower() or "apache" in content.lower():
        summary.append("Serveur Web détecté")

    return {
        "filename": filename,
        "summary": summary if summary else ["Aucune vulnérabilité critique détectée"]
    }

@app.get("/summaries")
async def get_report_summaries(current_user=Depends(get_current_user)):
    summaries = []
    for file in os.listdir(REPORTS_DIR):
        if file.endswith(".txt"):
            summaries.append(parse_report_summary(file))
    return summaries
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)

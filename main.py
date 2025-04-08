from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from datetime import datetime

app = FastAPI()

# Autoriser les requêtes du frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Répertoire des rapports
REPORTS_DIR = "reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

# ✅ Page d’accueil
@app.get("/")
def home():
    return {
        "message": "Bienvenue sur l’API ShadowSec AI 👋",
        "status": "🟢 En ligne",
        "endpoints_disponibles": [
            "/scan",
            "/reports",
            "/reports/{filename}",
            "/summaries"
        ]
    }

# Endpoint GET /reports – Liste tous les rapports
@app.get("/reports")
def list_reports():
    files = os.listdir(REPORTS_DIR)
    return [{"filename": f} for f in files if f.endswith(".txt")]

# Endpoint GET /reports/{filename} – Récupère un rapport spécifique
@app.get("/reports/{filename}")
def get_report(filename: str):
    filepath = os.path.join(REPORTS_DIR, filename)
    return FileResponse(filepath, media_type="text/plain", filename=filename)

# Endpoint POST /scan – Génère un rapport simulé
@app.post("/scan")
def launch_scan():
    now = datetime.now().strftime("%Y%m%d_%H%M")
    report_path = os.path.join(REPORTS_DIR, f"rapport_shadowsec_{now}.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"""ShadowSec AI Report - {now}

[Simulé] Scan Nmap : PORT 80/tcp ouvert (Apache)
[Simulé] Vulnérabilités SQLi : détectées
[Simulé] Vulnérabilités XSS : détectées
""")
    return {"message": "Scan lancé et rapport généré."}

# Fonction d’analyse d’un rapport pour extraire un résumé
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

# Endpoint GET /summaries – Retourne les résumés pour tous les rapports
@app.get("/summaries")
def get_report_summaries():
    summaries = []
    for file in os.listdir(REPORTS_DIR):
        if file.endswith(".txt"):
            summaries.append(parse_report_summary(file))
    return summaries
from headers_scan import router as headers_router
app.include_router(headers_router)

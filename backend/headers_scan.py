
from fastapi import APIRouter, HTTPException
import requests

router = APIRouter()

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Content-Type-Options",
    "X-Frame-Options",
    "Referrer-Policy",
    "Permissions-Policy"
]

@router.get("/scan/headers")
def scan_headers(url: str):
    try:
        response = requests.get(url, timeout=10)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de la connexion à l’URL : {e}")

    result = {}
    for header in SECURITY_HEADERS:
        result[header] = response.headers.get(header, "Absent")

    return {
        "url": url,
        "headers_analysis": result
    }

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

@app.get("/")
def root():
    return {"message": "ShadowSec backend opérationnel"}

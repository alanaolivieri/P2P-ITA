import shutil
import pandas as pd
import subprocess
import os
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

ORIGEN = os.getenv("ORIGEN")
REPO = os.getenv("REPO")
ORGANIZACION = os.getenv("ORGANIZACION")
INFOGRAFIA = os.getenv("INFOGRAFIA")

print("CWD:", os.getcwd())
print("BASE_DIR:", BASE_DIR)
print("ORIGEN:", ORIGEN)
print("REPO:", REPO)
print("ORGANIZACION:", ORGANIZACION)
print("INFOGRAFIA:", INFOGRAFIA)

DESTINO = os.path.join(REPO, "p2p_latest.xlsx")
ORGANIZACION_DESTINO = os.path.join(REPO, "actividades.xlsx")
INFOGRAFIA_DESTINO = os.path.join(REPO, "infografia.jpg")

df = pd.read_excel(ORIGEN, sheet_name="Data 2026")
df.drop('Count', axis=1, inplace=True, errors='ignore')
df.to_excel(DESTINO, index=False)

df_org = pd.read_excel(ORGANIZACION, sheet_name="Organización")
df_org.to_excel(ORGANIZACION_DESTINO, index=False)

shutil.copy(INFOGRAFIA, INFOGRAFIA_DESTINO)

subprocess.run(["git", "add", "p2p_latest.xlsx", "actividades.xlsx", "infografia.jpg"], cwd=REPO, check=True)

status = subprocess.run(
    ["git", "status", "--porcelain"],
    cwd=REPO,
    capture_output=True,
    text=True,
    check=True
)

if status.stdout.strip():
    subprocess.run(
        [
            "git",
            "commit",
            "-m",
            f"Auto update P2P and organization activities {datetime.now():%Y-%m-%d %H:%M}"
        ],
        cwd=REPO,
        check=True
    )
    subprocess.run(["git", "push"], cwd=REPO, check=True)
else:
    print("No hay cambios para subir.")

time.sleep(10)
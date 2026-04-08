import pandas as pd
import subprocess
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

ORIGEN = os.getenv("ORIGEN")
REPO = os.getenv("REPO")
DESTINO = os.path.join(REPO, "p2p_latest.xlsx")

df = pd.read_excel(ORIGEN, sheet_name="Data 2026")
df.fillna('', inplace=True)
df.drop('Count', axis = 1, inplace=True)
df.to_excel(DESTINO, index=False)

subprocess.run(["git", "add", "p2p_latest.xlsx"], cwd=REPO, check=True)
subprocess.run(
    [
        "git",
        "commit",
        "-m",
        f"Auto update P2P {datetime.now():%Y-%m-%d %H:%M}"
    ],
    cwd=REPO,
    check=True
)
subprocess.run(["git", "push"], cwd=REPO, check=True)
# Diretorios 

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT.parent.mkdir(parents=True, exist_ok=True)

PDV_ROOT = Path(__file__).resolve().parents[1]
PDV_ROOT.parent.mkdir(parents=True, exist_ok=True)

PDV_NEW_FILES_DIR = PROJECT_ROOT / "pdv_sales" / "pdv_new_files"
PDV_NEW_FILES_DIR.parent.mkdir(parents=True, exist_ok=True)

CATALOGO_FILE = PDV_ROOT / "data" / "produtos" / "catalogo.csv"
CATALOGO_FILE.parent.mkdir(parents=True, exist_ok=True)

LOJAS_FILE = PDV_ROOT / "data" / "lojas" / "lojas.csv"
LOJAS_FILE.parent.mkdir(parents=True, exist_ok=True)
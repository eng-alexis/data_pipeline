# Diretorios 

from pathlib import Path

PDV_ROOT = Path(__file__).resolve().parents[1]
PDV_ROOT.parent.mkdir(parents=True, exist_ok=True)

CATALOGO_FILE = PDV_ROOT / "data" / "produtos" / "catalogo.csv"
CATALOGO_FILE.parent.mkdir(parents=True, exist_ok=True)

LOJAS_FILE    = PDV_ROOT / "data" / "lojas" / "lojas.csv"
LOJAS_FILE.parent.mkdir(parents=True, exist_ok=True)
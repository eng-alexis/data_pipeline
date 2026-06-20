# Diretorios 

from pathlib import Path

PDV_ROOT = Path(__file__).resolve().parents[1]

CATALOGO_FILE = PDV_ROOT / "data" / "produtos" / "catalogo.csv"
LOJAS_FILE    = PDV_ROOT / "data" / "lojas" / "lojas.csv"
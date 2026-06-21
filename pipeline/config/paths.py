# Diretorios e scripts

from pathlib import Path

PIPELINE_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT  = Path(__file__).resolve().parents[2]

JSON_EVENTS_DIR    = PROJECT_ROOT / "pdv_simulator" / "pdv_sales" 
JSON_DATABASE_DIR  = PROJECT_ROOT / "pdv_simulator" / "pdv_sales" / "database"

JSON_PROCESSED_DIR = PIPELINE_ROOT / "processed_files" / "arq_processados"
JSON_DUPLICATE_DIR = PIPELINE_ROOT / "processed_files" / "arq_duplicados"

SQL_LOAD_TO_EVENTOS  = PIPELINE_ROOT / "src" / "silver" / "load" / "sql" / "load_to_eventos.sql"
SQL_LOAD_TO_PRODUTOS = PIPELINE_ROOT / "src" / "silver" / "load" / "sql" / "load_to_produtos.sql"
SQL_LOAD_TO_LOJAS    = PIPELINE_ROOT / "src" / "silver" / "load" / "sql" / "load_to_lojas.sql"
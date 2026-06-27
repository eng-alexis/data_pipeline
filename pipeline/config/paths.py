# Diretorios e scripts

from pathlib import Path

PIPELINE_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT  = Path(__file__).resolve().parents[2]

JSON_EVENTS_DIR    = PROJECT_ROOT / "pdv_simulator" / "pdv_sales" 
JSON_EVENTS_DIR.mkdir(parents=True, exist_ok=True)

JSON_DATABASE_DIR  = PROJECT_ROOT / "pdv_simulator" / "pdv_sales" / "database"

JSON_PROCESSED_DIR = PIPELINE_ROOT / "processed_files" / "arq_processados"
JSON_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

JSON_DUPLICATE_DIR = PIPELINE_ROOT / "processed_files" / "arq_duplicados" 
JSON_DUPLICATE_DIR.mkdir(parents=True, exist_ok=True)

SQL_LOAD_TO_EVENTOS  = PIPELINE_ROOT / "src" / "silver" / "load" / "sql" / "load_to_eventos.sql"
SQL_LOAD_TO_PRODUTOS = PIPELINE_ROOT / "src" / "silver" / "load" / "sql" / "load_to_produtos.sql"
SQL_LOAD_TO_LOJAS    = PIPELINE_ROOT / "src" / "silver" / "load" / "sql" / "load_to_lojas.sql"

SQL_LOAD_TO_FATO_VENDAS  = PIPELINE_ROOT / "src" / "gold" / "load" / "sql" / "load_to_fato_vendas.sql"
SQL_LOAD_TO_DIM_PRODUTOS = PIPELINE_ROOT / "src" / "gold" / "load" / "sql" / "load_to_dim_produtos.sql"
SQL_LOAD_TO_DIM_LOJAS    = PIPELINE_ROOT / "src" / "gold" / "load" / "sql" / "load_to_dim_lojas.sql"
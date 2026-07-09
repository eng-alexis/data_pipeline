# Diretorios e scripts

from pathlib import Path

PIPELINE_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT  = Path(__file__).resolve().parents[2]

PDV_NEW_FILES_DIR = PROJECT_ROOT / "pdv_sales" / "pdv_new_files"
PDV_NEW_FILES_DIR.mkdir(parents=True, exist_ok=True)

# JSON_DATABASE_DIR  = PROJECT_ROOT / "pdv_sales" / "database"

PIPE_PROCESSED_FILES_DIR = PROJECT_ROOT / "pdv_sales" / "pipe_processed_files"
PIPE_PROCESSED_FILES_DIR.mkdir(parents=True, exist_ok=True)

PIPE_DUPLICATE_FILES_DIR = PROJECT_ROOT / "pdv_sales" / "pipe_reject_files" / "duplicated_file"
PIPE_DUPLICATE_FILES_DIR.mkdir(parents=True, exist_ok=True)

PIPE_INVALID_ENTITY_DIR = PROJECT_ROOT / "pdv_sales" / "pipe_reject_files" / "invalid_entity"
PIPE_INVALID_ENTITY_DIR.mkdir(parents=True, exist_ok=True)

PIPE_EMPTY_FILES_DIR = PROJECT_ROOT / "pdv_sales" / "pipe_reject_files" / "empty_files"
PIPE_EMPTY_FILES_DIR.mkdir(parents=True, exist_ok=True)

SQL_LOAD_TO_EVENTOS  = PIPELINE_ROOT / "src" / "silver" / "load" / "sql" / "load_to_eventos.sql"
SQL_LOAD_TO_PRODUTOS = PIPELINE_ROOT / "src" / "silver" / "load" / "sql" / "load_to_produtos.sql"
SQL_LOAD_TO_LOJAS    = PIPELINE_ROOT / "src" / "silver" / "load" / "sql" / "load_to_lojas.sql"

SQL_LOAD_TO_FATO_VENDAS  = PIPELINE_ROOT / "src" / "gold" / "load" / "sql" / "load_to_fato_vendas.sql"
SQL_LOAD_TO_DIM_PRODUTOS = PIPELINE_ROOT / "src" / "gold" / "load" / "sql" / "load_to_dim_produtos.sql"
SQL_LOAD_TO_DIM_LOJAS    = PIPELINE_ROOT / "src" / "gold" / "load" / "sql" / "load_to_dim_lojas.sql"
SQL_LOAD_TO_DIM_CALENDARIO = PIPELINE_ROOT / "src" / "gold" / "load" / "sql" / "load_to_dim_calendario.sql"
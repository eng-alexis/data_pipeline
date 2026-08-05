# Como executar

## Pré requisitos

Antes de executar o projeto, certifique-se de possuir:

- Windows 11 ou Linux
- WSL2 (recomendado para Windows)
- Docker Desktop 28+
- Git
- Python 3.12+
- PostgreSQL
- Power BI Desktop (opcional, apenas para visualização dos dashboards)

## Guia de instalação (Linux)

```bash
#1. Clone o repositório:
git clone git@github.com:eng-alexis/data_pipeline.git

#2. Acesse a pasta do projeto:
cd data_pipeline

#3. Crie o ambiente virtual
python3 -m venv .venv

#4. Ative o ambiente virtual
source .venv/bin/activate

#5. Instale as dependências
pip install -r requeriments.txt

#6. Configure o arquivo
cp .env.example .env

#7. Inicie os containers
docker-compose up -d
```
---
## Executando o projeto

### 1. Gerar arquivos de vendas através do pdv_simulator

No terminal (Linux):
```bash
python3 -m pdv_simulator.simulador.pdv_main
```

Digite a `data inicial` e `data final` no input respeitando o formato de entrada (YYYY-MM-DD).
```bash
# 1° input -> digite a data inicial (ex: 2026-01-01):
 2020-01-01

# 2° input -> digite a data final (ex: 2026-01-02): 
 2020-01-02
```

### 2. Executar pipeline
```bash
python3 -m pipeline.orquestrador.pipeline_main
```
### 3. Ver resultados
Verifique os resultados do pipeline acessado o banco de dados `pdv_sales` e executando queries SQL.

#### 3.1 -  Acesse o banco postgres no container
No terminal (Linux):

```bash
#1. Entrar no container postgres
docker exec -it postgres bash

#2. Acessar o banco pdv_sales
psql -U admin -d pdv_sales
```

#### 3.2 - Execute queries SQL

```bash
# Retornar histórico de ciclos de execuções do pipeline.
SELECT * FROM audit.pipeline_cycle LIMIT 10;

# Retornar histórico de execuções do pipeline.
SELECT * FROM audit.pipeline_execution LIMIT 10;

# Retornar amostra da registros do schema RAW
SELECT * FROM raw.eventos LIMIT 10;

# Retornar amostra da registros do schema SILVER
SELECT * FROM silver.eventos LIMIT 10;
SELECT * FROM silver.produtos ORDER BY id_produto LIMIT 10;

# Retornar amostra da registros do schema GOLD
SELECT * FROM gold.fato_vendas LIMIT 10;
SELECT * FROM gold.dim_calendario ORDER BY data LIMIT 10;
```

### 4. Acessar relatorio de BI (windows)

#### 4.1 - Realize o download do dashboard em sua maquina.

[**Clique Aqui**](../dashboard/power_bi/) para acessar o local arquivo do dashboard.

local do arquivo: `data_pipeline/dashboard/power_bi/dash_pdv_sales.pbix`

#### 4.2 - Após realizar o download, abra o arquivo em sua maquina utilizando o Power BI Desktop.
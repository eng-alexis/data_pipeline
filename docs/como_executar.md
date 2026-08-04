## Como executar

### Pré requisitos

Antes de executar o projeto, certifique-se de possuir:

- Windows 11 ou Linux
- WSL2 (recomendado para Windows)
- Docker Desktop 28+
- Git
- Python 3.12+
- PostgreSQL
- Power BI Desktop (opcional, apenas para visualização dos dashboards)

### Guia de instalação (Linux)

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
### Executando o projeto

#### 1. Gerar arquivos de vendas através do pdv_simulator

No terminal (Linux):
```bash
python3 -m pdv_simulator.simulador.pdv_main
```

Digite a `data inicial` e `data final` no input respeitando o formato YYYY-MM-DD.
```bash
# 1° input -> digite a data inicial (ex: 2026-01-01):
 2020-01-01

# 2° input -> digite a data final (ex: 2026-01-01): 
 2020-01-02
```

#### 2. Executar pipeline
```bash
python3 -m pipeline.orquestrador.pipeline_main
```
#### 3. Abrir dashboard (Windows)

Realize o download do dashboard.
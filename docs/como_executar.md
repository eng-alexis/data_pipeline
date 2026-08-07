# Como executar

## Pré-requisitos

Antes de executar o projeto, certifique-se de possuir:

* Windows 11 ou Linux
* WSL2 — recomendado para usuários Windows
* Docker Desktop 28+
* Git
* Python 3.12+
* Power BI Desktop — opcional, necessário apenas para visualizar o dashboard

> **Observação:** o PostgreSQL utilizado pelo projeto é executado em um container Docker. Portanto, não é necessário instalar o PostgreSQL diretamente na máquina.

---

## 1. Instalação

### Linux

#### 1.1 Clone o repositório

```bash
git clone git@github.com:eng-alexis/data_pipeline.git
```

#### 1.2 Acesse a pasta do projeto

```bash
cd data_pipeline
```

#### 1.3 Crie o ambiente virtual Python

```bash
python3 -m venv .venv
```

#### 1.4 Ative o ambiente virtual

```bash
source .venv/bin/activate
```

#### 1.5 Instale as dependências

```bash
pip install -r requirements.txt
```

#### 1.6 Configure as variáveis de ambiente

Crie o arquivo `.env` a partir do arquivo de exemplo:

```bash
cp .env.example .env
```

Caso necessário, revise as variáveis presentes no `.env` antes de continuar.

#### 1.7 Inicie os containers

```bash
docker-compose up -d
```

Verifique se os containers foram iniciados corretamente:

```bash
docker ps
```

---

## 2. Executando o projeto

A execução do projeto é realizada em duas etapas:

1. Geração dos arquivos de vendas pelo `pdv_simulator`
2. Execução do pipeline de dados

### 2.1 Gerar arquivos de vendas

Com o ambiente virtual ativado, execute:

```bash
python3 -m pdv_simulator.simulador.pdv_main
```

O simulador solicitará uma **data inicial** e uma **data final**.

Informe as datas no formato `YYYY-MM-DD`.

Exemplo:

```text
1º input — data inicial:
2020-01-01

2º input — data final:
2020-01-02
```

Ao finalizar, o simulador exibe no terminal um resumo com informações sobre a simulação:

```text
• Duração (minutos) do simulador
• Total de dias simulados
• Total de arquivos gerados
```

### 2.2 Executar o pipeline

Após a geração dos arquivos, execute o pipeline:

```bash
python3 -m pipeline.orquestrador.pipeline_main
```

O orquestrador inicia um **ciclo do pipeline**.

Durante um ciclo, um ou mais arquivos podem ser processados. Cada arquivo processado corresponde a uma **execução do pipeline**.

**Conceitos utilizados no projeto:**

* **Ciclo:** uma execução do orquestrador. Pode conter uma ou várias execuções do pipeline.
* **Execução:** processamento de um único arquivo durante um ciclo.

Exemplo:

```text
1 ciclo
 ├── execução 1 → arquivo_001.json
 ├── execução 2 → arquivo_002.json
 └── execução 3 → arquivo_003.json
```

Ao finalizar o ciclo, o orquestrador exibe no terminal um resumo com informações sobre o processamento:

```text
• Nº do ciclo
• Duração (minutos) do ciclo
• Quantidade de arquivos localizados
• Quantidade de arquivos processados
• Quantidade de arquivos rejeitados
• Tamanho total dos arquivos (MB)
• Quantidade de registros válidos
• Quantidade de registros inválidos
```

## 3. Verificando os resultados

Após a execução do pipeline, os resultados podem ser verificados diretamente no banco de dados `pdv_sales`.

### 3.1 Acessar o PostgreSQL

Como o PostgreSQL está sendo executado em um container Docker, acesse o container:

```bash
docker exec -it postgres bash
```

Em seguida, acesse o banco de dados:

```bash
psql -U admin -d pdv_sales
```

### 3.2 Consultar os dados

#### Histórico dos ciclos de execução

Retorna o histórico dos ciclos de execução do pipeline:

```sql
SELECT * FROM audit.pipeline_cycle LIMIT 10;
```

#### Histórico das execuções

Retorna o histórico das execuções do pipeline:

```sql
SELECT * FROM audit.pipeline_execution LIMIT 10;
```

#### Dados da camada RAW

Retorna uma amostra dos registros armazenados na camada RAW:

```sql
SELECT * FROM raw.eventos LIMIT 10;
```

#### Dados da camada SILVER

Retorna uma amostra dos registros de eventos:

```sql
SELECT * FROM silver.eventos LIMIT 10;
```

Retorna uma amostra dos produtos ordenados pelo identificador:

```sql
SELECT * FROM silver.produtos
ORDER BY id_produto
LIMIT 10;
```

#### Dados da camada GOLD

Retorna uma amostra da tabela fato de vendas:

```sql
SELECT * FROM gold.fato_vendas LIMIT 10;
```

Retorna uma amostra da dimensão calendário:

```sql
SELECT * FROM gold.dim_calendario
ORDER BY data
LIMIT 10;
```

---

## 4. Visualizar o dashboard

O projeto possui um dashboard desenvolvido no Power BI.

### 4.1 Baixar o arquivo

O arquivo `.pbix` está disponível no diretório:

```text
dashboard/power_bi/dash_pdv_sales.pbix
```

Acesse o diretório [dashboard/power_bi](../dashboard/power_bi/) para baixar o arquivo.

### 4.2 Abrir o dashboard

Após baixar o arquivo, abra:

```text
dash_pdv_sales.pbix
```

utilizando o **Power BI Desktop**.

> **Observação:** o Power BI Desktop é necessário apenas para visualizar o dashboard. Ele não é necessário para executar o `pdv_simulator` ou o pipeline.

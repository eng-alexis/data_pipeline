# Pipeline

O pipeline é responsável por processar os dados gerados pelo `pdv_simulator`, realizando sua ingestão, validação, padronização, transformação e disponibilização para análise.

O processamento é dividido em camadas, permitindo separar as responsabilidades de cada etapa e manter um fluxo organizado de tratamento dos dados.

```text
Arquivos de origem
       │
       ▼
┌─────────────────┐
│   Orquestrador  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│      RAW        │
│ Ingestão e      │
│ validação       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     SILVER      │
│ Padronização e  │
│ tratamento      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│      GOLD       │
│ Transformação e │
│ disponibilização│
└────────┬────────┘
         │
         ▼
     Power BI
```

---

# Arquitetura do pipeline

O pipeline é organizado em três camadas principais:

| Camada     | Responsabilidade                                                | Resultado                          |
| ---------- | --------------------------------------------------------------- | ---------------------------------- |
| **Raw**    | Ingestão, validação inicial e armazenamento dos dados de origem | Dados brutos registrados no banco  |
| **Silver** | Padronização, limpeza e aplicação de tratamentos                | Dados estruturados e tratados      |
| **Gold**   | Transformação dos dados para consumo analítico                  | Dados preparados para análise e BI |

Além das camadas de dados, o pipeline possui um **orquestrador**, responsável por controlar a execução do fluxo.

---

# Orquestrador

O orquestrador é responsável por controlar a execução do pipeline, determinar a ordem de execução das camadas e controlar o comportamento da aplicação em caso de exceções.

### Objetivos

* Gerar o ID de contexto da execução.
* Localizar os arquivos de entrada.
* Extrair informações e metadados dos arquivos.
* Executar as camadas do pipeline na ordem correta.
* Controlar exceções.
* Registrar informações de auditoria.
* Encerrar a execução quando uma etapa crítica apresentar erro.

### Fluxo

```text
Orquestrador
     │
     ▼
Localização dos arquivos
     │
     ▼
Geração do ID da execução
     │
     ▼
    RAW
     │
     ▼
   SILVER
     │
     ▼
    GOLD
     │
     ▼
Fim da execução
```

### Entradas

| Parâmetro         | Descrição                                             |
| ----------------- | ----------------------------------------------------- |
| `path_files`      | Caminho do diretório contendo os arquivos de entrada. |
| `tipos_esperados` | Extensões de arquivos que devem ser processadas.      |

### Regras

* Apenas arquivos nos formatos `.json` e `.jsonl` são processados.
* O pipeline processa um único arquivo por execução.
* As camadas são executadas sequencialmente.
* Caso uma etapa apresente uma exceção não tratada, a execução é interrompida.
* Informações relevantes da execução são registradas para fins de auditoria.

Para obter detalhes sobre sua implementação, consulte a [documentação do orquestrador](orquestrador/README.md).

---

# Camada Raw

A camada **Raw** é responsável pela ingestão dos dados de origem e pela preservação das informações recebidas.

Nessa etapa são realizadas validações iniciais para garantir que os dados possam ser armazenados de forma segura no pipeline.

### Responsabilidades

* Receber os arquivos de origem.
* Extrair informações e metadados dos arquivos.
* Identificar arquivos já processados.
* Validar o schema dos registros.
* Separar registros inválidos.
* Armazenar registros válidos.
* Registrar informações de processamento.
* Controlar arquivos processados e duplicados.

### Fluxo

```text
Arquivo de origem
       │
       ▼
Extração de metadados
       │
       ▼
Validação do arquivo
       │
       ▼
Verificação de duplicidade
       │
       ├── Duplicado → reject_files/duplicated_file/
       │
       ▼
Validação do schema
       │
       ├── Inválido → Quarantena
       │
       ▼
Inserção dos registros
       │
       ▼
Registro de auditoria
```

A camada Raw **não tem como objetivo realizar transformações complexas nos dados**. Seu principal objetivo é garantir que os dados recebidos sejam corretamente registrados e rastreáveis.

Para obter detalhes sobre sua implementação, consulte a [documentação da camada Raw](src/raw/README.md).

---

# Camada Silver

A camada **Silver** é responsável pelo tratamento e padronização dos dados provenientes da camada Raw.

Nesta etapa os dados são preparados para que possam ser utilizados de maneira consistente pelas etapas posteriores do pipeline.

### Responsabilidades

* Ler os dados disponibilizados pela camada Raw.
* Padronizar informações.
* Realizar tratamentos e conversões necessárias.
* Aplicar regras de qualidade dos dados.
* Preparar os dados para a camada Gold.
* Registrar informações da execução.

### Fluxo

```text
Dados Raw
   │
   ▼
Leitura dos dados
   │
   ▼
Tratamentos
   │
   ▼
Padronização
   │
   ▼
Validações
   │
   ▼
Dados Silver
```

A camada Silver representa o estado **tratado e padronizado** dos dados, reduzindo inconsistências e preparando as informações para as transformações analíticas.

Para obter detalhes sobre sua implementação, consulte a [documentação da camada Silver](src/silver/README.md).

---

# Camada Gold

A camada **Gold** é responsável por transformar os dados tratados da camada Silver em estruturas destinadas ao consumo analítico.

Nesta etapa são aplicadas as regras necessárias para disponibilizar os dados de forma adequada para ferramentas de análise e visualização.

### Responsabilidades

* Consumir os dados da camada Silver.
* Aplicar transformações analíticas.
* Criar estruturas dimensionais e/ou fatos.
* Aplicar regras de negócio necessárias à análise.
* Disponibilizar os dados para consumo pelo Power BI.

### Fluxo

```text
Dados Silver
     │
     ▼
Transformações
     │
     ▼
Regras de negócio
     │
     ▼
Modelagem analítica
     │
     ▼
Dados Gold
     │
     ▼
Power BI
```

A camada Gold representa a camada de **consumo analítico** do pipeline.

Para obter detalhes sobre sua implementação, consulte a [documentação da camada Gold](src/gold/README.md).

---

# Fluxo completo dos dados

Considerando todas as etapas, o fluxo do pipeline pode ser representado da seguinte forma:

```text
                 PDV_SIMULATOR
                       │
                       ▼
              Arquivos JSON / JSONL
                       │
                       ▼
              ┌─────────────────┐
              │   ORQUESTRADOR  │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │      RAW        │
              │                 │
              │ Ingestão        │
              │ Validação       │
              │ Auditoria       │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │     SILVER      │
              │                 │
              │ Tratamento      │
              │ Padronização    │
              │ Qualidade       │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │      GOLD       │
              │                 │
              │ Transformação   │
              │ Modelagem       │
              │ Regras negócio  │
              └────────┬────────┘
                       │
                       ▼
                   POWER BI
```

---

# Controle e auditoria

O pipeline possui mecanismos de controle para permitir o acompanhamento das execuções.

Durante o processamento são registradas informações relacionadas à execução, permitindo identificar:

* qual execução está sendo realizada;
* quais arquivos foram processados;
* quais etapas foram executadas;
* quantidade de registros processados;
* ocorrências de erros;
* registros rejeitados ou enviados para quarentena;
* situação da execução.

O uso de um ID de execução permite relacionar as informações produzidas pelas diferentes etapas de um mesmo processamento.

---

# Tratamento de exceções

As exceções são controladas pelo orquestrador.

De forma geral:

```text
Execução
   │
   ▼
Camada atual
   │
   ├── Sucesso ──────────► Próxima camada
   │
   └── Exceção
          │
          ▼
     Registro de
       auditoria
          │
          ▼
    Encerramento da
       execução
```

Caso uma etapa apresente uma exceção que impeça a continuidade do processamento, o pipeline interrompe a execução e registra as informações disponíveis para permitir a identificação do problema.

---

# Estrutura do projeto

```text
pipeline/
│
├── common/
│
├── config/
│
├── database/
│
├── src/
│   ├── raw/
│   │   └── README.md
│   │
│   ├── silver/
│   │   └── README.md
│   │
│   └── gold/
│       └── README.md
│
├── orquestrador/
│   └── README.md
│
└── README.md
```

### Principais diretórios

| Diretório       | Responsabilidade                                    |
| --------------- | --------------------------------------------------- |
| `common/`       | Recursos compartilhados entre as etapas do projeto. |
| `config/`       | Configurações utilizadas pelo pipeline.             |
| `database/`     | Scripts e recursos relacionados ao banco de dados.  |
| `src/raw/`      | Implementação da camada Raw.                        |
| `src/silver/`   | Implementação da camada Silver.                     |
| `src/gold/`     | Implementação da camada Gold.                       |
| `orquestrador/` | Controle da execução do pipeline.                   |

---

# Documentação das camadas

Para informações específicas sobre cada etapa, consulte:

* [Documentação do orquestrador](orquestrador/README.md)
* [Documentação da camada Raw](src/raw/README.md)
* [Documentação da camada Silver](src/silver/README.md)
* [Documentação da camada Gold](src/gold/README.md)
* [Guia de execução](../docs/como_executar.md)

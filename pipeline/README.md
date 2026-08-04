# Pipeline

O pipeline realiza a extração, validação, padronização, transformação e disponibilização dos dados de origem utilizando camadas.

## Orquestrador do pipeline

O orquestrador é responsavel por executar todas as camadas do pipeline e decidir comportamento após exception.

### Objetivo

* Gerar id de contexto da execução. 
* Localizar e extrair arquivos.
* Executar as camadas do pipeline.
* Lidar com exceções.
* Registrar informações de auditoria.

###  Fluxo do orquestrador

    Orquestrador
    ↓
    Camada RAW
    ↓
    Camada Silver
    ↓
    Camada Gold

### Entradas

|Parâmetro | Descrição|
|-----|-----|
|path_files | caminho do diretorio dos arquivos json e jsonl.|
|tipos_esperados | extensões de arquivos que serão buscados.|

### Regras

- Apenas arquivos no formato .json e .jsonl são permitidos.
- O pipeline processa um unico arquivo por execução.
- Qualquer exceção resulta no interrompimento da execução do pipeline.

### Fluxo do processamento

1. Localiza os arquivos json e jsonl no diretorio
2. Extrai informações e metadados do arquivo
3. Gera id da execução atual (contexto do pipeline)
4. Executa a camada Raw
5. Executa a camada Silver
6. Executa a camada Gold
7. Executa a camada Gold (dim_calendario)
8. Em caso de exceção:
* Encerra execução atual;
* Registro de auditoria.
9. Encerra o ciclo do pipeline.

## Arquitetura

```
pipeline/
│
├── common/
├── config/
├── database/
│
├── src/
│   ├── raw/
│   ├── silver/
│   ├── gold/
│
├── orquestrador/
│
└── README.md
```

## Links para documentações

[**Clique Aqui**](src/raw/README.md) para ver a documentação da camada raw

[**Clique Aqui**](src/silver/README.md) para ver a documentação da camada silver

[**Clique Aqui**](src/gold/README.md) para ver a documentação da camada gold
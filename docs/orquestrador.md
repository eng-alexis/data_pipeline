# Orquestrador do pipeline

O orquestrador é responsavel por executar todas as camadas do pipeline e  decidir comportamento após exception.

## Objetivo

* Gerar id de contexto da execução. 
* Executar as camadas do pipeline.
* Lidar com exceções.
* Registrar informações de auditoria sobre a execução.
* Registrar informações de auditoria sobre o ciclo.

##  Fluxo do orquestrador

    Orquestrador
    ↓
    Camada RAW
    ↓
    Camada Silver
    ↓
    Camada Gold
    ↓
    Relatorio BI

## Entradas

Parâmetro | Descrição
-----|-----
path_files | caminho do diretorio dos arquivos json e jsonl.
tipos_esperados | extensões de arquivos que serão buscados

## Regras

- Apenas arquivos no formato .json e .jsonl são permitidos.
- O pipeline processa um unico arquivo por execução.
- Qualquer exceção resulta no interrompimento da execução do pipeline.

## Fluxo do processamento

2. Localiza os arquivos json e jsonl no diretorio
3. Extrai informações e metadados do arquivo
4. Gera id da execução atual (contexto do pipeline)
5. Executa a camada Raw
6. Executa a camada Silver
7. Executa a camada Gold
8. Executa a camada Gold (dim_calendario)
9. Em caso de exceção:
* Encerra execução atual;
* Registro de auditoria.
10. Encerra o ciclo do pipeline.
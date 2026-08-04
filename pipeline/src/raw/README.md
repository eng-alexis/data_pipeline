# Camada RAW

A camada Raw é responsável pela ingestão dos arquivos gerados pelo sistema de origem, realizando validações iniciais e persistindo os registros no banco de dados sem aplicar transformações de negócio.

## Objetivo

* Receber arquivos JSON/JSONL enviados pelo orquestrador.
* Garantir que apenas arquivos inéditos sejam processados.
* Validar a estrutura dos registros.
* Armazenar os dados brutos e encaminhar registros inválidos para quarentena.
* Registrar informações de auditoria sobre o processamento.

## Fluxo da camada

    Orquestrador
    ↓
    Validação
    ↓
    Persistência
    ↓
    Auditoria
    ↓
    Proxima camada (SILVER)

## Entradas

|Parâmetro |	Descrição|
|----- | -----|
|execucao_id | Identificador da execução do pipeline.|
|arquivo | Arquivo JSON ou JSONL a ser processado.|

## Saidas

Ao final da execução, a camada retorna:

Campo |	Descrição
----- | -----
id_arquivo | Identificador do arquivo na auditoria.
nome_arquivo | Nome final do arquivo processado.
hash_arquivo | Hash utilizado para controle de duplicidade.
registros_invalidos | Quantidade de registros invalidos.

## Regras

- Arquivos duplicados não são reprocessados.
- Apenas registros com schema válido são carregados.
- Registros inválidos são enviados para quarentena.
- O processamento ocorre em lotes de registros com tamanho pré-definido.
- Toda execução gera registros de auditoria.

## Fluxo de processamento

A camada raw:

1. Recebe id da execução e path do arquivo json/jsonl.
2. Define um hash calculado para o arquivo com base em seu conteudo.
3. Verifica se o arquivo já foi processado anteriormente através do hash calculado.
4. Caso o arquivo já tenha sido processado anteriormente:
* move o arquivo para a pasta de duplicados;
* registra o evento na auditoria;
* encerra a execução da camada.
5. Caso o arquivo não tenha sido processado anteriormente:
* Extrai e valida cada registro do arquivo utilizando contrato de schema;
* Persiste registros invalidos na tabela de quarentena;
* Persiste os registros válidos em lotes na camada Raw;
* Persiste os registros dos lotes na tabela raw.eventos.
6. Após o processamento:
* Renomeia o arquivo adicionando data e hora ao nome;
* Move o arquivo para pasta de arquivos processados.
* Registra informações de auditoria da camada.

## Transação

Durante o carregamento dos registros, todas as inserções são executadas dentro de uma transação.

Caso ocorra qualquer falha:

- rollback da transação;
- atualização da auditoria;
- encerramento da execuçao da camada.

## Exceções

Durante a execução da camada raw, as seguintes exceções podem ser disparadas:

|Exceção | Descrição|
|----- | -----|
|UnknownEntityException | Entidade do arquivo não suportada.|
|DuplicateFileException | O hash do arquivo já existe.|
|EmptyfileExcept | O arquivo esta vazio.|
|InsertRecordsFail | Erro inesperado no carregamento dos registros na tabela.|
|AllRecordsQuarantinedException | Todos os registros do arquivo são inválidos.|
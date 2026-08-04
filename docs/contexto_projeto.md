## Contexto

Uma pequena rede de supermercados utiliza um sistema PDV responsavel pelo registro de eventos de vendas de cada loja diariamente.

Todos os dias o sistema PDV disponibiliza:

* arquivos jsonl contento todos os eventos relacionados as vendas do dia anterior.
* arquivo json contento catalogo de produtos.
* arquivo json contendo informações de cada loja.

todos esses arquivos são persistidos no computador do proprietario da rede de supermercados.

## Problemas

- 1. Os arquivos permanecem armazenados exclusivamente no computador do proprietário da rede. Dessa forma, os dados dependem da disponibilidade e integridade desse equipamento.
Uma falha no armazenamento ou uma exclusão indevida pode comprometer o histórico de vendas e dificultar sua recuperação.

- 2. Os dados de vendas estão disponíveis apenas nos arquivos gerados pelo PDV e não estão organizados em uma estrutura adequada para análises e construção de indicadores de BI.
- 3. Não existe um contrato de dados que defina a estrutura esperada dos arquivos e registros recebidos pelo pipeline. Alterações ou registros inválidos podem, portanto, chegar ao processamento sem uma validação formal.

## Solução

Desenvolver um pipeline de dados responsável por receber os arquivos
gerados pelo sistema PDV, armazená-los de forma estruturada, validar e
tratar os registros e disponibilizar os dados processados para análise.

O pipeline deverá:

* Armazenar os registros no banco de dados;
* Realizar a padronização, limpeza e tratamento dos dados.
* Disponibizar dados prontos para analises;
* Registrar um historico de execuções do pipeline;
* Rodar diariamente de forma automatizada.

## O projeto deverá:

- Criar um banco de dados responsável por armazenar os dados do PDV;
- Garantir a qualidade e confiabilidade dos dados;
- Registrar o histórico de execução do pipeline;
- Disponibilizar dados tratados para BI;
- Desenvolver um relatório com principais métricas e indicadores;
- Identificar e tratar arquivos inválidos;

## Comparativo

### Situação atual

```bash
PDV
 ↓
Arquivos JSON / JSONL
 ↓
Computador local
```

### Situação proposta

```bash
PDV
 ↓
Arquivos JSON / JSONL
 ↓
Pipeline
 ├── Validação
 ├── Tratamento
 ├── Deduplicação
 ├── Auditoria
 └── Persistência
 ↓
Banco de dados
 ↓
Dados analíticos
 ↓
Power BI
```

## Escopo

Este projeto contempla:

- ingestão dos arquivos gerados pelo PDV;
- validação dos registros;
- tratamento e padronização dos dados;
- identificação de duplicidades;
- armazenamento dos dados;
- auditoria das execuções;
- disponibilização dos dados para BI;
- geração de indicadores de negócio.

## Fora do escopo

O projeto não tem como objetivo desenvolver ou substituir o sistema PDV
utilizado pelas lojas. O PDV é tratado como a origem dos dados.
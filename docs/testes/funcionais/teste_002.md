# TESTE-002 - PIPELINE

Este teste tem como objetivo: validar o processamento e a integridade dos dados ao longo das camadas `Raw`, `Silver` e `Gold`.

## Status

✅ PASSOU

## Data do teste
14/08/2026

## 1. Origem dos arquivos

### Simulador
PDV Simulator

### Período simulado:

`01/01/2025` → `10/01/2025`

**10** dias simulados

### Quantidade de arquivos gerados

**22** arquivos gerados
       
## 2. Executar o Pipeline

**Comando**:
```text
python3 -m pipeline.orquestrador.pipeline_main
```

---

## 3. Validação RAW

#### Validações:

| Validação                          | Resultado |
| -----------------------------------| :-------: |
| Quantidade de arquivos processados | ✅       |
| Quantidade de registros validos    | ✅       |
| Quantidade de registros invalidos  | ✅       |

---

### 3.1 Quantidade de arquivos processados

#### Objetivo:

Verificar se todos os `22` arquivos gerados pelo simulador foram processados pela camada RAW.

#### Consulta:

```SQL
SELECT COUNT(*) FROM audit.file_history WHERE status = 'PROCESSADO';
``` 

#### Resultado:

```text
22 arquivos processados pelo pipeline.
```
#### Conclusão:

O numero de arquivos processados (22) corresponde ao numero exato de arquivos gerados pelo simulador (22).

#### Status: ✅ PASSOU

---

### 3.2 Quantidade de registros validos

#### Objetivo:

Verificar a quantidade de registros validos.

#### Consulta:

```SQL
SELECT COUNT(*) FROM raw.eventos;
``` 

#### Resultado:

```text
28.241 registros válidos
```

#### Conclusão: 

Durante a execução, o pipeline processou `28.241` registros **validos**.

#### Status: ✅ PASSOU

---

### 3.3 Quantidade de registros invalidos

#### Objetivo: 

Verificar a existencia de registros invalidos.

#### Consulta:

```SQL
SELECT COUNT(*) FROM raw.quarantine;;
``` 

#### Resultado:

```text
0 registro inválido
```

#### Conclusão: 

Durante a execução, o pipeline não identificou nenhum registro **invalido**.

#### Status: ✅ PASSOU

---

## 4. Validação SILVER

#### Validações:

| Validação                | Resultado |
| ------------------------ | :-------: |
| Quantidade de registros  | ✅       |

---

### 4.1 Quantidade de registros

#### Objetivo: 

Verificar se a quantidade de registros processados pela `SILVER` é a mesma quantidade processada pela `RAW`.

#### Consulta:

A SILVER faz a ingestão dos dados disponibilizado pela RAW em 3 tabelas: `silver.eventos`, `silver.produtos` e `silver.lojas`.

```sql
SELECT COUNT(*) FROM silver.eventos;

SELECT COUNT(*) FROM silver.produtos;

SELECT COUNT(*) FROM silver.lojas;
```

#### Resultados:

```text
silver.eventos  = 28.190
silver.produtos = 50
silver.lojas    = 1
------------------------
Total            28.241
```

#### Conclusão:

A quantidade total de registros disponibilizados pela camada Silver corresponde à quantidade de registros carregados na camada RAW.
  
```text
RAW    = 28.241
Silver = 28.241
```

#### Status: ✅ PASSOU

---

## 5. Validação GOLD

#### Validações:

| Validação                      | Resultado |
| ------------------------------ | :-------: |
| Quantidade de registros        | ✅       |
| Regra de filtragem dos eventos | ✅       |
| Cálculo de valor_total         | ✅       |
| Dimensão calêndario            | ✅       |

---

---

### 5.1 Quantidade de registros

#### Objetivo: 

Verificar se a quantidade de registros disponibilizados pela camada Gold é a mesma quantidade disponibilizada pela camada Silver.

#### Consulta:

```sql
SELECT COUNT(*) FROM gold.fato_vendas;

SELECT COUNT(*) FROM gold.dim_produtos;

SELECT COUNT(*) FROM gold.dim_lojas;
```

#### Resultado:

```text
gold.fato_vendas  = 18734
gold.dim_produtos = 50
gold.dim_lojas    = 1
--------------------------
Total               18.785
```

**Observação:** A quantidade de registros da `gold.fato_vendas` é inferior à quantidade de registros da `silver.eventos` porque a camada Gold considera apenas eventos cujo tipo_evento corresponde a `item adicionado`.

#### Consulta de confirmação:

```sql
SELECT COUNT(*) FROM silver.eventos WHERE tipo_evento = 'item adicionado';
```

#### Resultado:

```text
18.734 registros do tipo "item adicionado"
```

#### Conclusão: 

A camado Gold disponibiliza corretamente os registros relacionados ao tipo de eventos `"item adicionado"`.

#### Status: ✅ PASSOU

---

### 5.2 Validação do cálculo do valor total

#### Objetivo:

Verificar se existem registros na gold.fato_vendas cujo `valor_total` seja diferente do resultado da multiplicação entre `valor_unitario` e `quantidade`.

```sql
WITH
  amostra AS (
    SELECT 
      gfv.pedido_uid, 
      gfv.id_produto, 
      gdp.valor AS valor_unitario, 
      gfv.quantidade, 
      gfv.valor_total 
    FROM 
      gold.fato_vendas AS gfv 
      JOIN gold.dim_produtos AS gdp ON (gfv.id_produto = gdp.id_produto) 
  ) 
SELECT 
  COUNT(*) 
FROM 
  amostra 
WHERE 
  valor_unitario * quantidade <> valor_total;
```

#### Resultado:

```text
Inconsistências encontradas: 0
```

#### Conclusão: 

Nenhum valor inconsitente foi identificado.

#### Status: ✅ PASSOU

---

### 5.3 Tabela dimensão calendario

#### Objetivo: 

Verificar se a camada Gold esta armazenando as informações de data corretamente na dimensão calêndario.

#### Consulta:

```sql
SELECT COUNT(*) FROM gold.dim_calendario;
```

#### Resultado:

```text
10 datas distintas encontrados na dimensão calendário 
```

#### Consulta:

```sql
SELECT MIN(data), MAX(data), COUNT(*) FROM gold.dim_calendario;
```
#### Resultado:

```text
    min     |    max     | count 
------------+------------+-------
 2025-01-01 | 2025-01-10 |    10
```

#### Conclusão: 

A camada Gold extrai e armazena corretamente as datas referentes aos arquivos gerados pelo simulador.

#### Status: ✅ PASSOU

## 7. Resultado da execução

O pipeline apresentou a seguinte execução:

```text
+---------------- DATA PIPELINE ---------------+

---------------- Ciclo iniciado ----------------

— Localizando arquivos no diretório...
— Quantidade de arquivos localizados = 22
— Processando 22 arquivo(s)...

por favor aguarde...

--------------- Ciclo finalizado ---------------

-------------------- Resumo --------------------

• N° do ciclo                        = 1
• Duração (minutos) do ciclo         = 0m 14s 

• Quantidade de arquivos localizados = 22
• Quantidade de arquivos processados = 22
• Quantidade de arquivos rejeitados  = 0
• Tamanho total dos arquivos (MB)    = 7.64 MB

• Quantidade de registros válidos    = 28,241
• Quantidade de registros inválidos  = 0

+----------------------------------------------+
```

## 8. Evidências

As evidências `textuais` da execução estão registradas neste documento.

As evidências `visuais` complementares podem ser encontradas em:

`docs/testes/evidencias/teste_002/`

## 9. Conclusão

- O pipeline localizou e processou 22 arquivos (json e jsonl) gerados pelo PDV Simulator.
- Nenhum erro/exception foi disparado durante a execução.
- Cada arquivo foi validado, processado e movido para pasta de arquivos processados.

Resultados:

```text
- 22 arquivos localizados.

- Camada RAW    → 28.241 registros na sua forma bruta.
- Camada SILVER → 28.241 registros padronizados.
- Camada GOLD   → 8.785  registros prontos para analises de BI.

- 22 arquivos processados.
```

### Status final

Resultado final: **TESTE APROVADO**.
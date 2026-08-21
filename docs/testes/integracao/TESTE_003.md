# TESTE-003 - INTEGRAÇÃO 

**PDV_SIMULATOR → PIPELINE → BI**

Este teste tem como objetivo validar o funcionamento integrado do fluxo completo do projeto, desde a geração dos dados pelo `PDV Simulator` até sua disponibilização no relatório de BI.

O fluxo validado é:

```text
PDV Simulator
 ↓
Arquivos de vendas
 ↓
Pipeline
 ↓
RAW
 ↓
Silver
 ↓
Gold
 ↓
Relatório BI
```

---

## Status

✅ PASSOU

## Data do teste
20/08/2026

---

# 1. Configuração do teste

### PDV Simulator

* Quantidade de lojas: 1
* Quantidade de caixas por loja: 2
* Período simulado: `01/01/2025 → 05/01/2025`

### Pipeline

* Ambiente: Python
* Banco de dados: Postgres
* Execução: manual

### Relatório BI

* Ferramenta: Power BI
* Dataset utilizado: gold.fato_vendas, gold.dim_produto, gold.dim_lojas, gold.dim_calendario.
* Data/hora de atualização: 20/08/2026 - 20:40

---

# 2. Execução do PDV Simulator

### Comando

```bash
python3 -m pdv_simulator.simulador.pdv_main
```

### Resultado esperado

```text
O simulador deve gerar os arquivos correspondentes ao período, lojas e caixas configurados.
```

### Resultados obtidos

```text
5 dias simulados
12 arquivos gerados
```

**Status:** ✅ PASSOU

---

# 3. Execução do Pipeline

### Comando

```bash
python3 -m pipeline.orquestrador.pipeline_main
```

### Resultado esperado

```text
O pipeline deve processar os arquivos gerados pelo simulador e disponibilizar os dados nas camadas RAW, Silver e Gold.
```

### Resultados obtidos

```text
Arquivos localizados  = 12        
Arquivos processados  = 12        
Registros encontrados = 14,244    
Registros válidos     = 14,244    
Registros inválidos   = 0         
```

**Status:** ✅ PASSOU

---

# 4. Validação da camada RAW

## 4.1 Quantidade de registros

**Objetivo:** verificar se os dados gerados pelo simulador foram carregados corretamente na RAW.

### Resultado esperado

```text
A camada raw deve carregar todos os 14,244 registros na tabela raw.eventos.
```

### Consulta

```sql
SELECT COUNT(*) AS quantidade FROM raw.eventos;
```

### Resultado obtido

```text
Quantidade encontrada: 14,244
```

**Status:** ✅ PASSOU

---

## 4.2 Registros inválidos

### Resultado esperado

```text
Nenhum registro deve ser carregado na tabela de quarentena, pois apenas registros validos foram gerados pelo simulador.
```

### Consulta

```sql
SELECT COUNT(*) AS quantidade FROM raw.quarantine;
```

### Resultado obtido

```text
Quantidade de registros inválidos: 0
```

**Status:** ✅ PASSOU

---

# 5. Validação da camada Silver

**Objetivo:** verificar se os dados válidos da RAW foram disponibilizados corretamente nas tabelas da Silver.

### Resultado esperado

```text
A camada silver deve carregar os 14,244 registros disponibilizados pela camada raw nas tabelas do schema silver (silver.eventos, silver.produtos e silver.lojas).
```

### Consultas

```sql
SELECT COUNT(*) FROM silver.eventos;

SELECT COUNT(*) FROM silver.produtos;

SELECT COUNT(*) FROM silver.lojas;
```

### Resultados obtidos

| Tabela            | Quantidade |
| ------------------| :--------: |
| `silver.eventos`  | 14,193     |
| `silver.produtos` | 50         |
| `silver.lojas`    | 1          |
| **Total**         | **14,244** |

**Status:** ✅ PASSOU

---

# 6. Validação da camada Gold

### Resultado esperado

```text
A camada gold deve carregar os 9,456 registros disponibilizados pela camada silver nas tabelas do schema gold.
```
**Observação:** A quantidade de registros carregados pela camada gold (9,456) é inferior à quantidade de registros da disponibilizados pela camada silver (14,244). Isso acontece pelo fato da camada gold considerar apenas eventos cujo tipo_evento corresponde a `item adicionado`.

### Consultas

```sql
SELECT COUNT(*) FROM gold.fato_vendas;

SELECT COUNT(*) FROM gold.dim_produtos;

SELECT COUNT(*) FROM gold.dim_lojas;
```

### Resultados obtidos

| Tabela              | Quantidade |
| --------------------| :--------: |
| `gold.fato_vendas`  | 9,405      |
| `gold.dim_produtos` | 50         |
| `gold.dim_lojas`    | 1          |
| **Total**           | **9,456**  |

**Status:** ✅ PASSOU

# 7. Validação do Relatório BI

## 7.1 Atualização dos dados

**Objetivo:** verificar se o relatório de BI recebeu os dados disponibilizados pela camada Gold.

### Resultado esperado

```text
O relatório deve apresentar os dados referentes ao período processado pelo pipeline.
```

### Resultado obtido

```text
O relatório de BI contem informações de vendas referente ao periodo simulado.
```

**Status:** ✅ PASSOU

---

## 7.2 Validação dos indicadores

Selecionar alguns indicadores do relatório e compará-los diretamente com consultas realizadas na Gold.

### Resultado esperado

```text
Os valores apresentados pelo BI devem corresponder aos valores calculados a partir das tabelas da gold.
```

### Resultado obtido

| Indicador             | Gold     | BI        | Resultado |
| --------------------- | :------: | :-------: | :-------: |
| Total de vendas       | 220333,8 | 220333,8  | ✅       |
| Quantidade de itens   | 23,504   |  23,504   | ✅       |
| Quantidade de pedidos | 2,394    |  2,394    | ✅       |
| Ticket médio          | 92.04    |  92.04    | ✅       |


**Status:** ✅ PASSOU

---

# 8. Validação ponta a ponta

Nesta etapa é realizada uma validação do fluxo completo:

```text
PDV Simulator
 ↓
Arquivos
 ↓
RAW
 ↓
Silver
 ↓
Gold
 ↓
BI
```

### Validações

| Etapa         | Validação                           | Status |
| ------------- | ----------------------------------- | :----: |
| PDV Simulator | Arquivos gerados corretamente       | ✅    |
| RAW           | Dados carregados                    | ✅    |
| Silver        | Dados processados                   | ✅    |
| Silver        | Transformações corretas             | ✅    |
| Gold          | Dados disponibilizados              | ✅    |
| Gold          | Transformações corretas             | ✅    |
| BI            | Dados atualizados                   | ✅    |
| BI            | Indicadores consistentes com a Gold | ✅    |

---

# 9. Evidências

As evidências `textuais` da execução estão registradas neste documento.

As evidências `visuais` complementares podem ser encontradas em:

`docs/testes/evidencias/TESTE_003/`

---

# 10. Conclusão

O fluxo integrado foi executado desde a geração dos dados pelo `PDV Simulator` até sua disponibilização no relatório de BI.

### Resultado

```text
PDV Simulator → ✅ PASSOU
RAW           → ✅ PASSOU
Silver        → ✅ PASSOU
Gold          → ✅ PASSOU
BI            → ✅ PASSOU
```

### Status final

Resultado final: **TESTE APROVADO**.
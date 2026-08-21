# TESTE-004 - TESTE DE VOLUME

Este teste tem como objetivo avaliar o comportamento do `PDV Simulator` e do `pipeline` diante de diferentes volumes de dados, utilizando diferentes períodos de simulação.

Os cenários avaliados são:

* 1 dia;
* 1 semana;
* 1 mês;
* 1 ano.

---

## Status

✅ PASSOU

## Data do teste

21/08/2026

---

# 1. Objetivo

Avaliar:

* capacidade de processamento;
* quantidade de arquivos processados;
* quantidade de registros processados;
* tempo de execução;
* comportamento das camadas Raw, Silver e Gold;
* comportamento do sistema conforme o volume aumenta.

---

# 2. Configuração

| Configuração    | Valor      |
| --------------- | ---------- |
| Lojas           |          1 |
| Caixas por loja |          2 |
| Período inicial | 01/01/2025 |
| Período final   | 31/12/2025 |

A configuração de lojas e caixas deve permanecer a mesma entre os cenários para permitir uma comparação consistente.

---

# 3. Cenário 1 — 1 dia

## Entrada

```text
01/01/2025 → 01/01/2025
```

## Métricas

| Métrica             | Resultado |
| ------------------- | --------: |
| Dias simulados      |         1 |
| Arquivos gerados    |         4 |
| Tamanho total (MB)  |   0,68 MB |
| Registros validos   |     2.561 |
| Registros invalidos |         0 |
| Registros Raw       |     2.561 |
| Registros Silver    |     2.561 |
| Registros Gold      |     1.695 |
| Tempo do simulador  |   00m 00s |
| Tempo do pipeline   |   00m 02s |

## Validações

| Validação                  | Resultado                                            |
| -------------------------- | ---------------------------------------------------- |
| Divergências entre camadas | A quantidade de registros entre as camadas está de acordo com as regras de transformação do pipeline.                                             |
| Dimensão calendário        | Contém `1` data do período simulado, sem duplicidades. |

**Status:** ✅ PASSOU

---

# 4. Cenário 2 — 1 semana

## Entrada

```text
01/01/2025 → 07/01/2025
```

## Métricas

| Métrica             | Resultado |
| ------------------- | --------: |
| Dias simulados      |         7 |
| Arquivos gerados    |        16 |
| Tamanho total (MB)  |   5,35 MB |
| Registros validos   |    19.793 |
| Registros invalidos |         0 |
| Registros Raw       |    19.793 |
| Registros Silver    |    19.793 |
| Registros Gold      |    13.187 |  
| Tempo do simulador  |   00m 03s |
| Tempo do pipeline   |   00m 11s |

## Validações

| Validação                  | Resultado                                            |
| -------------------------- | ---------------------------------------------------- |
| Divergências entre camadas | A quantidade de registros entre as camadas está de acordo com as regras de transformação do pipeline.                                             |
| Dimensão calendário        | Contém todas as `7` datas do do período simulado, sem duplicidades. |

**Status:** ✅ PASSOU

---

# 5. Cenário 3 — 1 mês

## Entrada

```text
01/01/2025 → 31/01/2025
```

## Métricas

| Métrica             | Resultado |
| ------------------- | --------: |
| Dias simulados      |        31 |
| Arquivos gerados    |        64 |
| Tamanho total (MB)  |  24,34 MB |
| Registros gerados   |    89.915 |
| Registros invalidos |         0 |
| Registros Raw       |    89.915 |
| Registros Silver    |    89.915 |
| Registros Gold      |    59.935 | 
| Tempo do simulador  |   00m 11s |
| Tempo do pipeline   |   00m 54s |

## Validações

| Validação                  | Resultado                                            |
| -------------------------- | ---------------------------------------------------- |
| Divergências entre camadas | A quantidade de registros entre as camadas está de acordo com as regras de transformação do pipeline.                                             |
| Dimensão calendário        | Contém todas as `31` datas do do período simulado, sem duplicidades. |

**Status:** ✅ PASSOU

---

# 6. Cenário 4 — 1 ano

## Entrada

```text
01/01/2025 → 31/12/2025
```

## Métricas

| Métrica             | Resultado |
| ------------------- | --------: |
| Dias simulados      |       365 |
| Arquivos gerados    |       732 |
| Tamanho total (MB)  | 285.17 MB |
| Registros validos   | 1.053.166 |
| Registros invalidos |         0 |
| Registros Raw       | 1.053.166 |
| Registros Silver    | 1.053.166 |
| Registros Gold      |   702.192 |
| Tempo do simulador  |   02m 24s |
| Tempo do pipeline   |   13m 47s |


## Validações

| Validação                  | Resultado                                            |
| -------------------------- | ---------------------------------------------------- |
| Divergências entre camadas | A quantidade de registros entre as camadas está de acordo com as regras de transformação do pipeline.                                             |
| Dimensão calendário        | Contém todas as `365` datas do do período simulado, sem duplicidades. |

**Status:** ✅ PASSOU

---

# 7. Comparação dos cenários

| Métrica             | 1 dia   | 1 semana | 1 mês    | 1 ano     |
| ------------------- | -------:| --------:| --------:| ---------:|
| Arquivos gerados    |      4  |       16 |       64 |       732 |
| Registros validos   |   2.561 |   19.793 |   89.915 | 1.053.166 |
| Registros inválidos |       0 |        0 |        0 |         0 |
| Registros Raw       |   2.561 |   19.793 |   89.915 | 1.053.166 |
| Registros Silver    |   2.561 |   19.793 |   89.915 | 1.053.166 |
| Registros Gold      |   1.695 |   13.187 |   59.935 |   702.192 |
| Tempo simulador     | 00m 00s |  00m 03s |  00m 11s |   02m 24s |
| Tempo pipeline      | 00m 02s |  00m 11s |  00m 54s |   13m 47s |
| Tamanho total (MB)  | 0,68 MB |  5,35 MB | 24,34 MB | 285,17 MB |

---

# 8. Desempenho

Registrar o tempo de execução de cada cenário.

| Cenário  | simulador | pipeline | Tempo total |
| -------- | --------- | -------- | ----------- |
| 1 dia    | 00m 00s   | 00m 02s  | **00m 02s** |
| 1 semana | 00m 03s   | 00m 11s  | **00m 14s** |
| 1 mês    | 00m 11s   | 00m 54s  | **01m 05s** |
| 1 ano    | 02m 24s   | 13m 47s  | **16m 11s** |

> Os resultados devem ser utilizados apenas para comparação dentro do ambiente em que os testes foram executados.

---

# 9. Evidências

As evidências dos cenários podem ser armazenadas em:

```text
docs/testes/evidencias/teste_004/
```

---

# 10. Conclusão

Os testes de volume foram executados utilizando diferentes períodos de simulação.

### Resultado

| Cenário  | Status |
| -------- | :----: |
| 1 dia    | ✅    |
| 1 semana | ✅    |
| 1 mês    | ✅    |
| 1 ano    | ✅    | 

### Observações

*A registrar após a execução dos testes.*

### Status final

Resultado final: **TESTE APROVADO**.
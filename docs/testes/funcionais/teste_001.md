# TESTE_001 - PDV_SIMULATOR

Este teste tem como objetivo validar o funcionamento do PDV Simulator, verificando a geração dos arquivos de eventos de vendas e dos arquivos de referência, bem como sua organização e estrutura.

## Status

✅ PASSOU

## Data do teste
14/08/2026

## 1. Configuração do simulador

- Quantidade de **lojas**: 1
- Quantidade de **caixas por loja**: 2

## 2. Entrada

Período simulado:

`01/01/2025` → `10/01/2025`

Total de dias simulados: **10 dias**

## 3. Execução

**Comando**
```text
python3 -m pdv_simulator.simulador.pdv_main
```

## 4. Critérios de validação

O teste considera o funcionamento do simulador aprovado quando:

- O período informado é processado corretamente.
- A quantidade de dias simulados corresponde ao período informado.
- Os arquivos de eventos são gerados para os caixas configurados.
- Os arquivos de referência são gerados corretamente.
- Os arquivos são armazenados nos diretórios esperados.
- Os arquivos possuem os formatos esperados.
- Os eventos possuem os campos definidos pelo modelo de dados.
- Os arquivos de referência possuem a estrutura esperada.

## 5. Métricas

| Métrica                | Esperado  | Obtido   | Status | 
|------------------------|:---------:|:--------:|:------:| 
| Dias simulados         | 10        | 10       | ✅    | 
| Arquivos de eventos    | 20        | 20       | ✅    | 
| Arquivos de referência | 2         | 2        | ✅    | 

### Cálculo esperado

A quantidade de arquivos de eventos é determinada pela quantidade de `dias`, `lojas` e `caixas` configurados:

**10** dias × **1** loja × **2** caixas = **20** arquivos de eventos

Além dos arquivos de eventos, são gerados:

- **1** catálogo de produtos
- **1** arquivo de informações das lojas

Portanto:

```text
20 arquivos de eventos
+ 1 catálogo de produtos
+ 1 arquivo de lojas

= 22 arquivos
```

## 6. Saida esperada

| Tipo                 | Formato | Quantidade |
|----------------------|:-------:|:----------:|
| Eventos de vendas    | JSONL   | 20         | 
| Catalogo de produtos | JSON    | 1          | 
| Arquivo de lojas     | JSON    | 1          | 
| **Total**            |         | **22**     |

---
## 7. Resultado da execução

O simulador apresentou a seguinte execução:

```text
+----------------- PDV SIMULATOR ------------------+

Digite o intervalo que deseja simular:

digite a data inicial (ex: 2026-01-01): 2025-01-01
digite a data final   (ex: 2026-01-02): 2025-01-10

---------------- Simulador iniciado ----------------

— Simulando 10 dia(s) de vendas...

por favor aguarde...

--------------- Simulador finalizado ---------------

---------------------- Resumo ----------------------

• Duração (minutos) do simulador  = 0m 4s

• Total de dias simulados         = 10
• Total de arquivos gerados       = 22

+--------------------------------------------------+
```

### Resultado

O simulador processou corretamente os 10 dias informados e gerou os 22 arquivos esperados, sendo:

- 20 arquivos de eventos de vendas;
- 1 arquivo de catálogo;
- 1 arquivo contendo as informações das lojas.

## 8. Validação dos arquivos gerados

### 8.1 Eventos de vendas

A amostra abaixo contempla dois eventos pertencentes a um pedido realizado no `caixa 1` da `loja 1` no dia `01/01/2025`.

| Informação      | Valor                                                         |
|-----------------|---------------------------------------------------------------|
| Nome do arquivo | 2025-01-01_eventos_l1_c1.jsonl                                | 
| Local de origem | /data_pipeline/pdv_sales/pdv_new_files/lojas/loja_1/2025/1/1/ |
| Formato         | JSONL                                                         |

#### Amostra:

```json
{
    "event_id": "c7f61b1c-06bf-42e4-9358-a2d7e5377fc6",
    "event_time": "2025-01-01T08:04:25",
    "emit_time": "2025-01-01T08:04:26",
    "tipo_evento": "pedido criado",
    "evento_seq": 1,
    "id_loja": 1,
    "id_caixa": 1,
    "id_pedido": 1,
    "produto_id": null,
    "quantidade": null,
    "valor_unitario": null
}
{
    "event_id": "6347392a-d1f8-4d0b-81f9-d04c0f5bc522",
    "event_time": "2025-01-01T08:04:25",
    "emit_time": "2025-01-01T08:04:26",
    "tipo_evento": "item adicionado",
    "evento_seq": 2,
    "id_loja": 1,
    "id_caixa": 1,
    "id_pedido": 1,
    "produto_id": 26,
    "quantidade": 3,
    "valor_unitario": 2.5
}
...
```
#### Validações

| Validação                        | Resultado |
|----------------------------------|:---------:|
| Arquivo possui formato JSONL     | ✅       |
| event_id presente                | ✅       |
| event_time presente              | ✅       |
| emit_time presente               | ✅       |
| Identificação da loja presente   | ✅       |
| Identificação do caixa presente  | ✅       |
| Identificação do pedido presente | ✅       |
| Sequência do evento presente     | ✅       |
| Tipo_evento presente             | ✅       |

### 8.2 Informações da Loja

Essa amostra contempla informações da unica loja sendo simulada

| Informação      | Valor                                                      |
|-----------------|------------------------------------------------------------|
| Nome do arquivo | 2025-01-01_lojas.json                                      | 
| Local de origem | /data_pipeline/pdv_sales/pdv_new_files/arquivos_referencia |
| Formato         | JSON                                                       |

#### Amostra:

```json
[
    {
        "ID": "1",
        "CNPJ": "12.345.678/0001-01",
        "Endereço": "Av. Paulista 1500",
        "Bairro": "Bela Vista",
        "Cidade": "São Paulo",
        "Estado": "SP",
        "Gerente": "Carlos Silva",
        "Horário_de_Atendimento": "08:00 - 22:00"
    }
]
```
#### Validação

O arquivo foi gerado no formato esperado e contém as informações referentes à loja configurada no teste.

Resultado: ✅ PASSOU

### 8.3 Catálogo de produtos

A amostra contempla informações de 2 produtos pertencentes ao catálogo de produtos.

| Informação      | Valor                                                      |
|-----------------|------------------------------------------------------------|
| Nome do arquivo | 2025-01-01_catalogo.json                                   | 
| Local de origem | /data_pipeline/pdv_sales/pdv_new_files/arquivos_referencia |
| Formato         | JSON                                                       |


#### Amostra:

```json
[
    {
        "id": "1",
        "nome": "Arroz 5kg",
        "valor": "24.9"
    },
    {
        "id": "2",
        "nome": "Feijão 1kg",
        "valor": "7.5"
    },
    ...
]
```

#### Validação

O arquivo foi gerado no formato esperado e apresenta a estrutura definida para o catálogo de produtos.

Resultado: ✅ PASSOU

## 9. Evidências

As evidências `textuais` da execução estão registradas neste documento.

As evidências `visuais` complementares podem ser encontradas em:

`docs/testes/evidencias/TESTE_001/`

## 10. Conclusão

O PDV Simulator foi executado utilizando uma loja, dois caixas e um período de 10 dias.

O resultado obtido foi compatível com o esperado:

```text
10 dias simulados

20 arquivos de eventos
1 arquivo de catálogo
1 arquivo de lojas
----------------------
= 22 arquivos gerados
```
Os arquivos analisados apresentaram os formatos e estruturas esperados.

Resultado final: **TESTE APROVADO**.
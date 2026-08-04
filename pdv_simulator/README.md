# PDV_SIMULATOR

O `pdv_simulator` é responsável por gerar dados simulados de vendas, lojas e produtos para alimentar o pipeline de dados.

## Fluxo do PDV_SIMULATOR

### 1. Entrada

O simulador recebe, via `input`, um intervalo de datas correspondente ao período que será simulado.

O intervalo informado é armazenado nas configurações do pdv_simulator e utilizado durante a execução da simulação.

### 2. Configurações

Durante a inicialização, o simulador obtém das configurações:

* Data inicial da simulação
* Data final da simulação
* Quantidade de lojas
* Quantidade de caixas por loja

Essas configurações determinam o volume e o período dos dados gerados.

### 3. Simulação

Para cada combinação de `data`, `loja` e `caixa` definida nas configurações, o simulador executa as etapas necessárias para geração dos dados.

#### 3.1 Catálogo de produtos

O catálogo base de produtos é carregado a partir do arquivo:

`base/catalogo.csv`

O catálogo é utilizado como referência para os produtos presentes nos eventos de venda.

#### 3.2 Simulação de vendas

Para cada caixa e data da simulação:

1. São gerados pedidos de venda.
2. Cada pedido recebe seus respectivos produtos e quantidades.
3. Os eventos relacionados às vendas são gerados.
4. Os eventos são armazenados no formato JSONL.

#### 3.3 Dados de lojas

As informações referentes às lojas utilizadas na simulação são armazenadas em formato JSON.

#### 3.4 Dados de produtos

O catálogo de produtos utilizado pelo simulador é convertido e armazenado em formato JSON.

### 4. Geração dos arquivos

Ao final da execução, o simulador gera arquivos contendo:

| Arquivo          | Formato | Conteúdo                            |
| ---------------- | ------- | ----------------------------------- |
| Eventos de venda | JSONL   | Eventos gerados durante a simulação |
| Catálogo         | JSON    | Produtos disponíveis                |
| Lojas            | JSON    | Informações das lojas               |

### 5. Armazenamento

Os arquivos gerados são armazenados no diretório local definido pelo **pdv_simulator**.

Esses arquivos posteriormente podem ser utilizados como entrada para o pipeline de dados.

## Eventos gerados

O simulador gera eventos relacionados às operações de venda realizadas nos caixas.

Cada evento possui informações como:

- ID do evento
- Data/hora do evento
- Data/hora da emissão do evento
- Tipo do evento
- Sequencia do evento
- Loja
- Caixa
- Pedido
- Produto
- Quantidade
- Valor

## Premissas

Atualmente, o simulador considera:

- Todas as lojas possuem a mesma quantidade de caixas.
- O catálogo de produtos é obtido de um arquivo CSV base.
- Os eventos são gerados de forma determinística/aleatória.
- Os dados gerados representam operações válidas de venda.

## Arquitetura

```bash
pdv_simulator/

    ├── config/
    ├── data/
    ├── simulador/
    ├── src/
    └── README.md
```

## Como executar

No terminal (Linux):
```bash
python3 -m pdv_simulator.simulador.pdv_main
```

Digite a `data inicial`e `data final` no input respeitando o formato YYYY-MM-DD.
```bash
# 1° input -> digite a data inicial (ex: 2026-01-01):
 2020-01-01

# 2° input -> digite a data final (ex: 2026-01-01): 
 2020-01-02
```

Os arquivos serão salvos em:

`pdv_sales/new_files/eventos/`

## Próximas evoluções

Para versões futuras, o simulador poderá incorporar comportamentos
mais próximos de um ambiente real, como:

- Duplicidade de eventos
- Eventos atrasados
- Eventos fora de ordem
- Cancelamentos
- Falhas na geração de eventos
- Maior quantidade de lojas e caixas
- Variação no volume de vendas
- Diferentes comportamentos por loja
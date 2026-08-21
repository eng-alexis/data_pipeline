# Testes

Este diretório apresenta os testes realizados no projeto, contemplando o `PDV Simulator`, o `pipeline de dados` e o `fluxo completo` de processamento das informações.

## Testes realizados

| ID        | Teste              | Tipo           | Status |
|-----------|--------------------|----------------|:------:|
| teste_001 | PDV Simulator      | Funcionalidade | ✅    |
| teste_002 | Pipeline           | Funcionalidade | ✅    |
| teste_003 | Fluxo do projeto   | Integração     | ✅    |
| teste_004 | Simulando 1 dia    | volume         | 🔲    |
| teste_005 | Simulando 1 semana | volume         | 🔲    |
| teste_006 | Simulando 1 mês    | volume         | 🔲    |
| teste_007 | Simulando 1 ano    | volume         | 🔲    |

---

## 1. Objetivos

Os testes possuem os seguintes objetivos:

- Validar o funcionamento do `PDV Simulator`.
- Validar o processamento das camadas `RAW`, `Silver` e `Gold`.
- Validar a integração entre o `simulador` e o `pipeline`.
- Verificar a integridade dos dados durante o `processamento`.
- Verificar o comportamento do `pipeline` em diferentes `volumes` de dados.
- Validar o tratamento de `registros` e `arquivos inválidos`.
- Validar o tratamento de `arquivos duplicados`.
- Registrar `evidências` dos testes realizados.

## 2. Tipos de teste

### 2.1 Testes funcionais

Verificam se cada componente executa corretamente sua responsabilidade.

Exemplos:

- Geração dos arquivos pelo `simulador`;
- Validação dos arquivos;
- Carregamento na camada `RAW`;
- Transformação para `Silver`;
- Disponibilização na `Gold`;
- Movimentação dos arquivos processados;
- Registro das execuções na `auditoria`.

### 2.2 Testes de integração

Verificam o funcionamento do fluxo completo:

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
```

### 2.3 Testes de volume

Verificam o comportamento do sistema diante de diferentes períodos de simulação:

- 1 dia;
- 1 semana;
- 1 mês;
- 1 ano.

### 2.4 Testes de exceção

Verificam o comportamento do sistema diante de situações inesperadas:

- Arquivo inválido;
- Arquivo duplicado;
- Arquivo vazio;
- Campos obrigatórios ausentes;
- Falha de conexão com o banco de dados;
- Registro inválido;
- Tipos de dados inválidos.

## Links para testes realizados

### Testes Funcionais

- [PDV Simulator](funcionais/teste_001.md) - Documentação do teste realizado no PDV Simulator.
- [Pipeline](funcionais/teste_002.md) - Documentação do teste realizado no Pipeline.

### Teste de integração

- [Integração](integracao/teste_003.md) - Documentação do teste de integração dos compotentes do projeto.

## Status da realização dos testes

- Em desenvolvimento
# 🚀 Tableau API - Sistema de Exportação e Processamento de Dados

Sistema automatizado em Python para exportar dados do Tableau Cloud e transformá-los em planilhas Excel processadas. O projeto utiliza **Personal Access Tokens (PATs)** para contornar a autenticação multifator (MFA) e oferece barras de progresso visuais para melhor feedback durante a execução.

## 📋 Sobre o Projeto

Este sistema foi desenvolvido com arquitetura orientada a objetos para:
- **Exportar dados** de visualizações específicas do Tableau Cloud como CSV
- **Transformar automaticamente** os dados CSV em planilhas Excel (XLSX)
- **Reorganizar e processar** dados usando pivot tables e formatação customizada
- **Fornecer feedback visual** com barras de progresso usando tqdm
- **Registrar logs detalhados** de todas as operações

### 🎯 Funcionalidades Principais

- ✅ **Autenticação segura** via Personal Access Token
- ✅ **Exportação automatizada** de dados do Tableau Cloud
- ✅ **Transformação de dados** CSV para XLSX com processamento avançado
- ✅ **Barras de progresso visuais** para acompanhar o processo
- ✅ **Sistema de logging** completo com arquivos de log
- ✅ **Arquitetura modular** orientada a objetos
- ✅ **Tratamento robusto de erros** com mensagens detalhadas

## 🏗️ Arquitetura do Projeto

```
backend/
├── src/
│   ├── __init__.py           # Módulo Python
│   ├── config.py            # Configurações e variáveis de ambiente
│   ├── auth.py              # Autenticação no Tableau Cloud
│   ├── tableau_export.py    # Exportação de dados do Tableau
│   ├── data_processing.py   # Processamento e transformação de dados
│   ├── progress.py          # Sistema de barras de progresso
│   ├── utils.py             # Utilitários (logging, validações)
│   └── main.py              # Aplicação principal
├── output/                  # Arquivos gerados (CSV e XLSX)
├── logs/                    # Arquivos de log da aplicação
├── requirements.txt         # Dependências Python
├── exemplo_progresso.py     # Demonstração do sistema de progresso
└── README.markdown          # Esta documentação
```

### 🛠️ Classes Principais

| Classe | Responsabilidade |
|--------|------------------|
| `TableauAPIApp` | Orquestração geral da aplicação |
| `Config` | Gerenciamento de configurações |
| `TableauAuthenticator` | Autenticação no Tableau Cloud |
| `TableauExporter` | Exportação de dados do Tableau |
| `DataProcessor` | Processamento e transformação de dados |
| `Logger` | Sistema de logging |
| `TaskProgress` | Barras de progresso com contexto |

## 🚀 Configuração e Instalação

### 1. Pré-requisitos

- **Python 3.8+** instalado
- **Conta no Tableau Cloud** com permissões adequadas
- **Personal Access Token (PAT)** configurado no Tableau Cloud

### 2. Instalação das Dependências

```bash
# Navegue até o diretório do projeto
cd backend

# Instale as dependências
pip install -r requirements.txt
```

### 3. Configuração das Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto `backend/` com as seguintes variáveis:

```env
# Configurações do Tableau Cloud
TABLEAU_SERVER=https://us-east-1.online.tableau.com
TABLEAU_SITE_ID=seu-site-id
TABLEAU_TOKEN_NAME=nome-do-seu-token
TABLEAU_TOKEN_VALUE=valor-do-seu-token

# Configurações de saída
OUTPUT_DIR=output
WORKBOOK_ID=id-da-pasta-de-trabalho
VIEW_ID=id-da-visualizacao

# Nomes dos arquivos (opcional)
NAME_FILE_ORIGINAL=BASE_DE_DADOS.csv
NAME_FILE_PROCESSED=ANALISE_DE_PEDIDOS.xlsx
```

### 4. Como Obter os IDs Necessários

#### Personal Access Token (PAT):
1. Acesse o Tableau Cloud
2. Vá em **My Account Settings**
3. Na aba **Personal Access Tokens**, clique em **Create new token**
4. Copie o nome e valor do token para o `.env`

#### Workbook ID e View ID:
1. Acesse a visualização desejada no Tableau Cloud
2. Na URL, você verá algo como: `#/site/seusite/workbooks/123456/views/789012`
3. `123456` é o `WORKBOOK_ID`
4. `789012` é o `VIEW_ID`

## 🎮 Como Usar

### Execução Básica

```bash
# Execute a aplicação principal
python -m src.main
```

### Exemplo de Saída

```
🚀 Iniciando processamento dos dados do Tableau...
============================================================

📁 Arquivos de saída:
   CSV: output\BASE_DE_DADOS.csv
   XLSX: output\ANALISE_DE_PEDIDOS.xlsx

Inicializando aplicação: 100%|████████| 100/100 [00:02<00:00, 45.2%/s]
Autenticando no Tableau: 100%|████████| 100/100 [00:01<00:00, 85.1%/s]
Exportando dados do Tableau: 100%|████████| 100/100 [00:05<00:00, 18.3%/s]
Processando dados CSV para XLSX: 100%|████████| 100/100 [00:01<00:00, 92.4%/s]
Progresso geral: 100%|████████| 2/2 [00:09<00:00, 4.8s/etapa]

✅ Processamento concluído com sucesso!
============================================================

📊 Informações dos arquivos gerados:
   📄 CSV: 15,234 bytes
   📈 XLSX: 28,456 bytes
```

### Demonstração do Sistema de Progresso

```bash
# Execute os exemplos de barra de progresso
python exemplo_progresso.py
```

## 📊 Processamento de Dados

### Estrutura Esperada do CSV

O sistema espera um CSV com as seguintes colunas:
- `Cidades`
- `Combustíveis` 
- `Measure Names`
- `Origens`
- `Medição`
- `Turno + Data`
- `Measure Values`

### Transformações Realizadas

1. **Pivot Table**: Converte `Measure Names` em colunas individuais
2. **Reorganização**: Ordena colunas conforme especificação do negócio
3. **Limpeza de Dados**: Remove vírgulas e converte para valores numéricos
4. **Formatação**: Salva como XLSX com formatação adequada

### Colunas de Saída (Measure Names)

O sistema reorganiza as seguintes medidas:
- Estoque Dia Anterior Última Medição
- Estoque Última Medição
- Venda Última Medição
- Compra Dia Última Medição
- Verificação, Capacidade, Vendas
- Giro de Estoque e Percentual de Capacidade
- Sugestões e Médias

## 📋 Logs e Monitoramento

### Sistema de Logging

- **Console**: Mensagens informativas e de erro
- **Arquivo**: Logs detalhados em `logs/tableau_api_YYYYMMDD.log`
- **Níveis**: INFO, WARNING, ERROR, DEBUG

### Exemplo de Log

```log
2025-07-25 14:22:12,628 - TableauAPIApp - INFO - Iniciando aplicação...
2025-07-25 14:22:12,630 - TableauAPIApp - INFO - Configurações validadas com sucesso
2025-07-25 14:22:13,587 - TableauAPIApp - INFO - Autenticação no Tableau realizada com sucesso
2025-07-25 14:22:14,100 - TableauAPIApp - INFO - Executando: Exportando dados do Tableau
2025-07-25 14:22:19,660 - TableauAPIApp - INFO - Executando: Transformando dados
2025-07-25 14:22:20,798 - TableauAPIApp - INFO - Processamento concluído com sucesso!
```

## 🔧 Solução de Problemas

### Erros Comuns

| Erro | Solução |
|------|---------|
| `Erro na autenticação` | Verifique PAT e configurações no `.env` |
| `Pasta de trabalho não encontrada` | Confirme o `WORKBOOK_ID` na URL do Tableau |
| `View não encontrada` | Confirme o `VIEW_ID` na URL do Tableau |
| `Colunas esperadas não encontradas` | Verifique se a view contém as colunas necessárias |
| `Importação pandas/tqdm não encontrada` | Execute `pip install -r requirements.txt` |

### Debug Avançado

```bash
# Execute com logs detalhados
python -c "
from src.main import TableauAPIApp
import logging
logging.basicConfig(level=logging.DEBUG)
app = TableauAPIApp()
app.run()
"
```

## 📦 Dependências

```txt
tableauserverclient==0.38
python-dotenv==1.1.1
pandas==2.3.1
openpyxl==3.1.5
tqdm==4.66.2
```

## 🔒 Segurança

- ⚠️ **Nunca commite o arquivo `.env`** 
- 🔐 **Mantenha o PAT seguro** e renove periodicamente
- 📝 **Monitore logs** para atividades suspeitas
- 🚫 **Revogue tokens** não utilizados no Tableau Cloud

## 🚧 Próximos Passos

- [ ] Interface web com Flask/FastAPI
- [ ] Agendamento automático de execuções
- [ ] Suporte a múltiplas visualizações
- [ ] Notificações por email
- [ ] Dashboard de monitoramento
- [ ] Integração com bancos de dados

## 📞 Suporte

Para problemas ou dúvidas:
1. Verifique os logs em `logs/tableau_api_YYYYMMDD.log`
2. Execute `python exemplo_progresso.py` para testar o sistema
3. Consulte a documentação oficial do [Tableau Server Client](https://tableau.github.io/server-client-python/)

---

**Desenvolvido com ❤️ usando Python, Tableau REST API e tqdm**
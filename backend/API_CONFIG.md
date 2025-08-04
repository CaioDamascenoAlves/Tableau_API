# 🔧 Configuração da API de Combustível

## 📋 Configurações Necessárias

Para habilitar o upload automático para a API de Combustível, configure as seguintes variáveis no seu arquivo `.env`:

```env
# Configurações da API de Combustível
COMBUSTIVEL_API_URL=https://combustivel-backend-production.up.railway.app
COMBUSTIVEL_API_TOKEN=seu-token-da-api-combustivel
ENABLE_API_UPLOAD=true
```

## 🔑 Como Obter seu Token

1. **Entre em contato** com o administrador da API de Combustível
2. **Solicite um token** de acesso para sua aplicação
3. **Substitua** `seu-token-da-api-combustivel` pelo token fornecido
4. **Mantenha o token seguro** e não o compartilhe

## ⚙️ Configurações Opcionais

### Desabilitar Upload Automático

Para processar apenas os dados sem enviar para a API:

```env
ENABLE_API_UPLOAD=false
```

### URL Personalizada

Se você está usando uma instância diferente da API:

```env
COMBUSTIVEL_API_URL=https://sua-instancia-api.com
```

## 🧪 Testando a Configuração

### Teste Básico

```bash
# Teste apenas a conexão com a API
python test_api.py
```

### Teste Detalhado

```bash
# Execute com logs detalhados
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from src.config import Config
from src.api_integration import CombustivelAPIUploader

config = Config()
uploader = CombustivelAPIUploader(config.COMBUSTIVEL_API_URL, config.COMBUSTIVEL_API_TOKEN)
print('Teste de conexão:', uploader.test_api_connection())
"
```

## 🔍 Troubleshooting

### Erro: "URL da API de Combustível é obrigatória"

**Solução**: Verifique se `COMBUSTIVEL_API_URL` está definida no `.env`

### Erro: "Token de autenticação é obrigatório"

**Solução**: Verifique se `COMBUSTIVEL_API_TOKEN` está definida no `.env`

### Erro: "Erro de autenticação" (HTTP 401)

**Soluções**:
1. Verifique se o token está correto
2. Confirme se o token não expirou
3. Entre em contato com o administrador da API

### Erro: "Arquivo muito grande" (HTTP 413)

**Soluções**:
1. Verifique o tamanho do arquivo XLSX gerado
2. O limite atual é de 50MB
3. Se necessário, otimize o processamento de dados

### Erro: "Timeout na requisição"

**Soluções**:
1. Verifique sua conexão com a internet
2. A API pode estar temporariamente indisponível
3. Tente novamente em alguns minutos

## 📊 Status Codes da API

### Upload de Arquivo

- **201 Created**: Upload realizado com sucesso (padrão da API)
- **200 OK**: Upload realizado com sucesso (compatibilidade)
- **401 Unauthorized**: Token inválido ou expirado
- **413 Payload Too Large**: Arquivo muito grande (>50MB)
- **422 Unprocessable Entity**: Erro de validação dos dados
- **500+ Server Error**: Erro interno do servidor

### Teste de Conexão

- **200 OK**: API funcionando normalmente
- **201 Created**: Resposta válida da API
- **404 Not Found**: API existe mas rota raiz não implementada (normal)
- **401 Unauthorized**: API funcionando, token pode estar incorreto
- **500+ Server Error**: API com problemas

## 📊 Logs da API

### Localização

Os logs da integração com a API são salvos em:
- **Console**: Mensagens de status em tempo real
- **Arquivo**: `logs/tableau_api_YYYYMMDD.log`

### Níveis de Log

- `INFO`: Operações normais (início/fim de upload)
- `WARNING`: Situações que merecem atenção
- `ERROR`: Erros que impedem o funcionamento
- `DEBUG`: Informações detalhadas para troubleshooting

### Exemplo de Logs

```log
2025-08-04 10:30:15,123 - CombustivelAPIClient - INFO - Iniciando upload do arquivo: output/ANALISE_DE_PEDIDOS.xlsx (28,456 bytes)
2025-08-04 10:30:18,456 - CombustivelAPIClient - INFO - Status da resposta: 201
2025-08-04 10:30:18,457 - CombustivelAPIClient - INFO - Upload realizado com sucesso: output/ANALISE_DE_PEDIDOS.xlsx
```

## 🔒 Segurança da API

### Boas Práticas

- ✅ **Mantenha o token seguro** - não compartilhe ou publique
- ✅ **Use HTTPS** - sempre use conexões seguras
- ✅ **Monitore logs** - verifique atividades suspeitas
- ✅ **Renove tokens** - periodicamente solicite novos tokens
- ✅ **Limite permissões** - use tokens com menor privilégio necessário

### O que NÃO fazer

- ❌ **Não hard-code tokens** no código fonte
- ❌ **Não commite o arquivo `.env`** 
- ❌ **Não compartilhe tokens** por email ou chat
- ❌ **Não use tokens em URLs** ou logs
- ❌ **Não ignore erros** de autenticação

## 🚀 Integração no Fluxo

### Automática

Quando `ENABLE_API_UPLOAD=true`, o upload acontece automaticamente após o processamento dos dados:

1. **Exportação** do Tableau → CSV
2. **Processamento** CSV → XLSX
3. **Upload automático** XLSX → API ✨

### Manual

Para controle manual, desabilite o upload automático e use:

```python
from src.config import Config
from src.api_integration import CombustivelAPIUploader

config = Config()
uploader = CombustivelAPIUploader(config.COMBUSTIVEL_API_URL, config.COMBUSTIVEL_API_TOKEN)

# Upload manual
result = uploader.upload_file("output/ANALISE_DE_PEDIDOS.xlsx")
print(result)
```

## 📞 Suporte

Para problemas específicos da API de Combustível:

1. **Verifique os logs** primeiro
2. **Execute o teste** `python test_api.py`
3. **Consulte esta documentação** para soluções comuns
4. **Entre em contato** com o suporte da API se necessário

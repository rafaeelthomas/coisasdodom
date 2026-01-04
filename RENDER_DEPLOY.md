# 🚀 Deploy no Render.com - Catálogo de Enxoval

## 📋 Pré-requisitos

- Conta no [Render.com](https://render.com)
- Repositório Git (GitHub, GitLab ou Bitbucket)
- Python 3.x instalado no servidor
- Node.js 18+ instalado no servidor

---

## 🔧 Configuração do Projeto

### 1. Adicionar Dependências Python

Crie um arquivo `requirements.txt` na raiz do projeto:

```txt
# Nenhuma dependência Python necessária
# O script usa apenas bibliotecas padrão
```

### 2. Verificar package.json

Certifique-se de que o `package.json` está correto:

```json
{
  "name": "catalogo-enxoval",
  "version": "1.0.0",
  "main": "server.js",
  "scripts": {
    "start": "node server.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "multer": "^1.4.5-lts.1",
    "cors": "^2.8.5",
    "sharp": "^0.33.5"
  }
}
```

### 3. Criar .gitignore

```
node_modules/
.DS_Store
*.log
.env
```

---

## 🌐 Deploy no Render.com

### Passo 1: Criar Web Service

1. Acesse [Render Dashboard](https://dashboard.render.com)
2. Clique em **"New +"** → **"Web Service"**
3. Conecte seu repositório Git
4. Configure o serviço:

**Configurações Básicas:**
- **Name**: `catalogo-enxoval-dominic`
- **Region**: `Oregon (US West)` (ou mais próximo)
- **Branch**: `main` (ou sua branch principal)
- **Root Directory**: deixe vazio
- **Runtime**: `Node`
- **Build Command**: `npm install && python3 -m pip install --upgrade pip`
- **Start Command**: `node server.js`

**Plan:**
- Selecione **Free** para testes ou **Starter** para produção

### Passo 2: Variáveis de Ambiente

Adicione as seguintes variáveis de ambiente (Environment Variables):

```bash
NODE_ENV=production
PORT=10000
```

### Passo 3: Deploy

1. Clique em **"Create Web Service"**
2. Aguarde o build e deploy (5-10 minutos)
3. Seu catálogo estará disponível em: `https://catalogo-enxoval-dominic.onrender.com`

---

## 🔒 Persistência de Dados

⚠️ **IMPORTANTE**: O Render.com **NÃO persiste arquivos** no sistema de arquivos entre deploysdeploys.

### Soluções para Armazenamento:

#### Opção 1: Cloudinary (Recomendado)
- Upload de imagens para CDN
- Thumbnails automáticos
- Free tier: 25 GB armazenamento + 25 GB bandwidth

#### Opção 2: AWS S3
- Armazenamento de objetos
- Integração simples
- Free tier: 5 GB por 12 meses

#### Opção 3: Render Disks (Pago)
- Armazenamento persistente no próprio Render
- A partir de $7/mês por 10 GB

---

## 🔄 Integrar Cloudinary (Recomendado)

### 1. Criar Conta Cloudinary

1. Acesse [Cloudinary.com](https://cloudinary.com)
2. Crie conta gratuita
3. Copie suas credenciais:
   - Cloud Name
   - API Key
   - API Secret

### 2. Instalar Cloudinary SDK

```bash
npm install cloudinary
```

### 3. Atualizar server.js

Adicione no início do arquivo:

```javascript
const cloudinary = require('cloudinary').v2;

// Configurar Cloudinary
cloudinary.config({
    cloud_name: process.env.CLOUDINARY_CLOUD_NAME,
    api_key: process.env.CLOUDINARY_API_KEY,
    api_secret: process.env.CLOUDINARY_API_SECRET
});
```

### 4. Adicionar Variáveis de Ambiente no Render

```bash
CLOUDINARY_CLOUD_NAME=seu_cloud_name
CLOUDINARY_API_KEY=sua_api_key
CLOUDINARY_API_SECRET=seu_api_secret
```

---

## 📝 Funcionalidades Implementadas

### ✅ Upload de Produtos
- Upload de imagens (JPG, PNG, GIF, WEBP)
- Geração automática de thumbnails (400x400px)
- Validação de tamanho (máx 5MB)
- Regeneração automática do HTML

### ✅ Deletar Produtos
- Botão de exclusão em cada produto
- Modal de confirmação
- Deleta imagem original e thumbnail
- Regenera HTML automaticamente

### ✅ Criação de Categorias
- Criar novas categorias
- Criar subcategorias
- Estrutura de pastas automática

### ✅ Design Responsivo
- Menu hamburguer mobile
- Grid adaptável (2-5 colunas)
- Touch-friendly
- Suporte a landscape

---

## 🐛 Troubleshooting

### Erro: "Module not found: sharp"

**Solução**:
```bash
# No Render, adicione ao Build Command:
npm install && npm rebuild sharp
```

### Erro: "Python not found"

**Solução**:
```bash
# Verifique se Python 3 está disponível no Render
python3 --version
```

### Erro: "Port already in use"

**Solução**: O Render define automaticamente a variável PORT. Use:
```javascript
const PORT = process.env.PORT || 3000;
```

### Imagens não aparecem após upload

**Causa**: Render não persiste arquivos.

**Solução**: Implemente Cloudinary ou AWS S3 (ver seções acima).

---

## 📊 Monitoramento

### Logs no Render

1. Acesse seu serviço no Dashboard
2. Clique na aba **"Logs"**
3. Monitore em tempo real:
   - ✅ Uploads bem-sucedidos
   - ❌ Erros de upload
   - 🔄 Regenerações de HTML

### Health Checks

O Render verifica automaticamente se o servidor está online:
- URL de Health Check: `/`
- Intervalo: 60 segundos
- Timeout: 30 segundos

---

## 🔐 Segurança

### Recomendações:

1. **Autenticação**: Adicione autenticação para proteção
```bash
npm install express-basic-auth
```

2. **Rate Limiting**: Previna spam de uploads
```bash
npm install express-rate-limit
```

3. **HTTPS**: Render fornece HTTPS gratuito automaticamente

4. **Validação**: Sempre valide uploads no servidor

---

## 💰 Custos Estimados

### Render.com

| Plan | Preço | CPU | RAM | Banda |
|------|-------|-----|-----|-------|
| Free | $0/mês | 0.1 CPU | 512 MB | 100 GB/mês |
| Starter | $7/mês | 0.5 CPU | 512 MB | 100 GB/mês |
| Standard | $25/mês | 1 CPU | 2 GB | 500 GB/mês |

### Cloudinary (Imagens)

| Plan | Preço | Armazenamento | Banda | Transformações |
|------|-------|---------------|-------|----------------|
| Free | $0/mês | 25 GB | 25 GB/mês | 25,000/mês |
| Plus | $89/mês | 100 GB | 100 GB/mês | 100,000/mês |

### **Recomendação**: Free tier de ambos para começar (Total: $0/mês) 🎉

---

## 🚀 Comandos Úteis

### Desenvolvimento Local

```bash
# Instalar dependências
npm install

# Iniciar servidor local
npm start

# Modo desenvolvimento (auto-reload)
npm run dev
```

### Git

```bash
# Commit e push para deploy automático
git add .
git commit -m "Atualização do catálogo"
git push origin main
```

### Render CLI

```bash
# Instalar Render CLI
npm install -g render-cli

# Login
render login

# Ver logs em tempo real
render logs -f

# Restart do serviço
render restart
```

---

## 📞 Suporte

- **Render Docs**: https://render.com/docs
- **Cloudinary Docs**: https://cloudinary.com/documentation
- **Issues**: Criar issue no repositório Git

---

## 🎉 Checklist Final

Antes de fazer deploy, verifique:

- [ ] `package.json` atualizado com todas as dependências
- [ ] Sharp instalado (`npm install sharp`)
- [ ] Variáveis de ambiente configuradas no Render
- [ ] `.gitignore` criado e configurado
- [ ] Código testado localmente
- [ ] Build Command configurado corretamente
- [ ] Start Command configurado corretamente
- [ ] Porta dinâmica configurada (`process.env.PORT`)
- [ ] CORS configurado para aceitar requisições
- [ ] Python 3 disponível no ambiente

---

**Deploy Completo!** 🎊

Seu catálogo está online em: `https://catalogo-enxoval-dominic.onrender.com`

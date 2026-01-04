# 📦 Catálogo de Enxoval - Pertences do Dominic

## 🚀 Como Usar o Catálogo

### Opção 1: Visualizar Apenas (Sem Adicionar Produtos)

Se você só quer **visualizar** o catálogo sem adicionar produtos novos:

1. Abra o arquivo `index.html` diretamente no navegador
2. Navegue pelas categorias no menu lateral
3. Clique nas imagens para ampliá-las

---

### Opção 2: Adicionar Produtos e Categorias (Requer Servidor)

Para **adicionar novos produtos e categorias**, siga os passos abaixo:

#### 1️⃣ Instalar Dependências

Abra o Terminal e navegue até a pasta do projeto:

```bash
cd "/Users/rafaelthomas/Desktop/Dominic/Catálogo/Pertences"
```

Instale as dependências do Node.js (precisa fazer apenas uma vez):

```bash
npm install
```

#### 2️⃣ Iniciar o Servidor

Inicie o servidor local:

```bash
npm start
```

Você verá a mensagem:
```
🚀 Servidor rodando em http://localhost:3000
```

#### 3️⃣ Acessar o Catálogo

Abra o navegador e acesse:

```
http://localhost:3000/index.html
```

#### 4️⃣ Adicionar Categorias

1. Clique no botão **"➕ Categoria"** na barra lateral
2. Preencha:
   - **Nome da Categoria** (obrigatório): Ex: "Roupas"
   - **Subcategoria** (opcional): Ex: "6-9 meses"
3. Clique em **"Criar Categoria"**
4. A pasta será criada automaticamente!

#### 5️⃣ Adicionar Produtos

1. Clique no botão **"📦 Produto"** na barra lateral
   - OU clique em **"➕ Adicionar Produto"** dentro de uma categoria
2. Preencha:
   - **Categoria**: Selecione a categoria
   - **Subcategoria**: Selecione a subcategoria (se houver)
   - **Nome do Produto**: Ex: "Body Azul com Estrelas"
   - **Imagem**: Escolha o arquivo de imagem (JPG, PNG, GIF, WEBP - máx 5MB)
3. Clique em **"Adicionar Produto"**
4. A imagem será salva na pasta correta e o catálogo será atualizado automaticamente!

#### 6️⃣ Parar o Servidor

Quando terminar de usar, pare o servidor pressionando:

```
Ctrl + C
```

---

## 📁 Estrutura de Pastas

```
Pertences/
├── index.html              # Catálogo principal
├── server.js               # Servidor Node.js
├── package.json            # Dependências
├── generate_catalog.py     # Script para regenerar HTML
├── INSTRUCOES.md          # Este arquivo
│
├── Brinquedos/            # Exemplo de categoria
│   ├── Chocalho.jpg
│   └── Livro.jpg
│
└── Body/                  # Exemplo com subcategorias
    ├── 0-3 meses/
    │   ├── Com Manga/
    │   │   ├── 1.jpg
    │   │   └── 2.jpg
    │   └── Sem Manga/
    │       ├── 1.jpg
    │       └── 2.jpg
    └── 6-9 meses/
        └── ...
```

---

## 🔧 Troubleshooting

### Erro: "Erro ao conectar com o servidor"

**Solução**: Certifique-se de que o servidor está rodando com `npm start`

### Erro: "npm: command not found"

**Solução**: Você precisa instalar o Node.js primeiro:
1. Acesse: https://nodejs.org/
2. Baixe e instale a versão LTS (recomendada)
3. Reinicie o Terminal e tente novamente

### Erro: "Cannot find module..."

**Solução**: Execute `npm install` novamente na pasta do projeto

### Produtos não aparecem depois de adicionar

**Solução**:
1. Aguarde a mensagem "Catálogo atualizado com sucesso!"
2. A página será recarregada automaticamente
3. Se não funcionar, recarregue manualmente (⌘ + R ou F5)

---

## 🎨 Funcionalidades

✅ Navegação lateral com categorias e subcategorias
✅ Grid responsivo de imagens
✅ Modal para visualização ampliada
✅ Adicionar categorias e subcategorias
✅ Upload de produtos com imagens
✅ Preview da imagem antes de salvar
✅ Atualização automática do catálogo
✅ Validação de arquivos (tipo e tamanho)
✅ Mensagens de sucesso/erro

---

## 📝 Notas

- As imagens são salvas automaticamente nas pastas corretas
- O catálogo HTML é regenerado automaticamente após adicionar produtos
- Formatos de imagem aceitos: JPG, JPEG, PNG, GIF, WEBP
- Tamanho máximo de imagem: 5MB
- O servidor roda localmente na porta 3000

---

## 💡 Dicas

- Organize os produtos por **idade** (0-3 meses, 6-9 meses, etc.)
- Use nomes descritivos para os produtos
- Tire fotos claras e bem iluminadas
- Mantenha o servidor rodando enquanto adiciona múltiplos produtos
- Use subcategorias para melhor organização (Ex: "Com Manga", "Sem Manga")

---

**Desenvolvido para o Dominic** ❤️

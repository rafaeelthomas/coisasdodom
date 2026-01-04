#!/bin/bash

echo "🚀 Iniciando o Catálogo de Enxoval..."
echo ""

# Verificar se o Node.js está instalado
if ! command -v node &> /dev/null; then
    echo "❌ Node.js não encontrado!"
    echo "📥 Por favor, instale o Node.js de https://nodejs.org/"
    exit 1
fi

# Verificar se as dependências estão instaladas
if [ ! -d "node_modules" ]; then
    echo "📦 Instalando dependências..."
    npm install
    echo ""
fi

# Iniciar o servidor em background
echo "🌐 Iniciando servidor local..."
node server.js &
SERVER_PID=$!

# Aguardar o servidor iniciar
sleep 2

# Abrir o navegador
echo "🌍 Abrindo navegador..."
open "http://localhost:3000/index.html"

echo ""
echo "✅ Catálogo iniciado com sucesso!"
echo ""
echo "📝 Instruções:"
echo "   - O navegador foi aberto automaticamente"
echo "   - Use os botões ➕ Categoria e 📦 Produto para adicionar itens"
echo "   - Para parar o servidor, pressione Ctrl+C"
echo ""
echo "⚠️  Deixe esta janela aberta enquanto usa o catálogo!"
echo ""

# Aguardar o servidor
wait $SERVER_PID

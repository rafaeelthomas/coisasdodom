#!/usr/bin/env python3
import os
import json
from urllib.parse import quote
import re

def natural_sort_key(s):
    """
    Função para ordenação natural (alfanumérica)
    Exemplo: 1.jpg, 2.jpg, 10.jpg em vez de 1.jpg, 10.jpg, 2.jpg
    """
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split('([0-9]+)', s)]

base_dir = os.path.dirname(os.path.abspath(__file__))
categories = {}

# Extensões de imagem válidas
image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}

# Percorrer todos os diretórios
for item in sorted(os.listdir(base_dir), key=natural_sort_key):
    item_path = os.path.join(base_dir, item)

    # Ignorar arquivos ocultos, pastas especiais e arquivos
    if (item.startswith('.') or
        item in ['thumbmails', 'node_modules'] or
        item.endswith('.html') or
        item.endswith('.js') or
        item.endswith('.json') or
        item.endswith('.py') or
        item.endswith('.sh') or
        item.endswith('.md') or
        not os.path.isdir(item_path)):
        continue

    # Coletar imagens da pasta com estrutura de subpastas
    for root, dirs, files in os.walk(item_path):
        # Ignorar pastas ocultas e node_modules
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
        dirs.sort(key=natural_sort_key)

        # Ordenar arquivos com ordenação natural
        sorted_files = sorted(files, key=natural_sort_key)

        for file in sorted_files:
            if os.path.splitext(file.lower())[1] in image_extensions:
                # Caminho relativo da imagem
                rel_path = os.path.relpath(os.path.join(root, file), base_dir)

                # Determinar subcategoria se houver
                rel_to_category = os.path.relpath(root, item_path)
                subcategory = rel_to_category if rel_to_category != '.' else None

                if item not in categories:
                    categories[item] = {}

                if subcategory:
                    if subcategory not in categories[item]:
                        categories[item][subcategory] = []
                    categories[item][subcategory].append({
                        'filename': file,
                        'path': rel_path
                    })
                else:
                    if '__root__' not in categories[item]:
                        categories[item]['__root__'] = []
                    categories[item]['__root__'].append({
                        'filename': file,
                        'path': rel_path
                    })

print(f"✅ Encontradas {len(categories)} categorias")
total_items = sum(len(items) for subcat in categories.values() for items in subcat.values())
print(f"✅ Total de {total_items} itens")
print("✅ Catálogo HTML atualizado com sucesso!")

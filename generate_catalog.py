#!/usr/bin/env python3
import os
import json
from urllib.parse import quote
import urllib.parse
import re

def natural_sort_key(s):
    """
    Função para ordenação natural (alfanumérica)
    Exemplo: 1.jpg, 2.jpg, 10.jpg em vez de 1.jpg, 10.jpg, 2.jpg
    """
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split('([0-9]+)', s)]

def url_encode_path(path):
    """
    Codifica um caminho de arquivo para URL, mantendo as barras
    """
    # Dividir por / para codificar cada parte separadamente
    parts = path.split('/')
    # Codificar cada parte (quote com safe='' para codificar espaços também)
    encoded_parts = [urllib.parse.quote(part, safe='') for part in parts]
    # Juntar novamente com /
    return '/'.join(encoded_parts)

def get_thumbnail_path(image_path, base_dir):
    """
    Retorna o caminho do thumbnail se existir, caso contrário retorna o caminho original
    """
    # Caminho absoluto do thumbnail
    thumbnail_abs = os.path.join(base_dir, '.thumbnails', image_path)
    if os.path.exists(thumbnail_abs):
        # Retornar caminho relativo para usar no HTML
        return os.path.join('.thumbnails', image_path).replace('\\', '/')
    # Se thumbnail não existe, usar imagem original
    return image_path.replace('\\', '/')

base_dir = os.path.dirname(os.path.abspath(__file__))
categories = {}

# Extensões de imagem válidas
image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}

# Percorrer todos os diretórios
for item in sorted(os.listdir(base_dir), key=natural_sort_key):
    item_path = os.path.join(base_dir, item)

    # Ignorar arquivos ocultos, pastas especiais e arquivos
    # IMPORTANTE: thumbmails é uma pasta com imagens antigas/duplicadas, não thumbnails!
    if (item.startswith('.') or
        item in ['node_modules', 'thumbmails'] or
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
                        'path': rel_path,
                        'thumbnail': get_thumbnail_path(rel_path, base_dir)
                    })
                else:
                    if '__root__' not in categories[item]:
                        categories[item]['__root__'] = []
                    categories[item]['__root__'].append({
                        'filename': file,
                        'path': rel_path,
                        'thumbnail': get_thumbnail_path(rel_path, base_dir)
                    })

# Ler o HTML template existente
html_path = os.path.join(base_dir, 'index.html')
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Encontrar onde começa e termina o conteúdo dinâmico
# O conteúdo dinâmico fica entre o </nav> da sidebar e o início dos modals
content_start_marker = '<!-- CONTENT START -->'
content_end_marker = '<!-- CONTENT END -->'

# Se os marcadores não existem, vamos usar padrões
if content_start_marker not in html_content:
    # Procurar pelo fim da sidebar e início do main content
    sidebar_end = html_content.find('</nav>')
    if sidebar_end == -1:
        sidebar_end = html_content.find('<div class="main-content">')

    # Procurar pelo início dos modals
    modal_start = html_content.find('<div class="modal" id="imageModal"')
    if modal_start == -1:
        modal_start = html_content.find('<div id="imageModal"')

    # Dividir o HTML em três partes: header, content, footer
    if sidebar_end > -1 and modal_start > -1:
        # Encontrar o início do main-content
        main_content_start = html_content.find('<main class="main-content"', sidebar_end)
        if main_content_start > -1:
            # Encontrar o final da tag de abertura
            main_content_start = html_content.find('>', main_content_start) + 1
            # Encontrar onde termina o main-content
            # Procurar por </main> antes dos modals
            search_area = html_content[main_content_start:modal_start]
            # O main-content termina com </main> seguido de modals
            last_closing_main = search_area.rfind('</main>')
            if last_closing_main > -1:
                html_header = html_content[:main_content_start]
                content_end_pos = main_content_start + last_closing_main
                html_footer = html_content[content_end_pos:]
            else:
                print("⚠️  Não foi possível identificar estrutura do HTML. Apenas contando itens.")
                html_header = html_footer = None
        else:
            print("⚠️  Não foi possível identificar estrutura do HTML. Apenas contando itens.")
            html_header = html_footer = None
    else:
        print("⚠️  Não foi possível identificar estrutura do HTML. Apenas contando itens.")
        html_header = html_footer = None
else:
    # Usar marcadores explícitos
    header_end = html_content.find(content_start_marker) + len(content_start_marker)
    footer_start = html_content.find(content_end_marker)
    html_header = html_content[:header_end]
    html_footer = html_content[footer_start:]

# Gerar o conteúdo HTML das categorias
html_categories = []

# Gerar links da sidebar
sidebar_links = []
for category_name in sorted(categories.keys(), key=natural_sort_key):
    category_id = quote(category_name)
    subcats = categories[category_name]

    # Se tem apenas __root__, é categoria simples
    if len(subcats) == 1 and '__root__' in subcats:
        item_count = len(subcats['__root__'])
        sidebar_links.append(f'''
                    <li class="category-item">
                        <a href="#{category_id}" class="category-link" onclick="showSection('{category_id}', event)">
                            {category_name} <span style="float: right; opacity: 0.7;">({item_count})</span>
                        </a>
                    </li>''')
    else:
        # Categoria com subcategorias
        total_items = sum(len(items) for subcat, items in subcats.items() if subcat != '__root__')
        if '__root__' in subcats:
            total_items += len(subcats['__root__'])

        # Link da categoria principal vai abrir uma seção agregada com todas as subcategorias
        sidebar_links.append(f'''
                    <li class="category-item">
                        <a href="#{category_id}" class="category-link" onclick="showSection('{category_id}', event)">
                            {category_name} <span style="float: right; opacity: 0.7;">({total_items})</span>
                        </a>
                        <ul class="subcategory-list">''')

        # Adicionar subcategorias
        for subcat_name in sorted([k for k in subcats.keys() if k != '__root__'], key=natural_sort_key):
            subcat_id = quote(f"{category_name}/{subcat_name}")
            item_count = len(subcats[subcat_name])
            sidebar_links.append(f'''
                            <li class="subcategory-item">
                                <a href="#{subcat_id}" class="subcategory-link" onclick="showSection('{subcat_id}', event)">
                                    {subcat_name} ({item_count})
                                </a>
                            </li>''')

        sidebar_links.append('''
                        </ul>
                    </li>''')

# Gerar seções de conteúdo
content_sections = []
for category_name in sorted(categories.keys(), key=natural_sort_key):
    category_id = quote(category_name)
    subcats = categories[category_name]

    # Se tem apenas __root__, é categoria simples
    if len(subcats) == 1 and '__root__' in subcats:
        items = subcats['__root__']
        item_count = len(items)

        content_sections.append(f'''
            <section class="section" id="{category_id}" data-category="{category_name}">
                <div class="section-header">
                    <div class="section-header-info">
                        <h2>{category_name}</h2>
                        <span class="item-count">{item_count} {' item' if item_count == 1 else 'itens'}</span>
                    </div>
                    <button class="add-product-btn" onclick="openProductModal('{category_name}')">
                        ➕ Adicionar Produto
                    </button>
                </div>
                <div class="image-grid">''')

        # Adicionar itens
        for item in items:
            filename = os.path.splitext(item['filename'])[0]
            # Codificar caminhos para URL (necessário para Render.com)
            img_path = url_encode_path(item['path'].replace('\\', '/'))
            thumb_path = url_encode_path(item['thumbnail'].replace('\\', '/'))

            content_sections.append(f'''
                    <div class="image-card" onclick="openModal('{img_path}', '{filename}')">
                        <button class="delete-btn" onclick="openDeleteModal('{img_path}', '{filename}', event)" title="Deletar produto">
                            ✕
                        </button>
                        <div class="image-wrapper">
                            <img src="{thumb_path}" alt="{filename}" loading="lazy">
                        </div>
                        <div class="image-info">
                            <div class="image-name" title="{filename}">{filename}</div>
                        </div>
                    </div>''')

        content_sections.append('''
                </div>
            </section>''')

    else:
        # Categoria com subcategorias
        # Criar uma seção agregada que mostra TODAS as subcategorias juntas
        total_items = sum(len(items) for subcat, items in subcats.items() if subcat != '__root__')

        content_sections.append(f'''
            <section class="section" id="{category_id}" data-category="{category_name}">
                <div class="section-header">
                    <div class="section-header-info">
                        <h2>{category_name}</h2>
                        <span class="item-count">{total_items} itens</span>
                    </div>
                </div>''')

        # Adicionar cada subcategoria como um bloco dentro da seção agregada
        for subcat_name in sorted([k for k in subcats.keys() if k != '__root__'], key=natural_sort_key):
            items = subcats[subcat_name]
            item_count = len(items)
            full_path = f"{category_name}/{subcat_name}"

            content_sections.append(f'''
                <div style="margin-bottom: 40px;">
                    <div class="section-header">
                        <div class="section-header-info">
                            <h3 style="font-size: 1.3rem; color: #2c3e50; margin-bottom: 10px;">{subcat_name}</h3>
                            <span class="item-count">{item_count} {' item' if item_count == 1 else 'itens'}</span>
                        </div>
                        <button class="add-product-btn" onclick="openProductModal('{full_path}')">
                            ➕ Adicionar Produto
                        </button>
                    </div>
                    <div class="image-grid">''')

            # Adicionar itens desta subcategoria
            for item in items:
                filename = os.path.splitext(item['filename'])[0]
                img_path = url_encode_path(item['path'].replace('\\', '/'))
                thumb_path = url_encode_path(item['thumbnail'].replace('\\', '/'))

                content_sections.append(f'''
                        <div class="image-card" onclick="openModal('{img_path}', '{filename}')">
                            <button class="delete-btn" onclick="openDeleteModal('{img_path}', '{filename}', event)" title="Deletar produto">
                                ✕
                            </button>
                            <div class="image-wrapper">
                                <img src="{thumb_path}" alt="{filename}" loading="lazy">
                            </div>
                            <div class="image-info">
                                <div class="image-name" title="{filename}">{filename}</div>
                            </div>
                        </div>''')

            content_sections.append('''
                    </div>
                </div>''')

        content_sections.append('''
            </section>''')

        # Agora gerar seções individuais para cada subcategoria (para quando clicar em uma subcategoria específica)
        for subcat_name in sorted([k for k in subcats.keys() if k != '__root__'], key=natural_sort_key):
            items = subcats[subcat_name]
            item_count = len(items)
            subcat_id = quote(f"{category_name}/{subcat_name}")
            full_path = f"{category_name}/{subcat_name}"

            content_sections.append(f'''
            <section class="section" id="{subcat_id}" data-category="{category_name}" data-subcategory="{subcat_name}">
                <div class="section-header">
                    <div class="section-header-info">
                        <h2>{category_name} / {subcat_name}</h2>
                        <span class="item-count">{item_count} {' item' if item_count == 1 else 'itens'}</span>
                    </div>
                    <button class="add-product-btn" onclick="openProductModal('{full_path}')">
                        ➕ Adicionar Produto
                    </button>
                </div>
                <div class="image-grid">''')

            # Adicionar itens
            for item in items:
                filename = os.path.splitext(item['filename'])[0]
                img_path = url_encode_path(item['path'].replace('\\', '/'))
                thumb_path = url_encode_path(item['thumbnail'].replace('\\', '/'))

                content_sections.append(f'''
                    <div class="image-card" onclick="openModal('{img_path}', '{filename}')">
                        <button class="delete-btn" onclick="openDeleteModal('{img_path}', '{filename}', event)" title="Deletar produto">
                            ✕
                        </button>
                        <div class="image-wrapper">
                            <img src="{thumb_path}" alt="{filename}" loading="lazy">
                        </div>
                        <div class="image-info">
                            <div class="image-name" title="{filename}">{filename}</div>
                        </div>
                    </div>''')

            content_sections.append('''
                </div>
            </section>''')

        # Se tem itens na raiz
        if '__root__' in subcats:
            items = subcats['__root__']
            item_count = len(items)

            content_sections.append(f'''
            <section class="section" id="{category_id}" data-category="{category_name}">
                <div class="section-header">
                    <div class="section-header-info">
                        <h2>{category_name}</h2>
                        <span class="item-count">{item_count} {' item' if item_count == 1 else 'itens'}</span>
                    </div>
                    <button class="add-product-btn" onclick="openProductModal('{category_name}')">
                        ➕ Adicionar Produto
                    </button>
                </div>
                <div class="image-grid">''')

            # Adicionar itens
            for item in items:
                filename = os.path.splitext(item['filename'])[0]
                img_path = url_encode_path(item['path'].replace('\\', '/'))
                thumb_path = url_encode_path(item['thumbnail'].replace('\\', '/'))

                content_sections.append(f'''
                    <div class="image-card" onclick="openModal('{img_path}', '{filename}')">
                        <button class="delete-btn" onclick="openDeleteModal('{img_path}', '{filename}', event)" title="Deletar produto">
                            ✕
                        </button>
                        <div class="image-wrapper">
                            <img src="{thumb_path}" alt="{filename}" loading="lazy">
                        </div>
                        <div class="image-info">
                            <div class="image-name" title="{filename}">{filename}</div>
                        </div>
                    </div>''')

            content_sections.append('''
                </div>
            </section>''')

# Se conseguimos extrair o template, gerar HTML completo
if html_header and html_footer:
    # Atualizar os links da sidebar no header
    # Encontrar onde ficam os links da sidebar
    nav_start = html_header.find('<nav class="sidebar-nav">')
    if nav_start > -1:
        nav_end = html_header.find('</nav>', nav_start)
        if nav_end > -1:
            # Encontrar onde começa o conteúdo da nav (depois da tag de abertura completa)
            content_start = html_header.find('>', nav_start) + 1
            # Substituir o conteúdo da nav, envolvendo em <ul class="category-list">
            sidebar_content = '\n                <ul class="category-list" id="categoryList">\n' + ''.join(sidebar_links) + '\n                </ul>\n            '
            new_header = html_header[:content_start] + sidebar_content + html_header[nav_end:]
            html_header = new_header

    # Montar HTML final
    final_html = html_header + '\n' + ''.join(content_sections) + '\n        ' + html_footer

    # Salvar o arquivo
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(final_html)

    print(f"✅ Encontradas {len(categories)} categorias")
    total_items = sum(len(items) for subcat in categories.values() for items in subcat.values())
    print(f"✅ Total de {total_items} itens")
    print("✅ Catálogo HTML atualizado com sucesso!")
else:
    # Apenas mostrar estatísticas
    print(f"✅ Encontradas {len(categories)} categorias")
    total_items = sum(len(items) for subcat in categories.values() for items in subcat.values())
    print(f"✅ Total de {total_items} itens")
    print("⚠️  HTML não foi modificado (estrutura não identificada)")

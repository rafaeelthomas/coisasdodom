#!/usr/bin/env python3
"""
Script para renomear arquivos e pastas removendo caracteres especiais
Converte: ç→c, ã→a, õ→o, ê→e, etc.
"""
import os
import re
import shutil
import unicodedata
from pathlib import Path

def remove_accents(text):
    """Remove acentos e caracteres especiais de uma string"""
    # Normalizar Unicode para NFC primeiro
    text = unicodedata.normalize('NFC', text)

    # Mapeamento de caracteres especiais para versões sem acento
    replacements = {
        'á': 'a', 'à': 'a', 'ã': 'a', 'â': 'a', 'ä': 'a',
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
        'ó': 'o', 'ò': 'o', 'õ': 'o', 'ô': 'o', 'ö': 'o',
        'ú': 'u', 'ù': 'u', 'û': 'u', 'ü': 'u',
        'ç': 'c',
        'ñ': 'n',
        'Á': 'A', 'À': 'A', 'Ã': 'A', 'Â': 'A', 'Ä': 'A',
        'É': 'E', 'È': 'E', 'Ê': 'E', 'Ë': 'E',
        'Í': 'I', 'Ì': 'I', 'Î': 'I', 'Ï': 'I',
        'Ó': 'O', 'Ò': 'O', 'Õ': 'O', 'Ô': 'O', 'Ö': 'O',
        'Ú': 'U', 'Ù': 'U', 'Û': 'U', 'Ü': 'U',
        'Ç': 'C',
        'Ñ': 'N',
    }

    result = text
    for old, new in replacements.items():
        result = result.replace(old, new)

    # Remover espaços no final
    result = result.rstrip()

    return result

def rename_in_directory(base_path, dry_run=False):
    """Renomeia arquivos e pastas em um diretório"""
    base_path = Path(base_path)
    changes = []

    # Pastas a ignorar
    ignore_dirs = {'.git', 'node_modules', 'thumbmails'}

    # Primeiro, coletar todas as mudanças necessárias
    # Começar dos níveis mais profundos para evitar problemas
    all_paths = []
    for root, dirs, files in os.walk(base_path, topdown=False):
        # Remover pastas ignoradas
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        root_path = Path(root)

        # Adicionar arquivos
        for file in files:
            file_path = root_path / file
            all_paths.append((file_path, False))  # False = é arquivo

        # Adicionar diretórios
        for dir_name in dirs:
            dir_path = root_path / dir_name
            all_paths.append((dir_path, True))  # True = é diretório

    # Processar mudanças
    for path, is_dir in all_paths:
        old_name = unicodedata.normalize('NFC', path.name)
        new_name = remove_accents(old_name)

        # Debug: mostrar o que está sendo processado
        if dry_run and ('ç' in old_name.lower() or 'ã' in old_name.lower() or 'õ' in old_name.lower()):
            print(f"DEBUG: Processando '{old_name}' → '{new_name}' (igual: {old_name == new_name})")

        if old_name != new_name:
            new_path = path.parent / new_name

            type_str = "DIR " if is_dir else "FILE"
            rel_old = path.relative_to(base_path)
            rel_new = new_path.relative_to(base_path)

            changes.append({
                'old': path,
                'new': new_path,
                'rel_old': str(rel_old),
                'rel_new': str(rel_new),
                'is_dir': is_dir
            })

            print(f"[{type_str}] {rel_old} → {rel_new}")

            if not dry_run:
                try:
                    # Renomear
                    path.rename(new_path)
                    print(f"  ✅ Renomeado com sucesso")
                except Exception as e:
                    print(f"  ❌ Erro: {e}")

    return changes

if __name__ == '__main__':
    import sys

    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Verificar se foi passado argumento --yes ou -y
    auto_confirm = len(sys.argv) > 1 and sys.argv[1] in ['--yes', '-y']

    print("=" * 80)
    print("SCRIPT DE RENOMEAÇÃO DE ARQUIVOS")
    print("=" * 80)
    print(f"Diretório base: {base_dir}")
    print()

    # Primeiro fazer um dry-run para mostrar o que será mudado
    print("🔍 SIMULAÇÃO (DRY RUN) - Nenhuma alteração será feita ainda:")
    print("-" * 80)
    changes = rename_in_directory(base_dir, dry_run=True)

    if not changes:
        print("✅ Nenhum arquivo ou pasta precisa ser renomeado!")
        sys.exit(0)

    print()
    print(f"📊 Total de mudanças: {len(changes)}")
    print()

    # Confirmar com o usuário
    if auto_confirm:
        response = 's'
        print("⚡ Auto-confirmado via argumento --yes")
    else:
        response = input("Deseja executar as mudanças? (s/N): ").strip().lower()

    if response == 's' or response == 'sim':
        print()
        print("🔄 EXECUTANDO MUDANÇAS:")
        print("-" * 80)
        changes = rename_in_directory(base_dir, dry_run=False)

        print()
        print(f"✅ Concluído! {len(changes)} arquivos/pastas renomeados.")
        print()
        print("⚠️  PRÓXIMOS PASSOS:")
        print("1. Execute: python3 generate_catalog.py")
        print("2. Faça commit: git add . && git commit -m 'Renomeia arquivos removendo acentos'")
        print("3. Faça push: git push")
    else:
        print()
        print("❌ Operação cancelada pelo usuário.")

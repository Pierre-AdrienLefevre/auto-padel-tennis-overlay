#!/usr/bin/env python3
"""
Script pour créer un exécutable standalone (.exe) avec PyInstaller.
Usage: python build_exe.py
"""

import sys

import PyInstaller.__main__


def build():
    """Construit l'exécutable."""

    # Déterminer le séparateur de chemin selon l'OS
    # Windows utilise ';', macOS/Linux utilisent ':'
    separator = ';' if sys.platform == 'win32' else ':'

    # Options PyInstaller
    options = [
        'app.py',  # Script principal
        '--name=PadelOverlayGenerator',  # Nom de l'exe
        '--onefile',  # Un seul fichier exe
        '--windowed',  # Pas de console (GUI seulement)
        f'--add-data=utils{separator}utils',  # Inclure le package utils
        '--hidden-import=PyQt6',
        '--hidden-import=PIL',
        '--hidden-import=openpyxl',
        '--hidden-import=lxml',
        '--hidden-import=requests',
        '--clean',  # Nettoyer avant build
        '--noconfirm',  # Pas de confirmation
    ]

    PyInstaller.__main__.run(options)


if __name__ == "__main__":
    print("[BUILD] Construction de l'executable...")
    print("=" * 50)
    build()
    print("=" * 50)
    print("[OK] Build termine!")
    print("[INFO] L'executable se trouve dans le dossier 'dist/'")

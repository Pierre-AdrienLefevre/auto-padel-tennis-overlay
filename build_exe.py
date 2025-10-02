#!/usr/bin/env python3
"""
Script pour créer un exécutable standalone (.exe) avec PyInstaller.
Usage: python build_exe.py
"""

import PyInstaller.__main__


def build():
    """Construit l'exécutable."""

    # Options PyInstaller
    PyInstaller.__main__.run([
        'app.py',  # Script principal
        '--name=PadelOverlayGenerator',  # Nom de l'exe
        '--onefile',  # Un seul fichier exe
        '--windowed',  # Pas de console (GUI seulement)
        '--icon=NONE',  # TODO: Ajouter une icône
        '--add-data=overlay_generator.py;.',  # Inclure le module overlay
        '--hidden-import=PyQt6',
        '--hidden-import=PIL',
        '--hidden-import=openpyxl',
        '--hidden-import=lxml',
        '--hidden-import=requests',
        '--clean',  # Nettoyer avant build
        '--noconfirm',  # Pas de confirmation
    ])


if __name__ == "__main__":
    print("🔨 Construction de l'exécutable...")
    print("=" * 50)
    build()
    print("=" * 50)
    print("✅ Build terminé!")
    print("📦 L'exécutable se trouve dans le dossier 'dist/'")

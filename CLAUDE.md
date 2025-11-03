# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Padel Video Overlay Generator** - Application PyQt6 desktop pour générer automatiquement des overlays de score sur des
vidéos de padel. Le workflow complet :

1. L'utilisateur édite sa vidéo de match de padel dans Adobe Premiere Pro, en la découpant point par point
2. Export de la timeline en Final Cut Pro XML (Fichier → Exporter → Final Cut Pro XML)
3. Les scores sont maintenus dans un fichier Excel (`match_points.xlsx`)
4. L'application PyQt6 (`app.py`) permet de :
    - Sélectionner les fichiers nécessaires (XML, Excel, vidéos)
    - Lancer le traitement automatique avec suivi de progression en temps réel
5. Le script Python (`main.py`) traite automatiquement :
    - Parse le XML pour extraire les timestamps de chaque clip
    - Lit le fichier Excel pour récupérer les scores
    - Génère des overlays PNG avec les scores (`utils/overlay_generator.py`)
    - Produit la vidéo finale avec overlays via FFmpeg (GPU-accelerated)

## Structure du Projet

```
.
├── app.py                          # Application PyQt6 (interface graphique)
├── main.py                         # Moteur de traitement vidéo
├── utils/
│   ├── overlay_generator.py        # Générateur d'overlays de score
│   └── build_exe.py                # Script de build PyInstaller
├── tests/
│   ├── test_main.py                # Tests unitaires pour main.py
│   └── test_overlay_generator.py   # Tests unitaires pour overlay_generator.py
├── .github/
│   ├── workflows/
│   │   ├── tests.yml               # CI: Tests automatiques (Windows + macOS)
│   │   ├── build.yml               # CI: Build des exécutables
│   │   └── release.yml             # CI: Release automatique avec versioning sémantique
│   └── instructions/
│       └── default.instructions.md # Instructions pour GitHub Copilot
├── pyproject.toml                  # Configuration Python + dépendances
├── WORKFLOW.md                     # Documentation du workflow Git et releases
└── README.md                       # Documentation utilisateur
```

## Fichiers Clés

### Code Source

- **`app.py`** - Interface graphique PyQt6 avec suivi de progression, vérification de mises à jour
- **`main.py`** - Script d'automatisation principal (parsing XML/Excel, traitement vidéo parallèle)
- **`utils/overlay_generator.py`** - Générateur d'overlays de score (design professionnel avec ombres)
- **`utils/build_exe.py`** - Script pour créer les exécutables Windows/macOS avec PyInstaller

### Tests

- **`tests/test_main.py`** - 19 tests unitaires (fonctions de conversion, formatage, parsing)
- **`tests/test_overlay_generator.py`** - 15 tests unitaires (parsing de scores, génération d'images)
- Couverture de code : focus sur les fonctions pures et critiques

### Données (exemples)

- **`data/Sequence_timeframe.xml`** - Exemple d'export Premiere Pro (Final Cut Pro XML)
- **`data/match_points.xlsx`** - Fichier Excel avec les scores de chaque point
- **`data/VID_*.mp4`** - Fichiers vidéo sources (très volumineux, 13GB+)

## Structure XML (Export Premiere Pro)

Format Final Cut Pro XML avec :

- Multiples éléments `<clipitem>`, un par segment/point de la timeline
- Chaque clipitem contient :
    - `<start>` et `<end>` - Position dans la timeline (en frames)
    - `<in>` et `<out>` - Timecodes du fichier source (en frames)
    - Frame rate: 60fps avec timing NTSC (`<timebase>60</timebase><ntsc>TRUE</ntsc>`)
- Fichiers sources référencés via `<file>` avec `<pathurl>`

## Structure Excel

Le fichier `match_points.xlsx` contient :

- **Colonnes** : Set, Num_Point, Set1, Set2, Jeux, Points, Commentaires
- **Format des scores** : "3/2" (équipe1/équipe2)
- Une ligne par point correspondant à chaque clip de la timeline

## Environnement de Développement

### Technologies

- **Python 3.13+**
- **PyQt6** - Interface graphique
- **FFmpeg** - Traitement vidéo (requis, avec support GPU)
- **Pillow** - Génération d'images overlay
- **lxml** - Parsing XML
- **openpyxl** - Lecture Excel

### Configuration

- **`pyproject.toml`** - Gestion des dépendances et configuration pytest
- **Installation** : `pip install -e ".[dev]"` (inclut pytest pour les tests)
- **Tests** : `pytest tests/ -v`
- **Build** : `python utils/build_exe.py`

### GitHub Actions CI/CD

- **Tests automatiques** : Lancés sur chaque PR (Windows + macOS)
- **Builds automatiques** : Générés sur PR vers `main`
- **Releases automatiques** : Versioning sémantique basé sur conventional commits
    - `feat:` → version MINOR (0.8.0 → 0.9.0)
    - `fix:` → version PATCH (0.8.0 → 0.8.1)
    - `feat!:` ou `BREAKING CHANGE:` → version MAJOR (0.8.0 → 1.0.0)

## Notes d'Implémentation

### Traitement Vidéo

- **Parallélisation** : ThreadPoolExecutor avec 4 workers pour traiter plusieurs segments simultanément
- **GPU Acceleration** : Détection automatique (NVENC sur Windows/Linux, VideoToolbox sur macOS)
- **NTSC Timing** : Gestion du framerate drop-frame (59.94fps)
- **Optimisations** : Copie audio sans réencodage, bitrate adaptatif

### Overlays

- **Position** : Bas-gauche de la vidéo (96px du bord gauche, 241px du bas)
- **Style** : Design professionnel avec ombres portées, coins arrondis
- **Résolution** : Support 4K (3840x2160) et autres résolutions
- **Polices** : Détection automatique multi-plateforme (Arial Bold, Helvetica, etc.)

### Tests

- **34 tests unitaires** couvrant les fonctions pures et critiques
- **Fixtures pytest** pour créer des fichiers temporaires
- **Pas de dépendance FFmpeg** dans les tests (rapidité)

### Compatibilité

- **Windows** : Exécutable `.exe` généré avec PyInstaller
- **macOS** : Application native (ARM64 + Intel via Rosetta)
- **Encodage** : Tous les messages évitent les emojis/Unicode pour compatibilité Windows console

## Workflow Git (voir WORKFLOW.md pour détails)

### Branches

- **`main`** - Code stable, protégé, déclenche les releases automatiques
- **`develop`** - Développement en cours
- **`feature/*`** - Branches de fonctionnalités

### Conventional Commits

Les messages de commit déterminent automatiquement la version :

```bash
feat: nouvelle fonctionnalité        # MINOR bump
fix: correction de bug                # PATCH bump
feat!: breaking change                # MAJOR bump
docs: mise à jour documentation       # PATCH bump
test: ajout de tests                  # PATCH bump
```

## Commandes Utiles

```bash
# Installation
pip install -e ".[dev]"

# Tests
pytest tests/ -v
pytest tests/ --cov=. --cov-report=html  # Avec couverture

# Build
python utils/build_exe.py

# Linter (si configuré)
ruff check .

# Lancer l'application
python app.py
```

## Considérations Importantes

- Les vidéos sources sont **très volumineuses** (13GB+) - efficacité critique
- Le nombre de clips XML doit correspondre au nombre de lignes Excel
- Chaque clip = un point dans le match
- FFmpeg doit être installé et accessible dans le PATH
- GPU fortement recommandé pour performances acceptables
- Les tests CI ne testent pas FFmpeg (trop lourd), uniquement les fonctions pures

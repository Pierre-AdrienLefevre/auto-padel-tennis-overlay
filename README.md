# 🎾 Padel Video Overlay Generator

[🇫🇷 Français](#français) | [🇬🇧 English](#english)

---

## Français

**Application desktop automatique pour générer des overlays de score professionnels sur des vidéos de padel/tennis.**
Lit les timelines Premiere Pro XML et les fichiers Excel de scores pour ajouter automatiquement des overlays avec FFmpeg
accéléré GPU.

[![Tests](https://github.com/Pierre-AdrienLefevre/auto-padel-tennis-overlay/workflows/Tests%20et%20V%C3%A9rifications/badge.svg)](https://github.com/Pierre-AdrienLefevre/auto-padel-tennis-overlay/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)

### ✨ Fonctionnalités

- 🖥️ **Interface PyQt6** - Application desktop conviviale avec suivi de progression en temps réel
- 📹 **Traitement Automatique** - Extrait les clips depuis les exports XML Premiere Pro
- 📊 **Intégration Excel** - Lit les scores depuis des fichiers Excel
- 🎨 **Overlays Professionnels** - Design épuré avec ombres portées et coins arrondis
- ⚡ **Accélération GPU** - Support VideoToolbox (macOS) et NVENC (Windows)
- 🎯 **Support 4K** - Optimisé pour la vidéo 4K (3840x2160)
- 🔄 **Support Multi-Sets** - Affiche automatiquement les sets complétés
- 🧵 **Traitement Parallèle** - Traite plusieurs segments vidéo simultanément
- 🔔 **Vérification Auto-MAJ** - Notifie quand une nouvelle version est disponible
- 🧪 **Tests Automatisés** - 34 tests unitaires avec CI/CD GitHub Actions

### 🚀 Installation

#### Prérequis

- **Python 3.13+** (ou utilisez les exécutables pré-compilés)
- **FFmpeg** avec support d'accélération matérielle
- **Adobe Premiere Pro** (pour l'export XML)

#### Option 1 : Exécutables Pré-compilés (Recommandé)

Téléchargez la dernière version
depuis [Releases](https://github.com/Pierre-AdrienLefevre/auto-padel-tennis-overlay/releases)

**Windows :**

```powershell
# Téléchargez PadelOverlayGenerator-Windows.exe
# Installez FFmpeg : https://ffmpeg.org/download.html
# Double-cliquez sur l'exécutable
```

**macOS :**

```bash
# Téléchargez PadelOverlayGenerator-macOS
# Installez FFmpeg : brew install ffmpeg
chmod +x PadelOverlayGenerator-macOS
./PadelOverlayGenerator-macOS
```

#### Option 2 : Installation depuis Source

```bash
git clone https://github.com/Pierre-AdrienLefevre/auto-padel-tennis-overlay.git
cd auto-padel-tennis-overlay
pip install -e .
python app.py
```

### 📖 Utilisation

#### 1. Préparer vos Fichiers

**Fichier Excel (`match_points.xlsx`):**

| Set | Num_Point | Set1 | Set2 | Jeux | Points | Commentaires |
|-----|-----------|------|------|------|--------|--------------|
| 1   | 1         |      |      | 0/0  | 0/15   |              |
| 1   | 2         |      |      | 0/0  | 0/40   |              |

**Export Premiere Pro :**

1. Découpez votre vidéo point par point
2. Exportez : **Fichier → Exporter → Final Cut Pro XML**

#### 2. Lancer l'Application

1. Ouvrez l'application
2. Sélectionnez XML, Excel, et dossier vidéos
3. Cliquez sur "Générer la vidéo avec overlays"
4. Suivez la progression
5. Vidéo finale dans `output/`

### 🔧 Détails Techniques

**Encodage GPU :**

| Plateforme    | Encodeur            | Config     |
|---------------|---------------------|------------|
| macOS         | `hevc_videotoolbox` | Quality 70 |
| Windows/Linux | `hevc_nvenc`        | Preset p4  |
| CPU Fallback  | `libx264`           | Ultrafast  |

**Performance (4K) :**

- Avec GPU : 2-3 sec/segment
- Avec CPU : 8-12 sec/segment

### 🤝 Contribution

Utilisez [conventional commits](https://www.conventionalcommits.org/) :

- `feat:` → Version MINOR
- `fix:` → Version PATCH
- `feat!:` → Version MAJOR

### 📝 Évolutions Futures Possibles

- [ ] Support DaVinci Resolve XML
- [ ] Thèmes d'overlay personnalisables
- [ ] Mode batch pour plusieurs matchs
- [ ] Application Electron multiplateforme

### 📄 Licence

MIT License - voir [LICENSE](LICENSE)

---

## English

**Automated desktop application to generate professional score overlays for padel/tennis match videos.** Reads Premiere
Pro XML timelines and Excel score sheets to automatically add overlays using GPU-accelerated FFmpeg.

[![Tests](https://github.com/Pierre-AdrienLefevre/auto-padel-tennis-overlay/workflows/Tests%20et%20V%C3%A9rifications/badge.svg)](https://github.com/Pierre-AdrienLefevre/auto-padel-tennis-overlay/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)

### ✨ Features

- 🖥️ **PyQt6 Interface** - User-friendly desktop app with real-time progress tracking
- 📹 **Automatic Processing** - Extracts clips from Premiere Pro XML exports
- 📊 **Excel Integration** - Reads match scores from Excel files
- 🎨 **Professional Overlays** - Clean design with drop shadows and rounded corners
- ⚡ **GPU Acceleration** - VideoToolbox (macOS) and NVENC (Windows) support
- 🎯 **4K Support** - Optimized for 4K (3840x2160) video processing
- 🔄 **Multi-Set Support** - Automatically displays completed sets
- 🧵 **Parallel Processing** - Processes multiple video segments simultaneously
- 🔔 **Auto-Update Check** - Notifies when new version is available
- 🧪 **Automated Testing** - 34 unit tests with GitHub Actions CI/CD

### 🚀 Installation

#### Requirements

- **Python 3.13+** (or use pre-compiled executables)
- **FFmpeg** with hardware acceleration support
- **Adobe Premiere Pro** (for XML export)

#### Option 1: Pre-compiled Executables (Recommended)

Download latest version from [Releases](https://github.com/Pierre-AdrienLefevre/auto-padel-tennis-overlay/releases)

**Windows:**

```powershell
# Download PadelOverlayGenerator-Windows.exe
# Install FFmpeg: https://ffmpeg.org/download.html
# Double-click the executable
```

**macOS:**
```bash
# Download PadelOverlayGenerator-macOS
# Install FFmpeg: brew install ffmpeg
chmod +x PadelOverlayGenerator-macOS
./PadelOverlayGenerator-macOS
```

#### Option 2: Install from Source

```bash
git clone https://github.com/Pierre-AdrienLefevre/auto-padel-tennis-overlay.git
cd auto-padel-tennis-overlay
pip install -e .
python app.py
```

### 📖 Usage

#### 1. Prepare Your Files

**Excel File (`match_points.xlsx`):**

| Set | Num_Point | Set1 | Set2 | Games | Points | Comments |
|-----|-----------|------|------|-------|--------|----------|
| 1   | 1         |      |      | 0/0   | 0/15   |          |
| 1   | 2         |      |      | 0/0   | 0/40   |          |

**Premiere Pro Export:**

1. Cut your video point-by-point
2. Export: **File → Export → Final Cut Pro XML**

#### 2. Run the Application

1. Open the application
2. Select XML, Excel, and video folder
3. Click "Generate video with overlays"
4. Follow the progress
5. Final video in `output/`

### 🔧 Technical Details

**GPU Encoding:**

| Platform      | Encoder             | Config     |
|---------------|---------------------|------------|
| macOS         | `hevc_videotoolbox` | Quality 70 |
| Windows/Linux | `hevc_nvenc`        | Preset p4  |
| CPU Fallback  | `libx264`           | Ultrafast  |

**Performance (4K):**

- With GPU: 2-3 sec/segment
- With CPU: 8-12 sec/segment

### 🤝 Contributing

Use [conventional commits](https://www.conventionalcommits.org/):

- `feat:` → MINOR version
- `fix:` → PATCH version
- `feat!:` → MAJOR version

### 📝 Future Roadmap

- [ ] DaVinci Resolve XML support
- [ ] Customizable overlay themes
- [ ] Batch mode for multiple matches
- [ ] Cross-platform Electron app

### 📄 License

MIT License - see [LICENSE](LICENSE)

---

### 🙏 Acknowledgments / Remerciements

- Built with **Python**, **PyQt6**, **Pillow**, and **FFmpeg**
- Designed for padel/tennis video editors
- Inspired by professional sports broadcast overlays
- Automated testing with **pytest** and **GitHub Actions**

**Made with ❤️ for the padel/tennis community**

*Last update: November 2025 | Dernière mise à jour : Novembre 2025*

### 📞 Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/Pierre-AdrienLefevre/auto-padel-tennis-overlay/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/Pierre-AdrienLefevre/auto-padel-tennis-overlay/discussions)
- 📖 **Documentation**: See [WORKFLOW.md](WORKFLOW.md) and [CLAUDE.md](CLAUDE.md)

⭐ **Star the project if you find it useful!** | **Donnez une étoile si le projet vous est utile !**
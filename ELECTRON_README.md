# Application Electron - Padel Overlay Generator

Version Electron de l'application avec interface web moderne.

## 🚀 Installation et lancement

### Prérequis

- Node.js 18+ installé
- Python 3.13+ installé
- Dépendances Python installées (`uv sync`)

### Installation

```bash
# Installer les dépendances Node.js
npm install
```

### Lancement en mode développement

```bash
npm start
```

### Build de l'application

```bash
# Build pour Windows
npm run build:win

# L'exécutable se trouve dans dist-electron/
```

## 📁 Structure du projet

```
├── electron/
│   ├── main.js          # Processus principal Electron
│   └── preload.js       # Script preload (sécurité)
├── renderer/
│   ├── index.html       # Interface utilisateur
│   ├── styles.css       # Styles CSS
│   └── app.js           # Logique frontend
├── main.py              # Backend Python
├── overlay_generator.py # Générateur d'overlays
└── package.json         # Configuration npm
```

## ✨ Fonctionnalités

- ✅ Interface web moderne avec gradient
- ✅ Sélection de fichiers native
- ✅ Barre de progression en temps réel
- ✅ Communication IPC Electron ↔ Python
- ✅ Vérification automatique des mises à jour
- ✅ Logs en temps réel
- ✅ Auto-update intégré

## 🔧 Développement

### Mode développement avec DevTools

```bash
NODE_ENV=development npm start
```

### Communication Electron-Python

L'app utilise:

- **IPC (Inter-Process Communication)** pour la communication frontend ↔ main process
- **Subprocess Python** pour le traitement vidéo
- **Événements** pour les mises à jour de progression en temps réel

## 📦 Distribution

### Avantages vs PyQt

✅ Interface web moderne (HTML/CSS/JS)
✅ Auto-update natif
✅ Cross-platform facile
✅ DevTools intégrés
❌ Taille plus grande (~150 MB vs 48 MB)

### Packaging

```bash
npm run build:win
```

Produit:

- Un installeur NSIS (`.exe`)
- Application standalone dans `dist-electron/`

## 🔄 Mises à jour

L'application vérifie automatiquement les mises à jour sur GitHub au démarrage.

Configuration dans `electron/main.js`:

- Repo: `Pierre-AdrienLefevre/auto-padel-tennis-overlay`
- Version: Lue depuis `package.json`

## 🐛 Debug

### Logs Python

Les logs Python sont capturés et affichés dans l'interface.

### DevTools Electron

Ouvrir avec `Ctrl+Shift+I` ou `F12` en mode développement.

### Tester la communication IPC

Vérifier dans la console:

```javascript
window.electronAPI // Doit afficher les méthodes disponibles
```

## 📝 Notes

- Python doit être installé et accessible dans le PATH
- FFmpeg doit être installé pour le traitement vidéo
- Le backend Python tourne dans un subprocess séparé

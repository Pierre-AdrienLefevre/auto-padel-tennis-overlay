# Padel Video Overlay Generator

Application desktop pour générer automatiquement des overlays de score sur des vidéos de padel.

## 🚀 Installation

### Option 1: Utiliser l'exécutable (.exe) - RECOMMANDÉ pour les utilisateurs

1. Téléchargez le fichier `PadelOverlayGenerator.exe` depuis
   les [Releases GitHub](https://github.com/username/repo/releases)
2. Double-cliquez sur le fichier pour lancer l'application
3. C'est tout! Aucune installation requise

### Option 2: Lancer depuis le code source (pour développeurs)

```bash
# Installer les dépendances
uv sync

# Lancer l'application
python app.py
```

## 📖 Utilisation

### Étape 1: Préparer vos fichiers

1. **Fichier XML** - Exportez votre timeline Premiere Pro:
    - `Fichier → Exporter → Final Cut Pro XML`

2. **Fichier Excel** - Créez un fichier avec vos scores:
    - Colonnes: Set, Num_Point, Set 1, Set 2, Jeux, Points, Commentaires

3. **Dossier vidéos** - Placez tous vos clips vidéo sources dans un dossier

### Étape 2: Générer la vidéo

1. Ouvrez l'application `PadelOverlayGenerator`
2. Cliquez sur **Parcourir** pour sélectionner:
    - Le fichier XML
    - Le fichier Excel
    - Le dossier contenant les vidéos
    - Le nom de la vidéo finale (ex: `match_final.mp4`)
3. Cliquez sur **🚀 Générer la vidéo avec overlays**
4. Attendez la fin du traitement
5. Votre vidéo avec overlays est prête!

## ⚙️ Configuration requise

- **OS**: Windows 10/11 (64-bit)
- **GPU**: NVIDIA RTX (pour accélération CUDA/NVENC) - Recommandé
- **RAM**: 8 GB minimum, 16 GB recommandé
- **Espace disque**: ~100 MB pour l'app + espace pour les vidéos

## 🔄 Mises à jour

L'application vérifie automatiquement les mises à jour au démarrage.
Si une nouvelle version est disponible, vous serez notifié.

## 🛠️ Construction de l'exécutable (pour développeurs)

```bash
# Installer PyInstaller
pip install pyinstaller

# Construire l'exe
python build_exe.py

# L'exe se trouve dans dist/PadelOverlayGenerator.exe
```

## 📝 Notes techniques

### Optimisations GPU

- **Décodage**: NVDEC (GPU)
- **Encodage**: NVENC HEVC preset p3 (GPU)
- **Traitement parallèle**: 3 segments simultanés
- **Bitrate**: Auto-détecté depuis la vidéo source

### Performance attendue

- **RTX 5070**: ~1-2 minutes pour 51 segments
- **RTX 4070**: ~2-3 minutes
- **CPU seulement**: ~15-20 minutes

## ❓ Dépannage

### "No NVENC capable devices found"

→ Votre GPU ne supporte pas NVENC. L'app utilisera le CPU (plus lent).

### "Erreur: FFmpeg not found"

→ Installez FFmpeg: https://ffmpeg.org/download.html

### Vidéo finale trop lourde

→ Ajustez le bitrate dans `main.py` ligne 74

## 📧 Support

Pour toute question ou problème, ouvrez une issue sur GitHub:
https://github.com/username/repo/issues

## 📜 Licence

MIT License - Voir LICENSE pour plus de détails

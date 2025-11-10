# Guide d'Installation - Padel Video Overlay Generator

## Introduction

Bienvenue dans le guide d'installation du **Padel Video Overlay Generator** ! Cette application vous permet d'ajouter
automatiquement des scores sur vos vidéos de padel en quelques clics.

Ce guide est conçu pour les vidéastes qui ne sont pas développeurs. Suivez simplement les étapes ci-dessous.

---

## Prérequis

Avant d'installer l'application, assurez-vous d'avoir :

- **Un ordinateur Windows (10 ou plus récent) ou macOS (10.15 Catalina ou plus récent)**
- **Adobe Premiere Pro** (pour éditer et exporter votre timeline)
- **Une connexion Internet** (pour télécharger les fichiers)

---

## Étape 1 : Télécharger l'application

### Pour Windows :

1. Rendez-vous sur la page des releases
   GitHub : [https://github.com/Pierre-AdrienLefevre/Automatisation_overlay_point/releases](https://github.com/Pierre-AdrienLefevre/Automatisation_overlay_point/releases)
2. Téléchargez le fichier **`PadelOverlay-Windows.exe`** (dernière version)
3. Enregistrez-le dans un dossier de votre choix (par exemple `C:\PadelOverlay`)

### Pour macOS :

1. Rendez-vous sur la page des releases
   GitHub : [https://github.com/Pierre-AdrienLefevre/Automatisation_overlay_point/releases](https://github.com/Pierre-AdrienLefevre/Automatisation_overlay_point/releases)
2. Téléchargez le fichier **`PadelOverlay-macOS.zip`** (dernière version)
3. Décompressez le fichier et déplacez l'application **`PadelOverlay.app`** dans votre dossier Applications
4. **Important pour macOS :** Au premier lancement, faites un clic droit sur l'application et choisissez "Ouvrir" (pour
   contourner la sécurité Gatekeeper)

---

## Étape 2 : Installer FFmpeg

FFmpeg est un logiciel gratuit qui permet de traiter les vidéos. Il est indispensable pour que l'application fonctionne.

### Pour Windows :

1. Téléchargez FFmpeg depuis le site
   officiel : [https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/)
2. Choisissez la version **"ffmpeg-release-essentials.zip"**
3. Décompressez le fichier dans un dossier (par exemple `C:\ffmpeg`)
4. **Ajouter FFmpeg au PATH :**
    - Ouvrez le menu Démarrer et cherchez "Variables d'environnement"
    - Cliquez sur "Modifier les variables d'environnement système"
    - Cliquez sur "Variables d'environnement..."
    - Dans la section "Variables système", trouvez la variable `Path` et cliquez sur "Modifier"
    - Cliquez sur "Nouveau" et ajoutez le chemin vers le dossier `bin` de FFmpeg (par exemple `C:\ffmpeg\bin`)
    - Cliquez sur "OK" pour valider
5. **Vérifier l'installation :**
    - Ouvrez l'Invite de commandes (tapez `cmd` dans le menu Démarrer)
    - Tapez `ffmpeg -version` et appuyez sur Entrée
    - Si l'installation est réussie, vous verrez la version de FFmpeg s'afficher

### Pour macOS :

1. Ouvrez le Terminal (Applications > Utilitaires > Terminal)
2. Installez Homebrew (si ce n'est pas déjà fait) en copiant cette commande :
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
3. Installez FFmpeg avec cette commande :
   ```bash
   brew install ffmpeg
   ```
4. **Vérifier l'installation :**
    - Dans le Terminal, tapez `ffmpeg -version` et appuyez sur Entrée
    - Si l'installation est réussie, vous verrez la version de FFmpeg s'afficher

---

## Étape 3 : Vérifier que tout fonctionne

1. Lancez l'application **PadelOverlay** (double-clic sur le fichier `.exe` ou `.app`)
2. L'interface graphique devrait s'ouvrir avec trois boutons de sélection de fichiers
3. Si vous voyez l'interface, félicitations ! L'installation est terminée

---

## Problèmes courants

### Windows : "FFmpeg n'est pas reconnu"

- Vérifiez que vous avez bien ajouté le chemin vers `ffmpeg\bin` dans la variable PATH
- Redémarrez votre ordinateur après avoir modifié les variables d'environnement

### macOS : "L'application ne peut pas être ouverte"

- Faites un clic droit sur l'application et choisissez "Ouvrir" au lieu de double-cliquer
- Allez dans Préférences Système > Sécurité et cliquez sur "Ouvrir quand même"

### L'application ne démarre pas

- Vérifiez que vous avez téléchargé la bonne version (Windows ou macOS)
- Assurez-vous que votre système d'exploitation est à jour

---

## Prochaines étapes

Maintenant que l'application est installée, consultez le **[Guide d'Utilisation](GUIDE_UTILISATION.md)** pour apprendre
à l'utiliser !

---

## Besoin d'aide ?

Si vous rencontrez des problèmes, vous pouvez :

- Consulter les issues
  GitHub : [https://github.com/Pierre-AdrienLefevre/Automatisation_overlay_point/issues](https://github.com/Pierre-AdrienLefevre/Automatisation_overlay_point/issues)
- Créer une nouvelle issue en décrivant votre problème

---

**Bon montage !**
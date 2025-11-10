# Guide d'Utilisation - Padel Video Overlay Generator

## Introduction

Ce guide vous explique comment utiliser l'application **Padel Video Overlay Generator** pour ajouter automatiquement des
scores sur vos vidéos de padel.

L'application transforme vos vidéos découpées point par point en une vidéo finale avec des overlays de score
professionnels.

---

## Vue d'ensemble du processus

Voici les grandes étapes du workflow :

1. **Montage dans Premiere Pro** : Vous éditez votre vidéo de match en découpant chaque point
2. **Export de la timeline** : Vous exportez la structure de votre timeline en format XML
3. **Préparation du fichier de scores** : Vous remplissez un tableau Excel avec les scores de chaque point
4. **Traitement automatique** : L'application génère la vidéo finale avec les overlays

Temps estimé : **5-10 minutes de préparation + temps de traitement automatique**

---

## Étape 1 : Préparer votre projet Premiere Pro

### 1.1 Montage de la vidéo

1. Importez vos rushes vidéo dans Premiere Pro
2. **Découpez votre timeline point par point** :
    - Chaque clip de la timeline doit correspondre à UN point du match
    - Exemple : Si le match a duré 45 points, vous devez avoir 45 clips sur votre timeline
    - Ordre : Du premier au dernier point (chronologique)

**Exemple de timeline :**

```
Clip 1 : Point 1 (0:00-0:15)
Clip 2 : Point 2 (0:15-0:28)
Clip 3 : Point 3 (0:28-0:45)
...
```

### 1.2 Export de la timeline en XML

1. Dans Premiere Pro, allez dans **Fichier > Exporter > Final Cut Pro XML**
2. Donnez un nom à votre fichier (par exemple `match_padel.xml`)
3. Enregistrez-le dans un dossier accessible (par exemple `Documents/PadelOverlay`)

**Ce fichier contient :**

- La structure de votre timeline (ordre des clips)
- Les timecodes de début et fin de chaque clip
- Les références vers vos fichiers vidéo sources

---

## Étape 2 : Préparer le fichier de scores (Excel)

### 2.1 Structure du fichier Excel

Vous devez créer un fichier Excel (`.xlsx`) avec les colonnes suivantes :

| Set | Num_Point | Set1 | Set2 | Jeux | Points | Commentaires |
|-----|-----------|------|------|------|--------|--------------|
| 1   | 1         | 0    | 0    | 0/0  | 0/0    | Service John |
| 1   | 2         | 0    | 0    | 0/0  | 15/0   |              |
| 1   | 3         | 0    | 0    | 0/0  | 15/15  |              |
| 1   | 4         | 0    | 0    | 0/0  | 30/15  |              |
| 1   | 5         | 0    | 0    | 1/0  | 0/0    | Break point  |

### 2.2 Explication des colonnes

- **Set** : Numéro du set en cours (1, 2 ou 3)
- **Num_Point** : Numéro du point dans le set (1, 2, 3...)
- **Set1** : Nombre de sets gagnés par l'équipe 1
- **Set2** : Nombre de sets gagnés par l'équipe 2
- **Jeux** : Score en jeux (format "X/Y", par exemple "3/2")
- **Points** : Score en points (format "X/Y", par exemple "15/30", "40/0", "A/40")
- **Commentaires** : Optionnel, pour vos notes personnelles

### 2.3 Règles importantes

- **Le nombre de lignes doit correspondre au nombre de clips** dans votre timeline Premiere Pro
- **Format des scores** : Toujours "Equipe1/Equipe2" avec un slash (/)
- **Points au tennis** : Utilisez 0, 15, 30, 40, A (pour avantage), ou "égalité"
- **Ordre chronologique** : La ligne 1 = Point 1 de la timeline, etc.

### 2.4 Télécharger un modèle

Un fichier d'exemple est disponible dans le dossier `data/match_points.xlsx` du projet. Vous pouvez le copier et
l'adapter à votre match.

---

## Étape 3 : Utiliser l'application

### 3.1 Lancer l'application

1. Double-cliquez sur **PadelOverlay.exe** (Windows) ou **PadelOverlay.app** (macOS)
2. L'interface graphique s'ouvre avec trois sections principales

### 3.2 Sélectionner les fichiers

#### Fichier XML de Premiere Pro

1. Cliquez sur **"Parcourir..."** à côté de "Fichier XML"
2. Sélectionnez le fichier `.xml` que vous avez exporté depuis Premiere Pro

#### Fichier Excel des scores

1. Cliquez sur **"Parcourir..."** à côté de "Fichier Excel"
2. Sélectionnez votre fichier `.xlsx` contenant les scores

#### Dossier des vidéos sources

1. Cliquez sur **"Parcourir..."** à côté de "Dossier vidéos"
2. Sélectionnez le dossier qui contient vos fichiers vidéo sources (ceux référencés dans Premiere Pro)
    - **Important** : Ce doit être le dossier parent où se trouvent vos rushes

### 3.3 Lancer le traitement

1. Vérifiez que tous les champs sont remplis (les trois fichiers/dossiers sont sélectionnés)
2. Cliquez sur **"Lancer le traitement"**
3. L'application va :
    - Vérifier que le nombre de clips correspond au nombre de lignes Excel
    - Créer les overlays de score pour chaque point
    - Traiter les vidéos et incruster les overlays
    - Assembler le tout en une vidéo finale

### 3.4 Suivi de la progression

Pendant le traitement, vous verrez :

- **Une barre de progression** qui se remplit
- **Des messages de statut** indiquant l'étape en cours
- **Le pourcentage d'avancement**

**Temps de traitement :** Cela dépend de :

- La longueur de votre vidéo (nombre de points)
- La résolution (HD, 4K)
- La puissance de votre ordinateur (GPU recommandé)
- Exemple : Un match de 40 points en Full HD peut prendre 10-30 minutes

---

## Étape 4 : Récupérer la vidéo finale

### 4.1 Localisation de la vidéo

Une fois le traitement terminé, la vidéo finale se trouve dans :

- **Dossier de sortie** : `output/` (créé à côté de l'application)
- **Nom du fichier** : `final_output.mp4`

### 4.2 Fichiers intermédiaires

L'application crée également des fichiers temporaires :

- **Dossier `overlays/`** : Contient les images PNG des scores (une par point)
- **Dossier `segments/`** : Contient les segments vidéo individuels avec overlays

Vous pouvez supprimer ces dossiers après traitement si vous n'en avez plus besoin.

---

## Caractéristiques des overlays

### Design

- **Position** : Bas-gauche de la vidéo (style professionnel)
- **Style** : Arrière-plan semi-transparent avec ombres portées
- **Lisibilité** : Police Arial Bold, contrastes optimisés

### Informations affichées

- Nombre de sets gagnés par chaque équipe
- Score en jeux (par exemple "3 - 2")
- Score en points (par exemple "15 - 30")

### Exemple visuel

```
┌──────────────────────┐
│  SET: 1 - 0          │
│  JEUX: 3 - 2         │
│  POINTS: 15 - 30     │
└──────────────────────┘
```

---

## Résolution de problèmes

### Erreur : "Le nombre de clips ne correspond pas"

- Vérifiez que votre fichier Excel a autant de lignes que de clips dans votre timeline
- Comptez bien tous les clips de la timeline (pas les transitions ou titres)

### Erreur : "Fichier vidéo introuvable"

- Vérifiez que le dossier vidéos sélectionné contient bien tous les rushes
- Les noms de fichiers doivent correspondre exactement à ceux utilisés dans Premiere Pro
- Attention à la casse (majuscules/minuscules) sur macOS/Linux

### Les overlays ne s'affichent pas

- Vérifiez le format des scores dans Excel (doit être "X/Y" avec un slash)
- Assurez-vous qu'il n'y a pas de cellules vides dans les colonnes Jeux et Points

### Le traitement est très lent

- Vérifiez que FFmpeg utilise bien votre GPU (message au démarrage)
- Fermez les autres applications gourmandes en ressources
- Pour les vidéos 4K, le traitement peut prendre plusieurs heures

### La vidéo finale a des problèmes de synchronisation

- Vérifiez que votre timeline Premiere Pro n'a pas de trous (gaps)
- Tous les clips doivent se suivre directement (pas d'espace entre eux)

---

## Conseils et bonnes pratiques

### Avant le tournage

- Filmez en continue (ne coupez pas entre les points)
- Utilisez un trépied pour plus de stabilité
- Assurez-vous d'avoir un bon éclairage

### Pendant le montage

- Découpez précisément au début et à la fin de chaque point
- Évitez les transitions complexes entre clips (coupe franche recommandée)
- Gardez une copie de votre projet Premiere avant export XML

### Préparation du fichier Excel

- Remplissez les scores en regardant la vidéo
- Vérifiez deux fois les scores (surtout en fin de set)
- Utilisez les commentaires pour noter les points importants

### Optimisation du traitement

- Si possible, utilisez un ordinateur avec GPU NVIDIA (plus rapide)
- Traitez vos vidéos en résolution 1080p si vous n'avez pas besoin de 4K
- Lancez le traitement pendant une pause (café, repas)

---

## Exemple de workflow complet

Voici un exemple concret pour un match :

1. **Tournage** : Vous filmez un match de padel (45 minutes, 38 points)
2. **Import** : Vous importez les rushes dans Premiere Pro
3. **Montage** : Vous découpez la timeline en 38 clips (un par point)
4. **Export XML** : Vous exportez "match_samedi.xml"
5. **Excel** : Vous créez "scores_match.xlsx" avec 38 lignes
6. **Application** :
    - XML : "match_samedi.xml"
    - Excel : "scores_match.xlsx"
    - Dossier : "D:/Videos/Padel/Rushes"
7. **Traitement** : 15 minutes de calcul
8. **Résultat** : "output/final_output.mp4" (vidéo de 12 minutes avec overlays)
9. **Publication** : Vous uploadez sur YouTube ou partagez avec les joueurs

---

## Mises à jour de l'application

L'application vérifie automatiquement les mises à jour au démarrage. Si une nouvelle version est disponible :

1. Un message s'affichera avec le numéro de version
2. Téléchargez la nouvelle version depuis GitHub Releases
3. Remplacez l'ancien exécutable par le nouveau

---

## Support et communauté

### Signaler un bug

Si vous rencontrez un problème :

1. Allez sur [GitHub Issues](https://github.com/Pierre-AdrienLefevre/Automatisation_overlay_point/issues)
2. Cliquez sur "New Issue"
3. Décrivez le problème avec le plus de détails possible :
    - Votre système d'exploitation et version
    - Les étapes pour reproduire le problème
    - Les messages d'erreur affichés
    - Captures d'écran si pertinent

### Demander une fonctionnalité

Vous avez une idée d'amélioration ? Créez une issue GitHub avec le tag "enhancement".

---

## FAQ (Foire Aux Questions)

**Q : Puis-je utiliser un autre logiciel de montage que Premiere Pro ?**
R : Pour l'instant, seul l'export XML de Premiere Pro est supporté. D'autres logiciels pourront être ajoutés dans le
futur.

**Q : Puis-je personnaliser le design des overlays ?**
R : Pas directement dans l'interface, mais vous pouvez modifier le code source si vous êtes développeur (voir
`utils/overlay_generator.py`).

**Q : Quelle est la résolution maximale supportée ?**
R : L'application supporte jusqu'à la 4K (3840x2160). Au-delà, les performances peuvent être dégradées.

**Q : Puis-je traiter plusieurs matchs en parallèle ?**
R : Non, lancez un traitement à la fois pour éviter les problèmes de ressources.

**Q : L'application fonctionne-t-elle hors ligne ?**
R : Oui, une fois installée (et FFmpeg), aucune connexion Internet n'est nécessaire (sauf pour les mises à jour).

**Q : Puis-je utiliser l'application pour d'autres sports ?**
R : Le système de score est conçu pour le padel/tennis. Pour d'autres sports, il faudrait modifier le code source.

---

**Bon montage et n'hésitez pas à partager vos créations !**
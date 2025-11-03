# 🔄 Workflow Git & Release Automatique

Ce document explique comment fonctionne le workflow de développement et de release automatique pour ce projet.

## 📋 Structure des branches

### `main` (branche principale)

- Code **stable** et **testé**
- Protégée : nécessite une PR + tests passés pour merger
- Chaque merge vers `main` → **Release automatique**

### `develop` (branche de développement)

- Code en cours de développement
- Tests s'exécutent automatiquement
- Point de départ pour créer des branches de feature

### `feature/*` (branches de fonctionnalités)

- Branches temporaires pour développer des nouvelles fonctionnalités
- Créées depuis `develop`
- Mergées vers `develop` une fois terminées

## 🚀 Processus de développement

### 1. Créer la branche `develop` (première fois uniquement)

```bash
# Créer develop depuis main
git checkout main
git pull
git checkout -b develop
git push -u origin develop
```

### 2. Travailler sur une nouvelle fonctionnalité

```bash
# Partir de develop
git checkout develop
git pull

# Créer une branche feature
git checkout -b feature/ma-nouvelle-fonctionnalite

# Développer, commiter
git add .
git commit -m "feat: ajouter ma nouvelle fonctionnalité"

# Pousser la branche
git push -u origin feature/ma-nouvelle-fonctionnalite
```

### 3. Créer une Pull Request vers `develop`

1. Aller sur GitHub
2. Créer une PR : `feature/ma-nouvelle-fonctionnalite` → `develop`
3. Les tests s'exécutent automatiquement
4. Merger la PR une fois les tests passés

### 4. Release vers production

Quand `develop` est stable et prêt pour une release :

```bash
# Créer une PR : develop → main
git checkout develop
git pull
```

1. Aller sur GitHub
2. Créer une PR : `develop` → `main`
3. Les tests s'exécutent automatiquement
4. Merger la PR

**🎉 La release se fait automatiquement !**

## 🤖 Versioning automatique (Conventional Commits)

La version est calculée automatiquement selon vos messages de commit :

### Format des commits

```bash
<type>(<scope>): <description>

[optional body]
[optional footer]
```

### Types de commits et leur impact sur la version

| Type de commit                 | Impact version            | Exemple                          |
|--------------------------------|---------------------------|----------------------------------|
| `feat:`                        | **MINOR** (0.8.0 → 0.9.0) | `feat: ajout mode nuit`          |
| `feat!:` ou `BREAKING CHANGE:` | **MAJOR** (0.8.0 → 1.0.0) | `feat!: nouvelle API`            |
| `fix:`                         | **PATCH** (0.8.0 → 0.8.1) | `fix: correction bug overlay`    |
| `docs:`                        | **PATCH** (0.8.0 → 0.8.1) | `docs: mise à jour README`       |
| `test:`                        | **PATCH** (0.8.0 → 0.8.1) | `test: ajout tests unitaires`    |
| `chore:`                       | **PATCH** (0.8.0 → 0.8.1) | `chore: mise à jour dépendances` |
| `refactor:`                    | **PATCH** (0.8.0 → 0.8.1) | `refactor: nettoyage code`       |
| Autre                          | **PATCH** (0.8.0 → 0.8.1) | Tout autre message               |

### Exemples de bons messages de commit

```bash
# Nouvelle fonctionnalité (MINOR)
git commit -m "feat: ajout support vidéos 8K"
git commit -m "feat(overlay): ajout animations de transition"

# Correction de bug (PATCH)
git commit -m "fix: résolution crash au démarrage"
git commit -m "fix(parser): correction lecture XML invalide"

# Breaking change (MAJOR)
git commit -m "feat!: refonte complète de l'API"
git commit -m "feat: nouvelle API

BREAKING CHANGE: l'ancienne API n'est plus supportée"

# Documentation (PATCH)
git commit -m "docs: ajout guide d'installation"

# Tests (PATCH)
git commit -m "test: ajout tests pour overlay_generator"

# Maintenance (PATCH)
git commit -m "chore: mise à jour PyQt6 vers 6.10.0"
```

## 📦 Que se passe-t-il lors d'une release automatique ?

Quand vous mergez une PR vers `main` :

1. **Analyse des commits** : Le workflow analyse tous vos commits depuis la dernière release
2. **Calcul de version** : Détermine automatiquement la nouvelle version (ex: 0.8.0 → 0.9.0)
3. **Création du tag** : Crée automatiquement le tag Git (ex: `v0.9.0`)
4. **Build des exécutables** :
    - Windows : `PadelOverlayGenerator-Windows.exe`
    - macOS : `PadelOverlayGenerator-macOS`
5. **Création de la release GitHub** avec :
    - Changelog automatique (liste des commits)
    - Fichiers exécutables téléchargeables
    - Checksums SHA256

## 🔧 Configuration GitHub Copilot

Avec GitHub Copilot activé, vous bénéficiez de :

- ✅ **Suggestions de commit messages** selon conventional commits
- ✅ **Auto-completion** des types de commits
- ✅ **Revue de code automatique** dans les PR
- ✅ **Suggestions de code** pendant le développement

## 📝 Checklist avant une release

Avant de merger `develop` → `main` :

- [ ] Tous les tests passent
- [ ] La documentation est à jour
- [ ] Le CHANGELOG est mis à jour (si manuel)
- [ ] Les messages de commit suivent conventional commits
- [ ] Aucun TODO ou FIXME critique dans le code
- [ ] L'application a été testée manuellement

## 🎯 Résumé visuel

```
feature/xxx ──┐
              ├──> develop ──┐
feature/yyy ──┘              │
                             ├──> main ──> 🚀 RELEASE AUTOMATIQUE
feature/zzz ───────────────> │            (tag + binaires + changelog)
```

## ❓ FAQ

### Puis-je encore créer des releases manuellement ?

Oui ! Vous pouvez toujours créer un tag manuellement :

```bash
git tag -a v0.9.0 -m "Release 0.9.0"
git push origin v0.9.0
```

Ou via l'interface GitHub (Actions → Release Automatique → Run workflow).

### Que faire si la version calculée est incorrecte ?

Si la version automatique ne convient pas, vous pouvez :

1. Créer un tag manuel avec la version souhaitée
2. Ou ajuster vos messages de commit pour la prochaine fois

### Puis-je désactiver les releases automatiques ?

Oui, supprimez simplement les lignes 4-6 dans `.github/workflows/release.yml` :

```yaml
on:
  pull_request: # ← Supprimer ces 3 lignes
    types: [ closed ]  # ← pour désactiver
    branches: [ main ] # ← les releases auto
```
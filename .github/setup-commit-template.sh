#!/bin/bash

# Script pour configurer le template de commit pour le projet

echo "🚀 Configuration du template de commit pour Analyses_depenses..."

# Configurer le template de commit localement pour ce projet
git config commit.template .gitmessage

echo "✅ Template de commit configuré !"
echo ""
echo "📝 Utilisation :"
echo "   À partir de maintenant, quand vous faites 'git commit' (sans -m),"
echo "   votre éditeur s'ouvrira avec le template pré-rempli."
echo ""
echo "💡 Rappel des types de commits :"
echo "   - feat:     Nouvelle fonctionnalité (version MINOR)"
echo "   - fix:      Correction de bug (version PATCH)"
echo "   - feat!:    Breaking change (version MAJOR)"
echo "   - docs:     Documentation"
echo "   - test:     Tests"
echo "   - refactor: Refactorisation"
echo "   - chore:    Maintenance"
echo ""
echo "📖 Pour plus d'informations, consultez .github/RELEASES.md"
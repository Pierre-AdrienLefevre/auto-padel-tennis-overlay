#!/usr/bin/env python3
"""
Module de génération d'overlays de score pour vidéos de padel/tennis.
Style basé sur l'exemple Overlay_précis2.png
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path


class PadelOverlayGenerator:
    """Génère des overlays de score style padel avec design professionnel."""

    def __init__(self, width=1920, height=1080):
        """
        Initialise le générateur d'overlay.

        Args:
            width: Largeur de l'image overlay (résolution vidéo)
            height: Hauteur de l'image overlay (résolution vidéo)
        """
        self.width = width
        self.height = height

        # Couleurs (basées sur l'exemple)
        self.color_bg_teams = (30, 58, 87, 255)      # Bleu marine foncé
        self.color_bg_games = (200, 200, 200, 255)   # Gris clair
        self.color_text_white = (255, 255, 255, 255) # Blanc
        self.color_text_black = (0, 0, 0, 255)       # Noir
        self.color_separator = (255, 255, 255, 200)  # Blanc semi-transparent

        # Dimensions du scoreboard
        self.margin = 40
        self.names_width = 570
        self.games_width = 200
        self.points_width = 200
        self.row_height = 75
        self.border_radius = 20
        self.spacing = 15  # Espacement entre les sections

    def load_fonts(self):
        """Charge les polices système."""
        try:
            # Police pour les noms d'équipes (Helvetica Bold)
            font_team = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 45)
            # Police pour les jeux (gros chiffres noirs)
            font_games = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 90)
            # Police pour les points (gros chiffres blancs)
            font_points = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 85)

            return font_team, font_games, font_points
        except Exception:
            # Fallback sur police par défaut
            default = ImageFont.load_default()
            return default, default, default

    def parse_score(self, jeux_str, points_str):
        """
        Parse les scores depuis le format Excel.

        Args:
            jeux_str: String format "3/3" (jeux équipe1/équipe2)
            points_str: String format "40/30" (points équipe1/équipe2)

        Returns:
            Tuple (jeux_eq1, jeux_eq2, points_eq1, points_eq2)
        """
        # Parser les jeux
        if isinstance(jeux_str, str) and '/' in jeux_str:
            jeux_parts = jeux_str.split('/')
            jeux_eq1 = jeux_parts[0].strip()
            jeux_eq2 = jeux_parts[1].strip() if len(jeux_parts) > 1 else "0"
        else:
            jeux_eq1, jeux_eq2 = "0", "0"

        # Parser les points
        if isinstance(points_str, str) and '/' in points_str:
            points_parts = points_str.split('/')
            points_eq1 = points_parts[0].strip()
            points_eq2 = points_parts[1].strip() if len(points_parts) > 1 else "0"
        else:
            points_eq1, points_eq2 = "0", "0"

        return jeux_eq1, jeux_eq2, points_eq1, points_eq2

    def create_overlay(self,
                      team1_names="LÉO / YANNOUCK",
                      team2_names="BILAL / PIERRE",
                      jeux="3/3",
                      points="40/30"):
        """
        Crée l'overlay complet avec le score.

        Args:
            team1_names: Noms de l'équipe 1 (format: "NOM1 / NOM2")
            team2_names: Noms de l'équipe 2
            jeux: Score de jeux (format: "eq1/eq2")
            points: Score de points (format: "eq1/eq2")

        Returns:
            Image PIL avec l'overlay
        """
        # Créer image transparente
        img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Charger les polices
        font_team, font_games, font_points = self.load_fonts()

        # Parser les scores
        jeux_eq1, jeux_eq2, points_eq1, points_eq2 = self.parse_score(jeux, points)

        # Calculer la hauteur totale
        total_height = self.row_height * 2 + 30

        # Position en bas à gauche
        x_start = self.margin
        y_start = self.height - total_height - self.margin

        # === SECTION 1: NOMS DES ÉQUIPES (fond bleu marine) ===
        x_names = x_start
        draw.rounded_rectangle(
            [(x_names, y_start),
             (x_names + self.names_width, y_start + total_height)],
            radius=self.border_radius,
            fill=self.color_bg_teams
        )

        # === SECTION 2: JEUX (fond gris clair) ===
        x_games = x_names + self.names_width + self.spacing
        draw.rounded_rectangle(
            [(x_games, y_start),
             (x_games + self.games_width, y_start + total_height)],
            radius=self.border_radius,
            fill=self.color_bg_games
        )

        # === SECTION 3: POINTS (fond bleu marine) ===
        x_points = x_games + self.games_width + self.spacing
        draw.rounded_rectangle(
            [(x_points, y_start),
             (x_points + self.points_width, y_start + total_height)],
            radius=self.border_radius,
            fill=self.color_bg_teams
        )

        # === LIGNES DE SÉPARATION HORIZONTALES ===
        sep_y = y_start + self.row_height + 15

        # Séparation dans la section noms
        draw.line(
            [(x_names + 30, sep_y), (x_names + self.names_width - 30, sep_y)],
            fill=self.color_separator,
            width=3
        )

        # Séparation dans la section jeux
        draw.line(
            [(x_games + 40, sep_y), (x_games + self.games_width - 40, sep_y)],
            fill=self.color_text_black,
            width=3
        )

        # Séparation dans la section points
        draw.line(
            [(x_points + 40, sep_y), (x_points + self.points_width - 40, sep_y)],
            fill=self.color_separator,
            width=3
        )

        # === TEXTES ===
        # Positions Y pour chaque ligne
        y1_offset = 18  # Équipe 1
        y2_offset = self.row_height + 23  # Équipe 2

        # ÉQUIPE 1 (ligne du haut)
        # Noms
        draw.text(
            (x_names + 30, y_start + y1_offset),
            team1_names.upper(),
            fill=self.color_text_white,
            font=font_team
        )
        # Jeux
        jeux1_bbox = draw.textbbox((0, 0), jeux_eq1, font=font_games)
        jeux1_width = jeux1_bbox[2] - jeux1_bbox[0]
        draw.text(
            (x_games + (self.games_width - jeux1_width) // 2, y_start + y1_offset - 10),
            jeux_eq1,
            fill=self.color_text_black,
            font=font_games
        )
        # Points
        points1_bbox = draw.textbbox((0, 0), points_eq1, font=font_points)
        points1_width = points1_bbox[2] - points1_bbox[0]
        draw.text(
            (x_points + (self.points_width - points1_width) // 2, y_start + y1_offset - 5),
            points_eq1,
            fill=self.color_text_white,
            font=font_points
        )

        # ÉQUIPE 2 (ligne du bas)
        # Noms
        draw.text(
            (x_names + 30, y_start + y2_offset),
            team2_names.upper(),
            fill=self.color_text_white,
            font=font_team
        )
        # Jeux
        jeux2_bbox = draw.textbbox((0, 0), jeux_eq2, font=font_games)
        jeux2_width = jeux2_bbox[2] - jeux2_bbox[0]
        draw.text(
            (x_games + (self.games_width - jeux2_width) // 2, y_start + y2_offset - 10),
            jeux_eq2,
            fill=self.color_text_black,
            font=font_games
        )
        # Points
        points2_bbox = draw.textbbox((0, 0), points_eq2, font=font_points)
        points2_width = points2_bbox[2] - points2_bbox[0]
        draw.text(
            (x_points + (self.points_width - points2_width) // 2, y_start + y2_offset - 5),
            points_eq2,
            fill=self.color_text_white,
            font=font_points
        )

        return img

    def save_overlay(self, img, output_path):
        """Sauvegarde l'overlay en PNG."""
        img.save(output_path, 'PNG')
        return output_path


# Fonction utilitaire pour usage simple
def generate_padel_overlay(jeux, points,
                           team1="LÉO / YANNOUCK",
                           team2="BILAL / PIERRE",
                           output_path="overlay.png",
                           width=1920, height=1080):
    """
    Fonction utilitaire pour générer rapidement un overlay.

    Args:
        jeux: Score de jeux (format: "3/3")
        points: Score de points (format: "40/30")
        team1: Noms équipe 1
        team2: Noms équipe 2
        output_path: Chemin de sortie
        width: Largeur de l'image
        height: Hauteur de l'image

    Returns:
        Chemin du fichier créé
    """
    generator = PadelOverlayGenerator(width, height)
    overlay_img = generator.create_overlay(
        team1_names=team1,
        team2_names=team2,
        jeux=jeux,
        points=points
    )
    return generator.save_overlay(overlay_img, output_path)


# Test si exécuté directement
if __name__ == "__main__":
    # Exemple de test
    print("🎾 Test du générateur d'overlay Padel")

    generator = PadelOverlayGenerator()

    # Créer un exemple
    overlay = generator.create_overlay(
        team1_names="LÉO / YANNOUCK",
        team2_names="BILAL / PIERRE",
        jeux="3/3",
        points="40/30"
    )

    # Sauvegarder
    output = "test_overlay.png"
    generator.save_overlay(overlay, output)
    print(f"✅ Overlay de test créé: {output}")
#!/usr/bin/env python3
"""
Module de génération d'overlays de score pour vidéos de padel/tennis.
Style basé sur l'exemple Overlay_précis2.png
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path


class PadelOverlayGenerator:
    """Génère des overlays de score style padel avec design professionnel."""

    def __init__(self, width=3840, height=2160):
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

        # Dimensions du scoreboard (pour 4K, x2 des valeurs 1080p)
        self.x_offset = 200  # Distance du bord gauche
        self.y_offset_from_bottom = 10  # Distance du bord du bas (bord bas de l'overlay)
        self.total_width = 2400  # Largeur totale de l'overlay
        self.total_height = 500  # Hauteur totale

        # Hauteur de chaque ligne
        self.row_height = 250

        # Largeurs des colonnes (x2 pour 4K)
        self.names_width = 560
        self.games_width = 200
        self.points_width = 200
        self.set_width = 160  # Largeur pour les colonnes de sets

        self.border_radius = 30
        self.spacing = 16  # Espacement entre les sections

    def load_fonts(self):
        """Charge les polices système."""
        try:
            # Police pour les noms d'équipes (x2 pour 4K)
            font_team = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 44)
            # Police pour les jeux (chiffres noirs, x2 pour 4K)
            font_games = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 90)
            # Police pour les points (chiffres blancs, x2 pour 4K)
            font_points = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 84)

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
                      points="40/30",
                      set1=None,
                      set2=None):
        """
        Crée l'overlay complet avec le score.

        Args:
            team1_names: Noms de l'équipe 1 (format: "NOM1 / NOM2")
            team2_names: Noms de l'équipe 2
            jeux: Score de jeux (format: "eq1/eq2")
            points: Score de points (format: "eq1/eq2")
            set1: Score du 1er set terminé (format: "eq1/eq2", ex: "5/7")
            set2: Score du 2ème set terminé (format: "eq1/eq2", ex: "1/0")

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

        # Calculer la hauteur totale avec les nouvelles dimensions
        total_height = self.total_height

        # Position selon les spécifications (96px du bord gauche, 241px du bas)
        x_start = self.x_offset
        y_start = self.height - self.y_offset_from_bottom - total_height

        # === SECTION 1: NOMS DES ÉQUIPES (fond bleu marine) ===
        x_names = x_start
        draw.rounded_rectangle(
            [(x_names, y_start),
             (x_names + self.names_width, y_start + total_height)],
            radius=self.border_radius,
            fill=self.color_bg_teams
        )

        # Position courante pour les sections suivantes
        x_current = x_names + self.names_width + self.spacing

        # === SETS TERMINÉS (si présents, insérés avant les jeux) ===
        x_set1 = None
        x_set2 = None

        if set1:
            x_set1 = x_current
            draw.rounded_rectangle(
                [(x_set1, y_start),
                 (x_set1 + self.set_width, y_start + total_height)],
                radius=self.border_radius,
                fill=self.color_bg_teams
            )
            x_current = x_set1 + self.set_width + self.spacing

        if set2:
            x_set2 = x_current
            draw.rounded_rectangle(
                [(x_set2, y_start),
                 (x_set2 + self.set_width, y_start + total_height)],
                radius=self.border_radius,
                fill=self.color_bg_teams
            )
            x_current = x_set2 + self.set_width + self.spacing

        # === JEUX DU SET EN COURS (fond gris clair) ===
        x_games = x_current
        draw.rounded_rectangle(
            [(x_games, y_start),
             (x_games + self.games_width, y_start + total_height)],
            radius=self.border_radius,
            fill=self.color_bg_games
        )

        # === POINTS (fond bleu marine) ===
        x_points = x_games + self.games_width + self.spacing
        draw.rounded_rectangle(
            [(x_points, y_start),
             (x_points + self.points_width, y_start + total_height)],
            radius=self.border_radius,
            fill=self.color_bg_teams
        )

        # === LIGNES DE SÉPARATION HORIZONTALES ===
        sep_y = y_start + self.row_height + 7

        # Séparation dans la section noms
        draw.line(
            [(x_names + 15, sep_y), (x_names + self.names_width - 15, sep_y)],
            fill=self.color_separator,
            width=2
        )

        # Séparation dans la section jeux
        draw.line(
            [(x_games + 20, sep_y), (x_games + self.games_width - 20, sep_y)],
            fill=self.color_text_black,
            width=2
        )

        # Séparation dans la section points
        draw.line(
            [(x_points + 20, sep_y), (x_points + self.points_width - 20, sep_y)],
            fill=self.color_separator,
            width=2
        )

        # Séparations dans les sets
        if x_set1:
            draw.line(
                [(x_set1 + 15, sep_y), (x_set1 + self.set_width - 15, sep_y)],
                fill=self.color_separator,
                width=2
            )
        if x_set2:
            draw.line(
                [(x_set2 + 15, sep_y), (x_set2 + self.set_width - 15, sep_y)],
                fill=self.color_separator,
                width=2
            )

        # === TEXTES ===
        # Positions Y pour chaque ligne (ajustées pour les nouvelles dimensions)
        y1_offset = 10  # Équipe 1
        y2_offset = self.row_height + 12  # Équipe 2

        # ÉQUIPE 1 (ligne du haut)
        # Noms
        draw.text(
            (x_names + 15, y_start + y1_offset),
            team1_names.upper(),
            fill=self.color_text_white,
            font=font_team
        )
        # Jeux
        jeux1_bbox = draw.textbbox((0, 0), jeux_eq1, font=font_games)
        jeux1_width = jeux1_bbox[2] - jeux1_bbox[0]
        draw.text(
            (x_games + (self.games_width - jeux1_width) // 2, y_start + y1_offset - 5),
            jeux_eq1,
            fill=self.color_text_black,
            font=font_games
        )
        # Points
        points1_bbox = draw.textbbox((0, 0), points_eq1, font=font_points)
        points1_width = points1_bbox[2] - points1_bbox[0]
        draw.text(
            (x_points + (self.points_width - points1_width) // 2, y_start + y1_offset - 3),
            points_eq1,
            fill=self.color_text_white,
            font=font_points
        )

        # ÉQUIPE 2 (ligne du bas)
        # Noms
        draw.text(
            (x_names + 15, y_start + y2_offset),
            team2_names.upper(),
            fill=self.color_text_white,
            font=font_team
        )
        # Jeux
        jeux2_bbox = draw.textbbox((0, 0), jeux_eq2, font=font_games)
        jeux2_width = jeux2_bbox[2] - jeux2_bbox[0]
        draw.text(
            (x_games + (self.games_width - jeux2_width) // 2, y_start + y2_offset - 5),
            jeux_eq2,
            fill=self.color_text_black,
            font=font_games
        )
        # Points
        points2_bbox = draw.textbbox((0, 0), points_eq2, font=font_points)
        points2_width = points2_bbox[2] - points2_bbox[0]
        draw.text(
            (x_points + (self.points_width - points2_width) // 2, y_start + y2_offset - 3),
            points_eq2,
            fill=self.color_text_white,
            font=font_points
        )

        # === SETS (si présents) ===
        if set1 and x_set1:
            set1_eq1, set1_eq2 = self.parse_score(set1, "0/0")[0:2]
            # Set 1 équipe 1
            set1_eq1_bbox = draw.textbbox((0, 0), set1_eq1, font=font_points)
            set1_eq1_width = set1_eq1_bbox[2] - set1_eq1_bbox[0]
            draw.text(
                (x_set1 + (self.set_width - set1_eq1_width) // 2, y_start + y1_offset - 5),
                set1_eq1,
                fill=self.color_text_white,
                font=font_points
            )
            # Set 1 équipe 2
            set1_eq2_bbox = draw.textbbox((0, 0), set1_eq2, font=font_points)
            set1_eq2_width = set1_eq2_bbox[2] - set1_eq2_bbox[0]
            draw.text(
                (x_set1 + (self.set_width - set1_eq2_width) // 2, y_start + y2_offset - 5),
                set1_eq2,
                fill=self.color_text_white,
                font=font_points
            )

        if set2 and x_set2:
            set2_eq1, set2_eq2 = self.parse_score(set2, "0/0")[0:2]
            # Set 2 équipe 1
            set2_eq1_bbox = draw.textbbox((0, 0), set2_eq1, font=font_points)
            set2_eq1_width = set2_eq1_bbox[2] - set2_eq1_bbox[0]
            draw.text(
                (x_set2 + (self.set_width - set2_eq1_width) // 2, y_start + y1_offset - 5),
                set2_eq1,
                fill=self.color_text_white,
                font=font_points
            )
            # Set 2 équipe 2
            set2_eq2_bbox = draw.textbbox((0, 0), set2_eq2, font=font_points)
            set2_eq2_width = set2_eq2_bbox[2] - set2_eq2_bbox[0]
            draw.text(
                (x_set2 + (self.set_width - set2_eq2_width) // 2, y_start + y2_offset - 5),
                set2_eq2,
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

    # Test 1: overlay simple
    overlay = generator.create_overlay(
        team1_names="LÉO / YANNOUCK",
        team2_names="BILAL / PIERRE",
        jeux="3/3",
        points="40/30"
    )
    generator.save_overlay(overlay, "test_overlay_simple.png")
    print("✅ Test 1: test_overlay_simple.png")

    # Test 2: overlay avec 2 sets
    overlay2 = generator.create_overlay(
        team1_names="LÉO / YANNOUCK",
        team2_names="PIERRE / BILAL",
        jeux="5/7",
        points="0/15",
        set1="5/7",
        set2="1/0"
    )
    generator.save_overlay(overlay2, "test_overlay_2sets.png")
    print("✅ Test 2: test_overlay_2sets.png")
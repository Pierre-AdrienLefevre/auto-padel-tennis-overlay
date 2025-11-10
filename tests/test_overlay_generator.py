#!/usr/bin/env python3
"""
Tests unitaires pour overlay_generator.py
Tests des fonctions pures et de la génération d'overlays.
"""

import pytest

from utils.overlay_generator import PadelOverlayGenerator


class TestPadelOverlayGenerator:
    """Tests pour la classe PadelOverlayGenerator."""

    @pytest.fixture
    def generator(self):
        """Fixture pour créer un générateur d'overlay."""
        return PadelOverlayGenerator(width=1920, height=1080)

    def test_parse_score_valid_format(self, generator):
        """Test du parsing avec format valide."""
        jeux_eq1, jeux_eq2, points_eq1, points_eq2 = generator.parse_score("3/2", "40/30")

        assert jeux_eq1 == "3"
        assert jeux_eq2 == "2"
        assert points_eq1 == "40"
        assert points_eq2 == "30"

    def test_parse_score_advantage(self, generator):
        """Test du parsing avec avantage."""
        jeux_eq1, jeux_eq2, points_eq1, points_eq2 = generator.parse_score("5/4", "A/40")

        assert jeux_eq1 == "5"
        assert jeux_eq2 == "4"
        assert points_eq1 == "A"
        assert points_eq2 == "40"

    def test_parse_score_zeros(self, generator):
        """Test du parsing avec scores à zéro."""
        jeux_eq1, jeux_eq2, points_eq1, points_eq2 = generator.parse_score("0/0", "0/0")

        assert jeux_eq1 == "0"
        assert jeux_eq2 == "0"
        assert points_eq1 == "0"
        assert points_eq2 == "0"

    def test_parse_score_missing_slash(self, generator):
        """Test du parsing avec format invalide (sans slash)."""
        jeux_eq1, jeux_eq2, points_eq1, points_eq2 = generator.parse_score("33", "4030")

        assert jeux_eq1 == "0"
        assert jeux_eq2 == "0"
        assert points_eq1 == "0"
        assert points_eq2 == "0"

    def test_parse_score_empty_string(self, generator):
        """Test du parsing avec chaîne vide."""
        jeux_eq1, jeux_eq2, points_eq1, points_eq2 = generator.parse_score("", "")

        assert jeux_eq1 == "0"
        assert jeux_eq2 == "0"
        assert points_eq1 == "0"
        assert points_eq2 == "0"

    def test_parse_score_none_values(self, generator):
        """Test du parsing avec valeurs None."""
        jeux_eq1, jeux_eq2, points_eq1, points_eq2 = generator.parse_score(None, None)

        assert jeux_eq1 == "0"
        assert jeux_eq2 == "0"
        assert points_eq1 == "0"
        assert points_eq2 == "0"

    def test_parse_score_spaces(self, generator):
        """Test du parsing avec espaces."""
        jeux_eq1, jeux_eq2, points_eq1, points_eq2 = generator.parse_score(" 3 / 2 ", " 40 / 30 ")

        assert jeux_eq1 == "3"
        assert jeux_eq2 == "2"
        assert points_eq1 == "40"
        assert points_eq2 == "30"

    def test_parse_score_tiebreak(self, generator):
        """Test du parsing avec tie-break."""
        jeux_eq1, jeux_eq2, points_eq1, points_eq2 = generator.parse_score("6/6", "7/5")

        assert jeux_eq1 == "6"
        assert jeux_eq2 == "6"
        assert points_eq1 == "7"
        assert points_eq2 == "5"

    def test_load_fonts_returns_three_fonts(self, generator):
        """Test que load_fonts retourne bien 3 polices."""
        font_team, font_games, font_points = generator.load_fonts()

        assert font_team is not None
        assert font_games is not None
        assert font_points is not None

    def test_create_overlay_basic(self, generator):
        """Test de création d'overlay basique."""
        overlay = generator.create_overlay(
            team1_names="ÉQUIPE A",
            team2_names="ÉQUIPE B",
            jeux="3/2",
            points="40/30"
        )

        assert overlay is not None
        assert overlay.size == (1920, 1080)
        assert overlay.mode == "RGBA"

    def test_create_overlay_with_sets(self, generator):
        """Test de création d'overlay avec sets."""
        overlay = generator.create_overlay(
            team1_names="ÉQUIPE A",
            team2_names="ÉQUIPE B",
            jeux="3/2",
            points="40/30",
            set1="6/4",
            set2="5/7"
        )

        assert overlay is not None
        assert overlay.size == (1920, 1080)
        assert overlay.mode == "RGBA"

    def test_create_overlay_default_values(self, generator):
        """Test de création d'overlay avec valeurs par défaut."""
        overlay = generator.create_overlay()

        assert overlay is not None
        assert overlay.size == (1920, 1080)
        assert overlay.mode == "RGBA"

    def test_generator_initialization_default(self):
        """Test de l'initialisation avec valeurs par défaut."""
        gen = PadelOverlayGenerator()

        assert gen.width == 3840
        assert gen.height == 2160

    def test_generator_initialization_custom(self):
        """Test de l'initialisation avec valeurs personnalisées."""
        gen = PadelOverlayGenerator(width=1280, height=720)

        assert gen.width == 1280
        assert gen.height == 720

    def test_save_overlay(self, generator, tmp_path):
        """Test de sauvegarde d'overlay."""
        overlay = generator.create_overlay()
        output_path = tmp_path / "test_overlay.png"

        result = generator.save_overlay(overlay, str(output_path))

        assert result == str(output_path)
        assert output_path.exists()

    def test_scale_factor_4k(self):
        """Test du facteur d'échelle pour 4K (référence = 1.0)."""
        gen = PadelOverlayGenerator(width=3840, height=2160)
        assert gen.scale_factor == 1.0

    def test_scale_factor_1080p(self):
        """Test du facteur d'échelle pour 1080p (0.5x)."""
        gen = PadelOverlayGenerator(width=1920, height=1080)
        assert gen.scale_factor == 0.5

    def test_scale_factor_720p(self):
        """Test du facteur d'échelle pour 720p (~0.33x)."""
        gen = PadelOverlayGenerator(width=1280, height=720)
        expected_scale = min(1280 / 3840, 720 / 2160)  # ~0.333
        assert abs(gen.scale_factor - expected_scale) < 0.001

    def test_dimensions_scale_with_resolution(self):
        """Test que les dimensions s'adaptent à la résolution."""
        gen_4k = PadelOverlayGenerator(width=3840, height=2160)
        gen_1080p = PadelOverlayGenerator(width=1920, height=1080)

        # Vérifier que les dimensions 1080p sont environ la moitié de la 4K
        assert gen_1080p.names_width == gen_4k.names_width // 2
        assert gen_1080p.games_width == gen_4k.games_width // 2
        assert gen_1080p.total_height == gen_4k.total_height // 2

    def test_overlay_size_matches_resolution(self):
        """Test que les overlays générés ont la bonne taille."""
        # Test 1080p
        gen_1080p = PadelOverlayGenerator(width=1920, height=1080)
        overlay_1080p = gen_1080p.create_overlay()
        assert overlay_1080p.size == (1920, 1080)

        # Test 720p
        gen_720p = PadelOverlayGenerator(width=1280, height=720)
        overlay_720p = gen_720p.create_overlay()
        assert overlay_720p.size == (1280, 720)

#!/usr/bin/env python3
"""
Application PyQt6 pour la génération automatique d'overlays de score sur vidéos de padel.
Interface graphique pour utilisateurs non-techniques.
"""

import sys
from pathlib import Path

import requests
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QFileDialog, QProgressBar,
    QTextEdit, QGroupBox, QMessageBox
)

from main import VideoOverlayAutomator

# Version de l'application
APP_VERSION = "0.8.0"
GITHUB_REPO = "Pierre-AdrienLefevre/auto-padel-tennis-overlay"  # À remplacer par votre repo GitHub


class UpdateChecker(QThread):
    """Thread pour vérifier les mises à jour sur GitHub."""
    update_available = pyqtSignal(str, str)  # nouvelle_version, url_download
    no_update = pyqtSignal()
    error = pyqtSignal(str)

    def run(self):
        try:
            # Vérifier la dernière release sur GitHub
            url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                data = response.json()
                latest_version = data.get('tag_name', '').lstrip('v')
                download_url = data.get('html_url', '')

                # Comparer les versions
                if self.compare_versions(latest_version, APP_VERSION):
                    self.update_available.emit(latest_version, download_url)
                else:
                    self.no_update.emit()
            else:
                self.no_update.emit()
        except Exception as e:
            self.error.emit(str(e))

    def compare_versions(self, v1, v2):
        """Compare deux versions (format: x.y.z)."""
        try:
            v1_parts = [int(x) for x in v1.split('.')]
            v2_parts = [int(x) for x in v2.split('.')]
            return v1_parts > v2_parts
        except:
            return False


class VideoProcessThread(QThread):
    """Thread pour le traitement vidéo (ne bloque pas l'interface)."""
    progress = pyqtSignal(str)  # message de progression
    progress_percent = pyqtSignal(int)  # pourcentage (0-100)
    progress_detail = pyqtSignal(int, int, str)  # current, total, time_remaining
    finished = pyqtSignal(bool, str)  # success, message

    def __init__(self, xml_path, excel_path, video_folder, output_path):
        super().__init__()
        self.xml_path = xml_path
        self.excel_path = excel_path
        self.video_folder = video_folder
        self.output_path = output_path

    def run(self):
        try:
            self.progress.emit("Initialisation...")
            self.progress_percent.emit(5)

            automator = VideoOverlayAutomator(
                self.xml_path,
                self.excel_path,
                self.video_folder
            )

            self.progress.emit("Parsing des fichiers...")
            self.progress_percent.emit(10)
            automator.parse_xml()
            automator.parse_excel()

            # Vérifier la correspondance
            if len(automator.clips) != len(automator.scores):
                min_len = min(len(automator.clips), len(automator.scores))
                automator.clips = automator.clips[:min_len]
                automator.scores = automator.scores[:min_len]

            total_clips = len(automator.clips)
            self.progress.emit(f"Traitement de {total_clips} segments...")
            self.progress_percent.emit(15)

            # Hook into the automator to get progress
            import time
            start_time = time.time()
            segment_times = []

            # On va modifier temporairement la méthode pour capturer la progression
            original_process = automator.process_single_segment
            completed = [0]  # Utilisé comme compteur mutable

            def wrapped_process(*args, **kwargs):
                seg_start = time.time()
                result = original_process(*args, **kwargs)
                seg_time = time.time() - seg_start

                if result:
                    segment_times.append(seg_time)
                    completed[0] += 1

                    # Calculer le temps restant
                    avg_time = sum(segment_times) / len(segment_times)
                    remaining = total_clips - completed[0]
                    est_remaining = avg_time * remaining

                    # Mettre à jour la progression
                    percent = 15 + int((completed[0] / total_clips) * 80)
                    self.progress_percent.emit(percent)

                    # Formater le temps restant
                    mins = int(est_remaining // 60)
                    secs = int(est_remaining % 60)
                    time_str = f"{mins}m{secs:02d}s" if mins > 0 else f"{secs}s"

                    self.progress_detail.emit(completed[0], total_clips, time_str)
                    self.progress.emit(f"Segment {completed[0]}/{total_clips} - Temps restant: ~{time_str}")

                return result

            automator.process_single_segment = wrapped_process
            automator.process_video(self.output_path)

            self.progress_percent.emit(100)
            self.finished.emit(True, f"Vidéo générée avec succès: {self.output_path}")
        except Exception as e:
            self.finished.emit(False, f"Erreur: {str(e)}")


class PadelOverlayApp(QMainWindow):
    """Application principale."""

    def __init__(self):
        super().__init__()
        self.xml_path = ""
        self.excel_path = ""
        self.video_folder = ""
        self.output_path = ""

        self.init_ui()
        self.check_for_updates()

    def init_ui(self):
        """Initialise l'interface utilisateur."""
        self.setWindowTitle(f"Padel Video Overlay Generator v{APP_VERSION}")
        self.setMinimumSize(900, 700)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Titre
        title = QLabel("🎾 Générateur d'Overlays Padel")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Section: Sélection des fichiers
        files_group = QGroupBox("1. Sélection des fichiers")
        files_layout = QVBoxLayout()

        # XML File
        xml_layout = QHBoxLayout()
        xml_layout.addWidget(QLabel("Fichier XML (Premiere Pro):"))
        self.xml_input = QLineEdit()
        self.xml_input.setPlaceholderText("Sélectionnez le fichier XML...")
        xml_layout.addWidget(self.xml_input)
        xml_btn = QPushButton("Parcourir")
        xml_btn.clicked.connect(self.select_xml)
        xml_layout.addWidget(xml_btn)
        files_layout.addLayout(xml_layout)

        # Excel File
        excel_layout = QHBoxLayout()
        excel_layout.addWidget(QLabel("Fichier Excel (Scores):"))
        self.excel_input = QLineEdit()
        self.excel_input.setPlaceholderText("Sélectionnez le fichier Excel...")
        excel_layout.addWidget(self.excel_input)
        excel_btn = QPushButton("Parcourir")
        excel_btn.clicked.connect(self.select_excel)
        excel_layout.addWidget(excel_btn)
        files_layout.addLayout(excel_layout)

        # Video Files
        video_layout = QHBoxLayout()
        video_layout.addWidget(QLabel("Fichiers vidéo:"))
        self.folder_input = QLineEdit()
        self.folder_input.setPlaceholderText("Sélectionnez les fichiers vidéo (MP4, MOV)...")
        video_layout.addWidget(self.folder_input)
        video_btn = QPushButton("Parcourir")
        video_btn.clicked.connect(self.select_videos)
        video_layout.addWidget(video_btn)
        files_layout.addLayout(video_layout)

        # Output File
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("Fichier de sortie:"))
        self.output_input = QLineEdit()
        self.output_input.setPlaceholderText("output_final.mp4")
        self.output_input.setText("output_final.mp4")
        output_layout.addWidget(self.output_input)
        output_btn = QPushButton("Parcourir")
        output_btn.clicked.connect(self.select_output)
        output_layout.addWidget(output_btn)
        files_layout.addLayout(output_layout)

        files_group.setLayout(files_layout)
        main_layout.addWidget(files_group)

        # Section: Traitement
        process_group = QGroupBox("2. Génération")
        process_layout = QVBoxLayout()

        # Bouton de génération
        self.generate_btn = QPushButton("🚀 Générer la vidéo avec overlays")
        self.generate_btn.setMinimumHeight(50)
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.generate_btn.clicked.connect(self.start_processing)
        process_layout.addWidget(self.generate_btn)

        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p% - %v/%m")
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
                height: 30px;
                font-size: 14px;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 3px;
            }
        """)
        process_layout.addWidget(self.progress_bar)

        # Label pour le temps restant
        self.time_label = QLabel("")
        self.time_label.setVisible(False)
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #4CAF50;")
        process_layout.addWidget(self.time_label)

        # Log de sortie
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setMaximumHeight(200)
        process_layout.addWidget(self.log_output)

        process_group.setLayout(process_layout)
        main_layout.addWidget(process_group)

        # Footer
        footer = QLabel(f"Version {APP_VERSION} • Traitement GPU accéléré (NVENC)")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("color: gray; font-size: 10px;")
        main_layout.addWidget(footer)

    def check_for_updates(self):
        """Vérifie les mises à jour au démarrage."""
        self.log("Vérification des mises à jour...")
        self.update_checker = UpdateChecker()
        self.update_checker.update_available.connect(self.show_update_dialog)
        self.update_checker.no_update.connect(lambda: self.log("Application à jour!"))
        self.update_checker.error.connect(lambda e: self.log(f"Impossible de vérifier les mises à jour: {e}"))
        self.update_checker.start()

    def show_update_dialog(self, version, url):
        """Affiche une boîte de dialogue pour la mise à jour."""
        reply = QMessageBox.question(
            self,
            "Mise à jour disponible",
            f"Une nouvelle version ({version}) est disponible!\n\n"
            f"Version actuelle: {APP_VERSION}\n"
            f"Nouvelle version: {version}\n\n"
            f"Voulez-vous télécharger la mise à jour?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            import webbrowser
            webbrowser.open(url)

    def select_xml(self):
        """Sélectionne le fichier XML."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Sélectionner le fichier XML",
            "",
            "XML Files (*.xml)"
        )
        if file_path:
            self.xml_path = file_path
            self.xml_input.setText(file_path)
            self.log(f"XML sélectionné: {Path(file_path).name}")

    def select_excel(self):
        """Sélectionne le fichier Excel."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Sélectionner le fichier Excel",
            "",
            "Excel Files (*.xlsx *.xls)"
        )
        if file_path:
            self.excel_path = file_path
            self.excel_input.setText(file_path)
            self.log(f"Excel sélectionné: {Path(file_path).name}")

    def select_videos(self):
        """Sélectionne les fichiers vidéo (multi-sélection possible)."""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Sélectionner les fichiers vidéo",
            "",
            "Fichiers vidéo (*.mp4 *.MP4 *.mov *.MOV);;Tous les fichiers (*.*)"
        )
        if file_paths:
            # Stocker le dossier parent du premier fichier
            self.video_folder = str(Path(file_paths[0]).parent)

            # Afficher les fichiers sélectionnés
            if len(file_paths) == 1:
                self.folder_input.setText(file_paths[0])
                self.log(f"✓ 1 fichier vidéo sélectionné: {Path(file_paths[0]).name}")
            else:
                self.folder_input.setText(f"{len(file_paths)} fichiers dans {self.video_folder}")
                self.log(f"✓ {len(file_paths)} fichiers vidéo sélectionnés:")
                for f in file_paths[:5]:  # Montrer max 5 fichiers
                    self.log(f"    • {Path(f).name}")
                if len(file_paths) > 5:
                    self.log(f"    ... et {len(file_paths) - 5} autre(s)")

    def select_output(self):
        """Sélectionne le fichier de sortie."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Enregistrer la vidéo sous",
            "output_final.mp4",
            "Video Files (*.mp4)"
        )
        if file_path:
            self.output_path = file_path
            self.output_input.setText(file_path)
            self.log(f"Sortie: {Path(file_path).name}")

    def start_processing(self):
        """Démarre le traitement vidéo."""
        # Validation
        if not self.xml_path or not self.excel_path or not self.video_folder:
            QMessageBox.warning(
                self,
                "Fichiers manquants",
                "Veuillez sélectionner tous les fichiers requis!"
            )
            return

        output = self.output_input.text() or "output_final.mp4"

        # Désactiver le bouton
        self.generate_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.time_label.setVisible(True)
        self.time_label.setText("Démarrage...")

        self.log("\n" + "=" * 50)
        self.log("DÉMARRAGE DU TRAITEMENT")
        self.log("=" * 50)

        # Lancer le thread de traitement
        self.process_thread = VideoProcessThread(
            self.xml_path,
            self.excel_path,
            self.video_folder,
            output
        )
        self.process_thread.progress.connect(self.log)
        self.process_thread.progress_percent.connect(self.update_progress)
        self.process_thread.progress_detail.connect(self.update_time_remaining)
        self.process_thread.finished.connect(self.processing_finished)
        self.process_thread.start()

    def update_progress(self, percent):
        """Met à jour la barre de progression."""
        self.progress_bar.setValue(percent)

    def update_time_remaining(self, current, total, time_str):
        """Met à jour le temps restant."""
        self.time_label.setText(f"📹 Segment {current}/{total} • ⏱️ Temps restant: ~{time_str}")

    def processing_finished(self, success, message):
        """Traitement terminé."""
        self.generate_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.time_label.setVisible(False)

        self.log("\n" + "=" * 50)
        self.log(message)
        self.log("=" * 50)

        if success:
            QMessageBox.information(
                self,
                "Succès!",
                "La vidéo a été générée avec succès!"
            )
        else:
            QMessageBox.critical(
                self,
                "Erreur",
                f"Une erreur s'est produite:\n{message}"
            )

    def log(self, message):
        """Ajoute un message au log."""
        self.log_output.append(message)
        # Auto-scroll vers le bas
        self.log_output.verticalScrollBar().setValue(
            self.log_output.verticalScrollBar().maximum()
        )


def main():
    """Point d'entrée de l'application."""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Style moderne

    window = PadelOverlayApp()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

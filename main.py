#!/usr/bin/env python3
"""
Automatisation de l'ajout d'overlays de score sur des vidéos de padel.
Lit un XML Premiere Pro et un fichier Excel avec les scores.
"""

import xml.etree.ElementTree as ET
import openpyxl
from pathlib import Path
import subprocess
import tempfile
import time
import platform
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from overlay_generator import PadelOverlayGenerator


class VideoOverlayAutomator:
    def __init__(self, xml_path, excel_path, video_folder=".",
                 team1_names="LÉO / YANNOUCK", team2_names="BILAL / PIERRE",
                 debug=False):
        self.xml_path = Path(xml_path)
        self.excel_path = Path(excel_path)
        self.video_folder = Path(video_folder)
        self.fps = 59.94  # NTSC 60fps (drop-frame)
        self.clips = []
        self.scores = []
        self.encoder = self.detect_gpu_encoder()
        self.overlay_generator = PadelOverlayGenerator()
        self.team1_names = team1_names
        self.team2_names = team2_names
        self.debug = debug

        # Configurer le logging
        if self.debug:
            # Créer le dossier logs s'il n'existe pas
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)

            # Nom du fichier log avec timestamp
            log_file = log_dir / f"video_processing_{time.strftime('%Y%m%d_%H%M%S')}.log"

            # Configuration du logging (fichier + console)
            logging.basicConfig(
                level=logging.DEBUG,
                format='[%(asctime)s] %(levelname)s: %(message)s',
                datefmt='%H:%M:%S',
                handlers=[
                    logging.FileHandler(log_file, encoding='utf-8'),
                    logging.StreamHandler()  # Affiche aussi dans la console
                ]
            )
            print(f"📝 Mode debug activé - Logs sauvegardés dans: {log_file}")
        else:
            logging.basicConfig(level=logging.WARNING)

    def detect_gpu_encoder(self):
        """Détecte le meilleur encodeur GPU disponible selon la plateforme."""
        system = platform.system()

        print("🔍 Détection de l'encodeur GPU...")

        # macOS: VideoToolbox
        if system == "Darwin":
            try:
                result = subprocess.run(
                    ['ffmpeg', '-hide_banner', '-encoders'],
                    capture_output=True, text=True, timeout=5
                )
                if 'hevc_videotoolbox' in result.stdout:
                    print("✅ GPU détecté: VideoToolbox (macOS)")
                    return {
                        'video_codec': 'hevc_videotoolbox',
                        'preset': None,
                        'crf': None,
                        'extra_params': [
                            '-q:v', '70',  # Plus bas = plus rapide (60 = bon compromis vitesse/qualité)
                            '-prio_speed', '1',  # Priorité à la vitesse d'encodage
                            '-realtime', '0',  # Pas de limitation temps réel
                            '-power_efficient', '-1'  # Max performance (0 = auto, 1 = économie d'énergie)
                        ]
                    }
            except:
                pass

        # Windows/Linux: NVIDIA NVENC
        elif system in ["Windows", "Linux"]:
            try:
                result = subprocess.run(
                    ['ffmpeg', '-hide_banner', '-encoders'],
                    capture_output=True, text=True, timeout=5
                )
                if 'hevc_nvenc' in result.stdout:
                    print("✅ GPU détecté: NVIDIA NVENC")
                    return {
                        'video_codec': 'hevc_nvenc',
                        'preset': 'p1',  # p1=fastest (max speed)
                        'crf': None,
                        'extra_params': [
                            '-rc:v', 'vbr',           # Variable bitrate (plus rapide que CBR)
                            '-b:v', '10M',            # Bitrate cible
                            '-maxrate:v', '15M',      # Bitrate max
                            '-bufsize:v', '20M',      # Buffer
                            '-spatial_aq', '1',       # Spatial AQ pour meilleure qualité
                            '-temporal_aq', '1',      # Temporal AQ
                            '-rc-lookahead', '20',    # Lookahead frames (compromis vitesse/qualité)
                            '-surfaces', '64',        # Max surfaces pour RTX (défaut 32)
                            '-2pass', '0'             # Désactive 2-pass (plus rapide)
                        ]
                    }
            except:
                pass

        # Fallback: CPU avec preset ultrafast
        print("⚠️  Pas de GPU détecté, utilisation CPU (ultrafast)")
        return {
            'video_codec': 'libx264',
            'preset': 'ultrafast',
            'crf': '23',
            'extra_params': []
        }

    def parse_xml(self):
        """Parse le XML Premiere Pro pour extraire les clips vidéo."""
        print(f"📄 Parsing XML: {self.xml_path}")
        tree = ET.parse(self.xml_path)
        root = tree.getroot()

        # Extraire tous les clips vidéo de la première track
        for track in root.findall('.//video/track'):
            for clipitem in track.findall('clipitem'):
                name = clipitem.find('name').text if clipitem.find('name') is not None else 'Unknown'
                start = int(clipitem.find('start').text) if clipitem.find('start') is not None else 0
                end = int(clipitem.find('end').text) if clipitem.find('end') is not None else 0
                in_point = int(clipitem.find('in').text) if clipitem.find('in') is not None else 0
                out_point = int(clipitem.find('out').text) if clipitem.find('out') is not None else 0

                # Trouver le chemin du fichier source
                file_elem = clipitem.find('.//file')
                pathurl = file_elem.find('pathurl').text if file_elem is not None and file_elem.find('pathurl') is not None else ''

                self.clips.append({
                    'name': name,
                    'start_frame': start,
                    'end_frame': end,
                    'in_frame': in_point,
                    'out_frame': out_point,
                    'duration_frames': end - start,
                    'pathurl': pathurl
                })
            break  # On prend seulement la première track

        print(f"✅ Found {len(self.clips)} video clips")
        return self.clips

    def parse_excel(self):
        """Parse le fichier Excel pour extraire les scores."""
        print(f"📊 Parsing Excel: {self.excel_path}")
        wb = openpyxl.load_workbook(self.excel_path)
        ws = wb.active

        # Lire les scores (skip header row)
        # Colonnes: Set, Num_Point, Set 1, Set 2, Jeux, Points, Commentaires
        for row in ws.iter_rows(min_row=2, values_only=True):
            if row[0] is not None:  # Si la row n'est pas vide
                set_num = row[0]
                point_num = row[1]
                set1 = row[2] if len(row) > 2 and row[2] is not None else None
                set2 = row[3] if len(row) > 3 and row[3] is not None else None
                jeux = row[4] if len(row) > 4 and row[4] is not None else "0/0"
                points = row[5] if len(row) > 5 and row[5] is not None else "0/0"
                commentaires = row[6] if len(row) > 6 and row[6] is not None else ""

                self.scores.append({
                    'set': set_num,
                    'point': point_num,
                    'set1': set1 if set1 else None,
                    'set2': set2 if set2 else None,
                    'jeux': jeux if jeux else "0/0",
                    'points': points if points else "0/0",
                    'commentaires': commentaires if commentaires else ""
                })

        print(f"✅ Found {len(self.scores)} scores")
        return self.scores

    def frames_to_seconds(self, frames):
        """Convertit des frames en secondes (NTSC)."""
        return frames / self.fps

    def find_video_file(self, clip_name):
        """Trouve le fichier vidéo source."""
        video_path = self.video_folder / clip_name
        if video_path.exists():
            return str(video_path)

        # Si pas trouvé, chercher dans le dossier courant
        current_path = Path('.') / clip_name
        if current_path.exists():
            return str(current_path)

        raise FileNotFoundError(f"Video file not found: {clip_name}")

    def get_video_bitrate(self, video_file):
        """Extrait le bitrate de la vidéo source."""
        try:
            result = subprocess.run(
                ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                 '-show_entries', 'stream=bit_rate', '-of', 'default=noprint_wrappers=1:nokey=1',
                 video_file],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0 and result.stdout.strip():
                bitrate_bps = int(result.stdout.strip())
                bitrate_mbps = bitrate_bps / 1_000_000
                return bitrate_mbps
        except:
            pass
        return None

    def format_time(self, seconds):
        """Formate le temps en heures:minutes:secondes."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        if hours > 0:
            return f"{hours}h{minutes:02d}m{secs:02d}s"
        elif minutes > 0:
            return f"{minutes}m{secs:02d}s"
        else:
            return f"{secs}s"

    def process_single_segment(self, i, clip, score, temp_path, original_bitrate, total_clips):
        """Traite un seul segment vidéo (pour parallélisation)."""
        segment_start_time = time.time()
        timings = {}

        print(f"\n[{i}/{total_clips}] Processing clip: {clip['name']}")
        logging.debug(f"Segment {i}: Début du traitement")

        # Trouver le fichier vidéo source
        t0 = time.time()
        try:
            video_file = self.find_video_file(clip['name'])
        except FileNotFoundError as e:
            print(f"⚠️  {e}, skipping...")
            return None
        timings['find_file'] = time.time() - t0
        logging.debug(f"Segment {i}: Fichier trouvé en {timings['find_file']:.3f}s")

        # Calculer les timestamps
        t0 = time.time()
        start_time = self.frames_to_seconds(clip['in_frame'])
        duration = self.frames_to_seconds(clip['duration_frames'])
        timings['calc_timestamps'] = time.time() - t0

        print(f"   Start: {start_time:.2f}s, Duration: {duration:.2f}s")

        # Déterminer quels sets afficher
        t0 = time.time()
        display_set1 = score['set1'] if score['set1'] and score['set1'] != score['jeux'] else None
        display_set2 = score['set2'] if score['set2'] and score['set2'] != score['jeux'] else None
        timings['calc_scores'] = time.time() - t0

        print(f"   Set1: {display_set1} | Set2: {display_set2} | Jeux: {score['jeux']} | Points: {score['points']}")

        # Créer l'overlay
        t0 = time.time()
        overlay_img = self.overlay_generator.create_overlay(
            team1_names=self.team1_names,
            team2_names=self.team2_names,
            jeux=score['jeux'],
            points=score['points'],
            set1=display_set1,
            set2=display_set2
        )
        overlay_path = temp_path / f"overlay_{i:03d}.png"
        self.overlay_generator.save_overlay(overlay_img, str(overlay_path))
        timings['create_overlay'] = time.time() - t0
        logging.debug(f"Segment {i}: Overlay créé en {timings['create_overlay']:.3f}s")

        # Créer le segment avec overlay
        segment_path = temp_path / f"segment_{i:03d}.mp4"

        # Construire la commande FFmpeg
        t0 = time.time()
        ffmpeg_cmd = [
            'ffmpeg',
            '-hwaccel', 'cuda',
            '-hwaccel_output_format', 'cuda',
            '-ss', str(start_time),
            '-i', video_file,
            '-i', str(overlay_path),
            '-filter_complex', '[0:v]hwdownload,format=nv12[base];[base][1:v]overlay=0:0,format=nv12,hwupload_cuda[out]',
            '-map', '[out]',
            '-t', str(duration),
            '-c:v', self.encoder['video_codec']
        ]

        if self.encoder['preset']:
            ffmpeg_cmd.extend(['-preset', self.encoder['preset']])

        if self.encoder['crf']:
            ffmpeg_cmd.extend(['-crf', self.encoder['crf']])

        # Utiliser le bitrate original si détecté
        if original_bitrate and self.encoder['video_codec'] == 'hevc_nvenc':
            custom_params = []
            for j, param in enumerate(self.encoder['extra_params']):
                if param == '-b:v':
                    custom_params.extend(['-b:v', f'{int(original_bitrate)}M'])
                    continue
                elif param == '-maxrate:v':
                    custom_params.extend(['-maxrate:v', f'{int(original_bitrate * 1.2)}M'])
                    continue
                elif param == '-bufsize:v':
                    custom_params.extend(['-bufsize:v', f'{int(original_bitrate * 2)}M'])
                    continue
                if j > 0 and self.encoder['extra_params'][j-1] in ['-b:v', '-maxrate:v', '-bufsize:v']:
                    continue
                custom_params.append(param)
            ffmpeg_cmd.extend(custom_params)
        else:
            ffmpeg_cmd.extend(self.encoder['extra_params'])

        # Audio: copier si déjà en AAC, sinon réencoder
        ffmpeg_cmd.extend([
            '-c:a', 'copy',  # Copie l'audio (pas de réencodage)
            '-y',
            str(segment_path)
        ])

        timings['build_cmd'] = time.time() - t0

        print(f"   Running FFmpeg ({self.encoder['video_codec']})...")
        logging.debug(f"Segment {i}: Commande FFmpeg: {' '.join(ffmpeg_cmd)}")

        t0 = time.time()
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        timings['ffmpeg_execution'] = time.time() - t0
        logging.debug(f"Segment {i}: FFmpeg exécuté en {timings['ffmpeg_execution']:.3f}s")

        if result.returncode != 0:
            print(f"   ❌ FFmpeg error: {result.stderr}")
            logging.error(f"Segment {i}: Erreur FFmpeg: {result.stderr}")
            return None

        segment_elapsed = time.time() - segment_start_time
        print(f"   ✅ Segment créé en {self.format_time(segment_elapsed)}")

        # Log détaillé des timings
        if self.debug:
            logging.debug(f"Segment {i}: Timings détaillés:")
            for key, value in timings.items():
                pct = (value / segment_elapsed) * 100
                logging.debug(f"  - {key}: {value:.3f}s ({pct:.1f}%)")

        return {
            'path': str(segment_path),
            'time': segment_elapsed,
            'index': i,
            'timings': timings if self.debug else None
        }

    def process_video(self, output_path="output_final.mp4"):
        """
        Traite la vidéo complète avec les overlays.
        """
        print(f"\n🎬 Starting video processing...")
        total_start_time = time.time()

        # Détecter le bitrate de la première vidéo source
        original_bitrate = None
        if self.clips:
            try:
                first_video = self.find_video_file(self.clips[0]['name'])
                original_bitrate = self.get_video_bitrate(first_video)
                if original_bitrate:
                    print(f"📊 Bitrate original détecté: {original_bitrate:.1f} Mbps")
            except:
                pass

        # Créer un dossier temporaire pour les segments
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Traitement parallèle des segments (optimal pour RTX 5070)
            # Note: RTX 5070 a ~2-3 encodeurs NVENC, plus de workers = contention
            max_workers = 3
            print(f"\n🚀 Traitement parallèle activé ({max_workers} workers)")

            segments_data = []
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                # Soumettre tous les jobs
                futures = {}
                for i, (clip, score) in enumerate(zip(self.clips, self.scores), 1):
                    future = executor.submit(
                        self.process_single_segment,
                        i, clip, score, temp_path, original_bitrate, len(self.clips)
                    )
                    futures[future] = i

                # Récupérer les résultats au fur et à mesure
                completed = 0
                for future in as_completed(futures):
                    completed += 1
                    result = future.result()
                    if result:
                        segments_data.append(result)

                    # Afficher progression
                    print(f"\n📊 Progression: {completed}/{len(self.clips)} segments terminés")

            # Trier les segments par index et extraire les paths
            segments_data.sort(key=lambda x: x['index'])
            segments = [s['path'] for s in segments_data]
            segment_times = [s['time'] for s in segments_data]

            # Statistiques
            if segment_times:
                avg_time = sum(segment_times) / len(segment_times)
                print(f"\n⏱️  Temps moyen par segment: {self.format_time(avg_time)}")

                # Rapport détaillé des timings en mode debug
                if self.debug:
                    logging.debug("\n========== RAPPORT DÉTAILLÉ DES TIMINGS ==========")
                    all_timings = {}
                    for seg in segments_data:
                        if seg.get('timings'):
                            for key, value in seg['timings'].items():
                                if key not in all_timings:
                                    all_timings[key] = []
                                all_timings[key].append(value)

                    logging.debug("\nTemps moyens par étape:")
                    for key, values in all_timings.items():
                        avg = sum(values) / len(values)
                        min_val = min(values)
                        max_val = max(values)
                        logging.debug(f"  {key}:")
                        logging.debug(f"    Moyenne: {avg:.3f}s | Min: {min_val:.3f}s | Max: {max_val:.3f}s")
                    logging.debug("=" * 50)

            # Concaténer tous les segments
            if segments:
                concat_start_time = time.time()
                print(f"\n🔗 Concatenating {len(segments)} segments...")

                # Créer le fichier de liste pour FFmpeg
                concat_file = temp_path / "concat_list.txt"
                with open(concat_file, 'w') as f:
                    for seg in segments:
                        f.write(f"file '{seg}'\n")

                # Concaténer
                concat_cmd = [
                    'ffmpeg',
                    '-f', 'concat',
                    '-safe', '0',
                    '-i', str(concat_file),
                    '-c', 'copy',
                    '-y',
                    output_path
                ]

                result = subprocess.run(concat_cmd, capture_output=True, text=True)

                concat_elapsed = time.time() - concat_start_time

                if result.returncode == 0:
                    print(f"\n✅ Final video created: {output_path}")
                    print(f"📹 Total segments: {len(segments)}")
                    print(f"⏱️  Concatenation time: {self.format_time(concat_elapsed)}")
                else:
                    print(f"\n❌ Concatenation failed: {result.stderr}")
            else:
                print("\n❌ No segments were created")

            total_elapsed = time.time() - total_start_time
            print(f"\n⏱️  TEMPS TOTAL: {self.format_time(total_elapsed)}")

    def run(self, output_path="output_final.mp4"):
        """Exécute le workflow complet."""
        print("=" * 60)
        print("🎾 PADEL VIDEO OVERLAY AUTOMATOR")
        print("=" * 60)

        self.parse_xml()
        self.parse_excel()

        # Vérifier la correspondance
        if len(self.clips) != len(self.scores):
            print(f"\n⚠️  WARNING: {len(self.clips)} clips but {len(self.scores)} scores")
            print(f"   Using minimum: {min(len(self.clips), len(self.scores))}")
            min_len = min(len(self.clips), len(self.scores))
            self.clips = self.clips[:min_len]
            self.scores = self.scores[:min_len]

        self.process_video(output_path)

        print("\n" + "=" * 60)
        print("✨ DONE!")
        print("=" * 60)


if __name__ == "__main__":
    # Configuration
    XML_FILE = "data/Sequence_timeframe.xml"
    EXCEL_FILE = "data/match_points.xlsx"
    OUTPUT_FILE = "output/output_final.mp4"
    VIDEO_FOLDER = "data"  # Dossier contenant les vidéos sources

    # Activer le mode debug (mettre False pour désactiver)
    DEBUG_MODE = True

    # Lancer l'automatisation
    automator = VideoOverlayAutomator(XML_FILE, EXCEL_FILE, VIDEO_FOLDER, debug=DEBUG_MODE)
    automator.run(OUTPUT_FILE)

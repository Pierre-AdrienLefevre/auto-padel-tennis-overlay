# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a video automation tool for adding score overlays to padel match videos edited in Adobe Premiere Pro. The workflow:

1. User edits padel match video in Premiere Pro, cutting it point-by-point
2. User exports the timeline as Final Cut Pro XML (Fichier → Exporter → Final Cut Pro XML)
3. User maintains match scores in an Excel file (`match_points.xlsx`)
4. Python script automatically:
   - Parses the XML to extract timestamps of each cut/clip
   - Reads the Excel file to get scores for each point
   - Generates video overlays displaying scores
   - Produces final video with overlays using FFmpeg

## Key Files

- `main.py` - Main automation script
- `Séquence 01.xml` - Example Premiere Pro XML export (Final Cut Pro XML format)
- `match_points.xlsx` - Excel file containing match scores for each point
- `VID_20250927_091606_00_*.mp4` - Source video files (typically very large, 13GB+)

## XML Structure (Premiere Pro Export)

The Premiere Pro XML export contains:
- Multiple `<clipitem>` elements, each representing a cut/segment in the timeline
- Each clipitem has:
  - `<start>` and `<end>` - Timeline position in the sequence (in frames)
  - `<in>` and `<out>` - Source file timecodes (in frames)
  - Frame rate: 60fps with NTSC timing (`<timebase>60</timebase><ntsc>TRUE</ntsc>`)
- Source files referenced via `<file>` elements with `<pathurl>`

## Excel Structure

The `match_points.xlsx` file needs to be examined to understand column structure. Expected format includes score information for each point that corresponds to the clips in the timeline.

## Development Environment

- Python 3.13+
- Project uses `pyproject.toml` for dependency management
- Key dependencies needed:
  - `openpyxl` or `pandas` for Excel reading
  - `xml.etree.ElementTree` or `lxml` for XML parsing
  - `ffmpeg-python` or subprocess calls to FFmpeg for video processing
  - `Pillow` or `opencv-python` for overlay generation

## Workflow Implementation Notes

- The number of clips in the XML should match the number of rows in the Excel file
- Each clip represents one point in the match
- Overlay should appear at the bottom-left of the video (based on user's existing template)
- Need to handle NTSC drop-frame timecode conversion (59.94fps)
- Videos are large (13GB+) - processing efficiency is important

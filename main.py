import os
import csv
from datetime import datetime
from typing import List

import numpy as np
from pydub import AudioSegment
import streamlit as st

SAMPLE_RATE = 44100  # Hertz
BASE_FREQUENCY = 440  # Base tone frequency in Hz

def list_tracks(directory: str = '.') -> List[str]:
    """Return a list of MP3 files available in the given directory."""
    return [f for f in os.listdir(directory) if f.lower().endswith('.mp3')]

def create_tone(freq: float, duration_sec: float) -> AudioSegment:
    """Generate a binaural beat tone.

    Args:
        freq: Frequency difference between left and right channels in Hz.
        duration_sec: Length of the tone in seconds.

    Returns:
        A stereo AudioSegment containing the binaural tone.
    """
    t = np.linspace(0, duration_sec, int(SAMPLE_RATE * duration_sec), False)
    left_wave = np.sin(2 * np.pi * BASE_FREQUENCY * t)
    right_wave = np.sin(2 * np.pi * (BASE_FREQUENCY + freq) * t)
    audio = np.stack([left_wave, right_wave], axis=1)
    audio *= (2**15 - 1) / np.max(np.abs(audio))
    audio = audio.astype(np.int16)
    tone = AudioSegment(
        audio.tobytes(),
        frame_rate=SAMPLE_RATE,
        sample_width=2,
        channels=2,
    )
    return tone

def mix_audio(tone: AudioSegment, track_path: str, duration_sec: float) -> AudioSegment:
    """Overlay tone with the background track looped for the given duration."""
    background = AudioSegment.from_file(track_path)
    loops = int(duration_sec * 1000 / len(background)) + 1
    background_loop = background * loops
    background_loop = background_loop[: int(duration_sec * 1000)]
    mixed = background_loop.overlay(tone)
    return mixed

def export_session(audio: AudioSegment, output_dir: str = '.') -> str:
    """Export the AudioSegment to MP3 and return the file path."""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"session_{timestamp}.mp3"
    path = os.path.join(output_dir, filename)
    audio.export(path, format='mp3')
    return path

def log_request(brainwave: str, duration: int, track: str, output_file: str) -> None:
    """Append a session entry to session_log.csv."""
    log_exists = os.path.exists('session_log.csv')
    with open('session_log.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not log_exists:
            writer.writerow(['timestamp', 'brainwave', 'duration_min', 'track', 'output'])
        writer.writerow([
            datetime.now().isoformat(),
            brainwave,
            duration,
            track,
            output_file,
        ])

def main() -> None:
    st.title('Binaural Beat Generator')

    tracks = list_tracks()
    if not tracks:
        st.warning('No MP3 tracks found in the app directory.')
    brainwaves = {'Delta': 2, 'Theta': 5, 'Alpha': 10, 'Beta': 15}

    wave_choice = st.selectbox('Brainwave Type', list(brainwaves.keys()))
    duration_choice = st.selectbox('Session Duration (minutes)', [1, 5, 10, 15, 20, 30])
    track_choice = st.selectbox('Background Track', tracks)

    if st.button('Generate'):
        tone = create_tone(brainwaves[wave_choice], duration_choice * 60)
        track_path = os.path.join('.', track_choice)
        if not os.path.exists(track_path):
            st.error(f'Background track "{track_choice}" not found. Please contact support@humn.be')
            return
        mixed = mix_audio(tone, track_path, duration_choice * 60)
        out_path = export_session(mixed)
        log_request(wave_choice, duration_choice, track_choice, out_path)
        with open(out_path, 'rb') as f:
            st.download_button('Download MP3', f, file_name=os.path.basename(out_path))

if __name__ == '__main__':
    main()

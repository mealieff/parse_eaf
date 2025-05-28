import sys
import wave
import contextlib
from pydub import AudioSegment
from textgrid import TextGrid
from textgrid import IntervalTier
import argparse

def extract_annotated_segments(wav_path, textgrid_path, out_wav_path, out_textgrid_path, tier_name=None):
    # Load audio
    audio = AudioSegment.from_wav(wav_path)

    # Load TextGrid
    tg = TextGrid()
    tg.read(textgrid_path)

    # Find the tier to use
    if tier_name:
        tier = next((t for t in tg.tiers if t.name == tier_name), None)
        if not tier:
            raise ValueError(f"Tier '{tier_name}' not found in TextGrid.")
    else:
        # Use first interval tier by default
        tier = next((t for t in tg.tiers if hasattr(t, 'intervals')), None)
        if not tier:
            raise ValueError("No interval tier found in TextGrid.")

    # Extract annotated intervals (non-empty labels)
    annotated_intervals = [iv for iv in tier.intervals if iv.mark.strip()]

    # Concatenate audio segments and build new intervals
    new_audio = AudioSegment.empty()
    new_intervals = []
    current_time = 0.0

    for iv in annotated_intervals:
        start_ms = int(iv.minTime * 1000)
        end_ms = int(iv.maxTime * 1000)
        segment = audio[start_ms:end_ms]
        new_audio += segment
        duration = (end_ms - start_ms) / 1000.0
        new_intervals.append((current_time, current_time + duration, iv.mark))
        current_time += duration

    # Export new audio
    new_audio.export(out_wav_path, format="wav")

    # Create new TextGrid
    new_tg = TextGrid(minTime=0, maxTime=current_time)
    new_tier = IntervalTier(name=tier.name, minTime=0, maxTime=current_time)
    for start, end, label in new_intervals:
        new_tier.add(start, end, label)
    new_tg.append(new_tier)
    new_tg.write(out_textgrid_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract annotated segments from WAV and TextGrid.")
    parser.add_argument("wav", help="Input WAV file")
    parser.add_argument("textgrid", help="Input TextGrid file")
    parser.add_argument("out_wav", help="Output WAV file")
    parser.add_argument("out_textgrid", help="Output TextGrid file")
    parser.add_argument("--tier", help="Tier name (optional)", default=None)
    args = parser.parse_args()

    extract_annotated_segments(args.wav, args.textgrid, args.out_wav, args.out_textgrid, args.tier)
import tgt
import parselmouth
import numpy as np
import argparse
import json

def get_time_points(start, end):
    """Return 5%, 50%, and 95% time points between start and end."""
    duration = end - start
    return [start + 0.05 * duration, start + 0.5 * duration, start + 0.95 * duration]

def extract_pitch_and_formants(sound, time_points):
    """Extract F0, F2, and F3 at given time points from a parselmouth.Sound object."""
    pitch = sound.to_pitch()
    formant = sound.to_formant_burg()
    results = []
    for t in time_points:
        f0 = pitch.get_value_at_time(t)
        f2 = formant.get_value_at_time(2, t)
        f3 = formant.get_value_at_time(3, t)
        results.append({'time': t, 'F0': f0, 'F2': f2, 'F3': f3})
    return results

def analyze_textgrid(textgrid_path, wav_path, tier_name):
    tg = tgt.read_textgrid(textgrid_path)
    tier = tg.get_tier_by_name(tier_name)
    snd = parselmouth.Sound(wav_path)
    analysis = []
    for interval in tier.intervals:
        if interval.text.strip() == "":
            continue
        time_points = get_time_points(interval.start_time, interval.end_time)
        feats = extract_pitch_and_formants(snd, time_points)
        analysis.append({
            'label': interval.text,
            'start': interval.start_time,
            'end': interval.end_time,
            'features': feats
        })
    return analysis

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Analyze F0, F2, F3 at 5%, 50%, 95% of intervals in a TextGrid.")
    parser.add_argument("textgrid", help="Path to TextGrid file")
    parser.add_argument("wav", help="Path to corresponding WAV file")
    parser.add_argument("tier", help="Tier name to analyze")
    parser.add_argument("--output", help="Output JSON file", default="analysis.json")
    args = parser.parse_args()

    results = analyze_textgrid(args.textgrid, args.wav, args.tier)
    with open(args.output, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Analysis saved to {args.output}")

    ## Update this script so output is written to csv file
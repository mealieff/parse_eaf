import os
import argparse
import xml.etree.ElementTree as ET
from praatio import tgio
import soundfile as sf

def parse_eaf(eaf_file, tier_name):
    """
    Parse ELAN EAF file and extract aligned annotations (start, end, text) from specified tier.
    Returns list of dicts with keys: start (sec), end (sec), text (str).
    """
    tree = ET.parse(eaf_file)
    root = tree.getroot()

    # Map TIME_SLOT_ID to time in ms
    time_slots = {}
    for ts in root.findall(".//TIME_SLOT"):
        ts_id = ts.attrib["TIME_SLOT_ID"]
        time_slots[ts_id] = int(ts.attrib.get("TIME_VALUE", 0))

    # Find tier by TIER_ID
    tier = None
    for t in root.findall("TIER"):
        if t.attrib.get("TIER_ID") == tier_name:
            tier = t
            break
    if tier is None:
        raise ValueError(f"Tier '{tier_name}' not found in {eaf_file}")

    annotations = []
    for ann in tier.findall(".//ALIGNABLE_ANNOTATION"):
        ts_ref1 = ann.attrib["TIME_SLOT_REF1"]
        ts_ref2 = ann.attrib["TIME_SLOT_REF2"]
        start_sec = time_slots.get(ts_ref1, 0) / 1000.0
        end_sec = time_slots.get(ts_ref2, 0) / 1000.0
        text_elem = ann.find("ANNOTATION_VALUE")
        text = text_elem.text.strip() if text_elem is not None else ""
        annotations.append({"start": start_sec, "end": end_sec, "text": text})

    print(f"Found {len(annotations)} annotations in tier '{tier_name}':")
    for ann in annotations:
        print(f"  start={ann['start']}, end={ann['end']}, text='{ann['text']}'")

    return annotations

def write_text_file(annotations, txt_path):
    """
    Writes a plain text transcript by concatenating all annotation texts separated by spaces.
    """
    transcript = " ".join(ann["text"] for ann in annotations if ann["text"].strip() != "")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(transcript)
    print(f"Wrote transcript text to {txt_path}")

def write_textgrid(annotations, tg_path, wav_path):
    with sf.SoundFile(wav_path) as f:
        duration = f.frames / f.samplerate

    intervals = []
    for ann in annotations:
        if ann["text"].strip():
            intervals.append((ann["start"], ann["end"], ann["text"]))

    print(f"Number of intervals to write to TextGrid: {len(intervals)}")

    tg = tgio.Textgrid()
    tg.addTier(tgio.IntervalTier("words", intervals, 0, duration))
    tg.save(tg_path)  # No extra arguments
    print(f"Wrote TextGrid to {tg_path}")



def main():
    parser = argparse.ArgumentParser(description="Convert EAF + WAV to MFA-compatible .txt and .TextGrid files")
    parser.add_argument("--eaf", required=True, help="Input ELAN .eaf file path")
    parser.add_argument("--wav", required=True, help="Corresponding WAV audio file path")
    parser.add_argument("--tier", default="transcription", help="Tier name in EAF to extract (default: transcription)")
    parser.add_argument("--out_dir", required=True, help="Output directory to save .txt and .TextGrid")
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    annotations = parse_eaf(args.eaf, args.tier)

    base_name = os.path.splitext(os.path.basename(args.wav))[0]
    txt_path = os.path.join(args.out_dir, f"{base_name}.txt")
    tg_path = os.path.join(args.out_dir, f"{base_name}.TextGrid")

    write_text_file(annotations, txt_path)
    write_textgrid(annotations, tg_path, args.wav)

if __name__ == "__main__":
    main()


# Sample usage: 
# python ../parse_eaf/parse.py --eaf mfa_corpus/setpu_negatives.eaf --wav mfa_corpus/setpu_negatives.wav --tier transcription --out_dir mfa_corpus 

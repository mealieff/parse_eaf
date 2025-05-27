import argparse
import os
import sys
import subprocess
from xml.etree import ElementTree as ET

def extract_transcription(eaf_path, tier_name):
    tree = ET.parse(eaf_path)
    root = tree.getroot()
    ns = {'elan': 'http://www.w3.org/2001/XMLSchema-instance'}

    # Find the tier
    tier = None
    for t in root.findall('TIER'):
        if t.attrib.get('TIER_ID') == tier_name:
            tier = t
            break
    if tier is None:
        raise ValueError(f"Tier '{tier_name}' not found in {eaf_path}")

    # Extract annotations
    annotations = []
    for ann in tier.findall('ANNOTATION/ALIGNABLE_ANNOTATION'):
        value = ann.find('ANNOTATION_VALUE')
        if value is not None and value.text:
            annotations.append(value.text.strip())
    return ' '.join(annotations)

def write_text_for_fave(text, wav_path, temp_dir):
    basename = os.path.splitext(os.path.basename(wav_path))[0]
    txt_path = os.path.join(temp_dir, f"{basename}.txt")
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(text)
    return txt_path

def run_fave_align(fave_dir, wav_path, txt_path, output_path):
    align_script = os.path.join(fave_dir, "fave-align.py")
    dict_path = os.path.join(fave_dir, "dict", "cmudict.0.7a.plain")
    model_path = os.path.join(fave_dir, "model", "english.nnet.chain.tdnn1b_sp")
    cmd = [
        sys.executable, align_script,
        wav_path, txt_path, output_path,
        '--dict', dict_path,
        '--model', model_path
    ]
    subprocess.run(cmd, check=True)

def main():
    parser = argparse.ArgumentParser(description="Force align EAF transcription tier using FAVE-align.")
    parser.add_argument('eaf_file', help='Path to ELAN .eaf file')
    parser.add_argument('wav_file', help='Path to corresponding .wav file')
    parser.add_argument('output_dir', help='Directory to save the output TextGrid')
    parser.add_argument('--tier', default='transcription', help='Name of the transcription tier (default: transcription)')
    parser.add_argument('--fave_dir', default='FAVE-align', help='Path to FAVE-align directory')
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    temp_dir = args.output_dir

    # Extract transcription
    transcription = extract_transcription(args.eaf_file, args.tier)
    if not transcription:
        print("No transcription found in the specified tier.")
        sys.exit(1)

    # Write text for FAVE
    txt_path = write_text_for_fave(transcription, args.wav_file, temp_dir)

    # Output TextGrid path
    basename = os.path.splitext(os.path.basename(args.wav_file))[0]
    textgrid_path = os.path.join(args.output_dir, f"{basename}.TextGrid")

    # Run FAVE-align
    try:
        run_fave_align(args.fave_dir, args.wav_file, txt_path, textgrid_path)
        print(f"Alignment complete. Output saved to {textgrid_path}")
    except subprocess.CalledProcessError as e:
        print("FAVE-align failed:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
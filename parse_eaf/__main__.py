import sys
import os
import argparse
from parse import *

def parse_args():
    parser = argparse.ArgumentParser(description="Train and test Tone2Vec model, save model, and perform clustering.")
    parser.add_argument("--data_dir", type=str, default="~/dataset", help="Path to input data directory")
    parser.add_argument("--output_dir", type=str, default="~/output", help="Path to output transcriptions")
    return parser.parse_args()

def main():
    args = parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    dataset = [f for f in os.listdir(args.data_dir) if f.endswith(".txt")]
    eaf_files = [f for f in os.listdir(args.data_dir) if f.endswith(".eaf")]

    for eaf_file in eaf_files:
        wav_file = eaf_file.replace(".eaf", ".wav")
        wav_path = os.path.join(args.data_dir, "audio", wav_file)
        eaf_path = os.path.join(args.data_dir, eaf_file)

        if os.path.exists(wav_path):
            train_data.extend(process_eaf_data(eaf_path, wav_path))
    with open(os.path.join(args.output_dir, "train_segments.jsonl"), "w", encoding="utf-8") as f:
        for fn in dataset:
            text = open(args.data_dir+'/'+fn).read()
            f.write(json.dumps({"text": text}, ensure_ascii=False) + "\n")

    vocab = create_vocab(text)
    with open(os.path.join(args.output_dir, "vocab.json"), "w", encoding="utf-8") as f:
        json.dump(vocab, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()

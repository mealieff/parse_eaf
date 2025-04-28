# parse_eaf
This tool extracts pairs of audio file and transcription from EAF. EAF files + ELAN link. EAF is an XML file with time offsets + tiers. Explain how the modules extract this data and the output. 
- Include a toy example (WAV file + EAF file around 3 sentences)


# main.py

outputs : train_segments.jsonl and vocab.json


# example use

- example how to use it as a command line tool, and how to use the modules

python3 main.py --data_dir ./aligned_lamkang --output_dir ./processed_data
python -m parse_eaf

# parse_eaf
This Python module extracts pairs of audio file and transcription from ELAN .eaf files. ELAN (EUDICO Linguistic Annotator) is widely used in linguistic fieldwork to annotate audio and video data. ELAN '.eaf' files are XML containing time stamps and a number of annotation tiers. This module simplifies the parsing and extraction of tiered time-aligned annotations for downstream processing.


### Modular functions in 'main.py'

`parse_eaf(eaf_file)`: Parses an ELAN `.eaf` XML file and extracts time-aligned annotations. It converts timestamp references into actual time in seconds and returns a list of dictionaries with `start`, `end`, and `text` fields for each annotation.

`extract_audio_segments(wav_file, annotations)`: Uses the timestamps from the annotations to extract corresponding audio segments from a WAV file using `soundfile`. Returns a list of dictionaries, each containing a NumPy array of audio (`speech`) and its matching transcript (`text`).

`process_eaf_data(eaf_path, wav_path)`: Combines `parse_eaf` and `extract_audio_segments` into a pipeline: given an EAF file and its associated audio, it returns the aligned speech/text data in one step.

`create_vocab(data_dir)`: Builds a character-level vocabulary from the transcriptions in the dataset. It assigns a unique index to each character and adds special tokens like `<unk>` and `<pad>`. Saves the vocabulary as a JSON file in the specified directory.

Processing output: 'train_segments.jsonl' and 'vocab.json'


# example use

- example how to use it as a command line tool, and how to use the modules

python3 main.py --data_dir ./aligned_lamkang --output_dir ./processed_data
python -m parse_eaf

# File Stucture 
```
parse_eaf/
├── __init__.py       # Package marker
├── main.py           # Main parsing functions
```

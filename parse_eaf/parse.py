import os
import argparse
import numpy as np
import xml.etree.ElementTree as ET
import json
import soundfile as sf


def parse_eaf(eaf_file):
    """
    Parses an ELAN (.eaf) file and extracts aligned transcriptions.
    Returns:
        List of dicts with 'start', 'end', and 'text' timestamps.
    """
    tree = ET.parse(eaf_file)
    root = tree.getroot()
    
    time_slots = {}
    for ts in root.findall(".//TIME_SLOT"):
        time_id = ts.attrib["TIME_SLOT_ID"]
        time_value = int(ts.attrib["TIME_VALUE"])  # Time in milliseconds
        time_slots[time_id] = time_value
    
    annotations = []
    for ann in root.findall(".//ANNOTATION"):
        time_ref1 = ann.find(".//ALIGNABLE_ANNOTATION").attrib["TIME_SLOT_REF1"]
        time_ref2 = ann.find(".//ALIGNABLE_ANNOTATION").attrib["TIME_SLOT_REF2"]
        start = time_slots[time_ref1] / 1000  # Convert ms to seconds
        end = time_slots[time_ref2] / 1000
        
        text_element = ann.find(".//ANNOTATION_VALUE")
        if text_element is not None:
            text = text_element.text.strip()
            annotations.append({"start": start, "end": end, "text": text})
    
    return annotations

def extract_audio_segments(wav_file, annotations):
    """
    Extracts segments from a WAV file based on EAF timestamps.
    
    Returns:
        List of dicts with extracted audio & corresponding transcription.
    """
    speech_segments = []
    for ann in annotations:
        start_frame = int(ann["start"] * SAMPLING_RATE)
        end_frame = int(ann["end"] * SAMPLING_RATE)

        speech_array, _ = sf.read(wav_file, start=start_frame, stop=end_frame)
        speech_segments.append({"speech": speech_array, "text": ann["text"]})
    
    return speech_segments

def process_eaf_data(eaf_path, wav_path):
    """
    Parses EAF file and extracts corresponding speech from WAV file.
    Returns:
        List of processed training data.
    """
    annotations = parse_eaf(eaf_path)
    return extract_audio_segments(wav_path, annotations)

def create_vocab(text):
    vocab = {}
    for char in text: 
       if char not in vocab:
           vocab[char] = len(vocab)
    vocab["<unk>"] = len(vocab)
    vocab["<pad>"] = len(vocab)
    return vocab

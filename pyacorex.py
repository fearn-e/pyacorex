import json
import numpy as np
import os
import sys

if len(sys.argv) < 2:
    print(f'Usage: {sys.argv[0]} filename.wav')
    sys.exit(-1)

def load_acorex_corpus(json_path):
    data = None
    try:
        with open(json_path, 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        print(f"JSON file {sys.argv[1]} not found.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON file {sys.argv[1]}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    audio_files_JSON = data.get("fileList", [])
    corpus_values_JSON = data.get("time.raw", [])

    audio_files = []
    for file_path in audio_files_JSON:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as audio_file:
                    audio_files.append(audio_file.read())
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
        else:
            print(f"File {file_path} not found.")

    corpus_values = [np.array(item) for item in corpus_values_JSON]

    return audio_files, corpus_values

def main():
    audio_files, corpus_values = load_acorex_corpus(sys.argv[1])

    print(f"Loaded {len(audio_files)} audio files.")
    print(f"Corpus values file count: {len(corpus_values)}")
    for i, item in enumerate(corpus_values):
        print(f"Corpus values file {i} (segment, descriptor) count: {item.shape}")

main()
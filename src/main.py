import argparse
from os import system, path, remove

from pydub import AudioSegment as aus
from functools import reduce
from epub_reader.epub_reader import EpubParser
from util.sequential_uuid import SequentialID
from tts.tts_api import TextToSpeechClient

def clear():
    system('clear')


def delete_files(files):
    for file_name in files:
        remove(file_name)
        print(f'removed: {file_name}')


def main():
    parser = argparse.ArgumentParser(description='epub TTS')
    parser.add_argument('path', type=str, help='path to epub file')
    parser.add_argument('--output', type=str, help='output path')
    args = parser.parse_args()
    path_to_epub = args.path
    result_path = args.output
    formatted_text_path = "./output/texts/tmp.txt"
    audio_output_skeleton = './output/audio/tmp'
    convert_epub_to_audio(audio_output_skeleton, formatted_text_path, path_to_epub, result_path)


def convert_epub_to_audio(audio_output_skeleton, formatted_text_path, path_to_epub, result_path):
    EpubParser(path_to_epub).write_to_file(formatted_text_path)
    tts = TextToSpeechClient()
    id = SequentialID(audio_output_skeleton)
    sounds_and_path = []
    with open(formatted_text_path) as file_pointer:
        for line in file_pointer:
            save_line(id, line, sounds_and_path, tts)
    sounds, paths = zip(*sounds_and_path)
    combined_sounds = reduce(lambda combined, sound: combined + sound, sounds)
    output_dir = result_path if result_path else './output/combined_audio'
    output_path = path.join(output_dir, 'out.mp3')
    export_sounds(combined_sounds, output_path)
    delete_files(paths)


def save_line(id, line, sounds_and_path, tts):
    file = id.generate_name() + '.wav'
    tts.set_output_file(file)
    tts.save(line)
    print(f'saved:\n{line}')
    sound_ = aus.from_file(file, format='wav')
    sounds_and_path.append((sound_, file))


def export_sounds(combined_sounds, output_path : str):
    combined_sounds.export(output_path, format="mp3")


if __name__ == '__main__':
    main()

import os

from src.audio_player.audio_player import AudioPlayer, InvalidOSException
from src.epub_reader.epub_reader import EpubParser
from src.tts.tts_api import TextToSpeechClient
import argparse
from multiprocessing import Pool, cpu_count, Value
from threading import Thread
from queue import PriorityQueue
from time import sleep


COUNTER = Value('i', 0)
queue = PriorityQueue()

def get_file_name():
    global COUNTER
    with COUNTER.get_lock():
        COUNTER.value += 1
        return '../output/tmp__' + str(COUNTER.value) + '.wav'


def play_line(line: str, priority: int) -> tuple[int, str, str]:
    try:
        print("executing play_line")
        output_file_name = get_file_name()
        tts = TextToSpeechClient(output_file=output_file_name)
        tts.save(line)
        return priority, line, output_file_name
    except Exception as e:
        print(f"Exception in play_line: {e}")
        raise


def place_queue(res : tuple[int, str, str]):
    priority, line, output_file_name = res
    queue.put((priority, line, output_file_name))


def clear():
    os.system('cls')


def play_audio(queue: PriorityQueue):

    audio_player = AudioPlayer()
    while True:
        # print("busy waiting")
        if not queue.empty():
            _, sentence, audio_file = queue.get()
            print(sentence)
            audio_player.play(audio_file)
            os.remove(audio_file)
            clear()
        else:
            sleep(0.1)


def main():
    # parser = argparse.ArgumentParser(description='epub TTS')
    # parser.add_argument('path', type=str, help='path to epub file')
    # args = parser.parse_args()
    # path = args.path
    # path = '../inputs/lgtcm.epub'
    output_text = '../output/rm.txt'
    # EpubParser(path).write_to_file(output_text)
    with open(output_text) as file_pointer:
        print(f"cpu_count: {cpu_count()}")
        with Pool(cpu_count() // 2) as thread_pool:
            for i, line in enumerate(file_pointer):
                res = thread_pool.apply_async(play_line, args=(line, i), callback=place_queue)
                try:
                    res.get(timeout=5)  # get the result of play_line
                except Exception as e:
                    continue
    audio_thread = Thread(target=play_audio, args=(queue,))
    audio_thread.start()
    thread_pool.close()
    thread_pool.join()
    # audio_thread.join()


if __name__ == '__main__':
    main()

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
    print("executing play_line")
    output_file_name = get_file_name()
    tts = TextToSpeechClient(output_file=output_file_name)
    tts.save(line)
    return priority, line, output_file_name


def place_queue(res : tuple[int, str, str]):
    priority, line, output_file_name = res
    with queue.mutex:
        if not queue.full():
            queue.put((priority, line, output_file_name))


def clear():
    os.system('cls')


def play_audio(queue: PriorityQueue, num_lines : int):

    audio_player = AudioPlayer()
    i = 0
    while i < num_lines:
        # print("busy waiting")
        if not queue.empty() and queue[0] == i:
            with queue.mutex:
                if not queue.full():
                    _, sentence, audio_file = queue.get()
                    print(sentence)
                    audio_player.play(audio_file)
                    os.remove(audio_file)
                    clear()
                    i += 1



def main():
    # parser = argparse.ArgumentParser(description='epub TTS')
    # parser.add_argument('path', type=str, help='path to epub file')
    # args = parser.parse_args()
    # path = args.path
    # path = '../inputs/lgtcm.epub'
    output_path = '../output/texts/simple.txt'
    # EpubParser(path).write_to_file(output_path)
    with open(output_path) as file_pointer:
        print(f"cpu_count: {cpu_count()}")
        lines = file_pointer.readlines()
        num_lines = len(lines)
        file_pointer.seek(0)
        promises = []
        with Pool(cpu_count()) as thread_pool:
            for i, line in enumerate(file_pointer):
                print(f'schedule thread {i}')
                res = thread_pool.apply_async(play_line, args=(line, i), callback=place_queue)
                promises.append(res)
            audio_thread = Thread(target=play_audio, args=(queue,num_lines,))
            audio_thread.start()
            thread_pool.close()
            print('closed thread pool')
            print('main thread blocked until thread_pool finishes')
            for promise in promises:
                promise.get()
            thread_pool.join()


if __name__ == '__main__':
    main()

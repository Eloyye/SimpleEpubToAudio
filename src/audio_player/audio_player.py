import contextlib
import os
import wave
from enum import Enum
from math import ceil


class OperatingSystem(Enum):
    APPLE = 0
    LINUX = 1
    WINDOWS = 2


class InvalidOSException(Exception):
    pass


def resolve_OS(os_str_: str) -> OperatingSystem:
    os_str = os_str_.lower()
    if os_str == 'apple' or os_str == 'macos' or os_str == 'mac':
        return OperatingSystem.APPLE
    elif os_str == 'linux' or os_str == 'linuxos':
        return OperatingSystem.APPLE
    elif os_str == 'windows' or os_str == 'windowsos':
        return OperatingSystem.WINDOWS
    else:
        raise InvalidOSException(f"{os_str_} is not a valid/supported operating system")


def is_wav_file(file_path):
    if len(file_path) < 5:
        return False
    else:
        file_ext = file_path[len(file_path) - 4:]
        return file_ext == '.wav'


class AudioPlayer:
    def __init__(self, operating_system="apple"):
        os_ = resolve_OS(operating_system)
        if os_ == OperatingSystem.APPLE:
            self.prog = 'afplay'
        elif os_ == OperatingSystem.LINUX:
            self.prog = 'mpg123'
        else:
            self.prog = 'fmedia'

    # blocks current thread and executes program
    def play(self, file_path: str) -> None:
        res = " ".join([self.prog, file_path])
        os.system(res)

    #     get the duration of the file path in seconds
    def get_duration(self, file_path: str) -> int:
        if not is_wav_file(file_path):
            raise Exception('not a .wav file')
        with contextlib.closing(wave.open(file_path, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            return ceil(duration)

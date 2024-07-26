# !/usr/bin/python

import os
import string
import sys
import threading
from ctypes import windll
from typing import List
from pyuac import main_requires_admin

from modules.img_plugin import png_to_txt, jpg_to_txt
from modules.txt import read_file as read_txt
from modules.xlsx import read_file as read_xlsx
from modules.pptx import read_file as read_pptx
from modules.doc import read_file as read_docx
from modules.pdf import read_file as read_pdf


def get_drives() -> List[str]:
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1

    return drives


def process_file(full_path: str, substring: str) -> None:
    try:
        extension = '.' + full_path.split('.')[-1]

        match extension:
            case '.txt':
                full_text = read_txt(full_path)
            case '.xlsx':
                full_text = read_xlsx(full_path)
            case '.pptx':
                full_text = read_pptx(full_path)
            case '.jpg':
                full_text = jpg_to_txt(full_path)
            case '.png':
                full_text = png_to_txt(full_path)
            case '.docx':
                full_text = read_docx(full_path)
            case '.pdf':
                full_text = read_pdf(full_path)
            case _:
                return

        if substring in full_text:
            print(full_path)

    except (UnicodeDecodeError, PermissionError):
        pass


def search_in_folder(start_folder: str, substring: str) -> None:
    for root, dirs, files in os.walk(start_folder):
        for file in files:
            full_path = os.path.join(root, file)
            process_file(full_path, substring)


class DriveThread(threading.Thread):
    letter: str
    substring: str

    def __init__(self, letter: str, substring: str) -> None:
        threading.Thread.__init__(self)
        self.letter = letter
        self.substring = substring

    def run(self):
        search_in_folder(self.letter, self.substring)


threads: List[DriveThread] = []


@main_requires_admin
def main(substring: str, folder: str | None = None) -> None:
    if folder is None:
        for drive in get_drives():
            thread = DriveThread(f"{drive}:/", substring)
            thread.start()

            threads.append(thread)

        for thread in threads:
            thread.join()
    else:
        search_in_folder(folder, substring)


if __name__ == '__main__':
    arg: str = sys.argv[1] if len(sys.argv) > 1 else 'test'
    start_folder: str | None = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        main(arg, start_folder)
    except RuntimeError as e:
        pass

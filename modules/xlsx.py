import zipfile
import shutil
import tempfile
from os import listdir
from os.path import isdir

from modules.img_plugin import png_to_txt, jpg_to_txt


def read_file(xlsx_path: str) -> str:
    lines: list[str]
    with zipfile.ZipFile(xlsx_path, "r") as file_archive:
        temp_dir = tempfile.mktemp()
        file_archive.extractall(temp_dir)
        lines = _get_from_shared_strings(f"{temp_dir}\\xl")
        lines += _get_from_worksheets(f"{temp_dir}\\xl\\worksheets")
        if isdir(f"{temp_dir}\\xl\\media"):
            lines += _get_from_images(f"{temp_dir}\\xl\\media")
        if isdir(f"{temp_dir}\\xl\\charts"):
            lines += _get_from_charts(f"{temp_dir}\\xl\\charts")

    shutil.rmtree(temp_dir)
    return '\n'.join(lines)


def _get_from_images(path: str) -> list[str]:
    text = []
    for filename in listdir(path):
        if filename.endswith(".png"):
            text.append(png_to_txt(f"{path}\\{filename}"))
        elif filename.endswith(".jpg"):
            text.append(jpg_to_txt(f"{path}\\{filename}"))
    return text


def _get_from_shared_strings(path: str) -> list[str]:
    with open(f"{path}/sharedStrings.xml", "r") as file_strings:
        shared_strings_xml = file_strings.readlines()[1]
        lines = shared_strings_xml.split("<si><t>")[1:]
        lines[-1] = lines[-1].removesuffix("</sst>")
        lines = [line.removesuffix("</t></si>") for line in lines]
        return lines


def _get_from_worksheet(worksheet_name: str) -> list[str]:
    with open(worksheet_name, "r") as file_strings:
        worksheet_xml = file_strings.readlines()[1]
        lines = worksheet_xml.split("<v>")
        lines = [line.split("<", 1)[0] for line in lines]
        return [line if line != "\n" else "" for line in lines]


def _get_from_worksheets(path: str) -> list[str]:
    lines = []
    for filename in listdir(path):
        if filename.endswith(".xml"):
            lines += _get_from_worksheet(f"{path}/{filename}")
    return lines


def _get_from_charts(path: str) -> list[str]:
    lines = []
    for filename in listdir(path):
        if filename.startswith("chart"):
            lines += _get_from_chart(f"{path}/{filename}")
    return lines


def _get_from_chart(chart_name: str) -> list[str]:
    with open(chart_name, "r") as file_chart:
        xml_chart = file_chart.readlines()[1]
        lines = xml_chart.split("<a:t>")
        lines = [line.split("</a:t>")[0] for line in lines]
        return lines[1:]


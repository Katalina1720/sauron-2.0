# Sauron-2.0

## Проект для студкемпа Яндекса по разработке ПО.

Необходимо разработать консольную утилиту, которая
будет:

Работать для отдельного файла и рекурсивно обходить
директории в поисках файлов различных форматов
(поведение управляется параметрами)
В каждом файле она будет осуществлять поиск по ключевым
словам (параметр keyword) - одному или нескольким
принимая во внимание структуру файла.

Утилита должна быть расширяемой и поддерживать плагины
для различных форматов данных. Например, модуль OCR
для работы с PDF со скриншотами и фотографиями. Или
модуль для расбора сжатых файлов.

## Добавление модулей

Для того, чтобы написать модуль для расширения `.z`, нужно создать скрипт `z.py` в папке modules и создать там
функцию `read_file(filename)`, которая вернет текстовое содержимое файла. Пример работы с расширением `.txt`:

modules/txt.py

```python
def read_file(file: str) -> str:
    with open(file) as f:
        return f.read()
```
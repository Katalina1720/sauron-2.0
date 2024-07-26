def read_file(file: str) -> str:
    try:
        with open(file, encoding='utf8') as f:
            return f.read()
    except:
        return ''

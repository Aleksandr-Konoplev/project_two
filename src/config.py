from configparser import ConfigParser

def config(filename: str, section: str = 'postgresql'):
    parser = ConfigParser()
    with open(filename, encoding='cp1251') as f:
        parser.read_file(f)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1].strip()  # удаляем лишние пробелы
    else:
        raise Exception(f'Section {section} not found in the {filename} file')

    return db


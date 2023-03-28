import conllu
import os


def open_tb(path: str) -> conllu.SentenceList:
    with open(path) as file:
        tb = conllu.parse(file.read())
    return tb


def get_map(map_char: str) -> dict:
    with open(map_char) as file:
        lines = file.readlines()
    return {l.split('>')[0].strip(): l.split('>')[1].strip() for l in lines}


def convert_string(s: str, map_char: dict) -> str:
    for char in map_char:
        s = s.replace(char, map_char[char])
    return s


def change_chars(tb: conllu.SentenceList, map_char: dict) -> conllu.SentenceList:
    for sent in tb:
        sent.metadata['text'] = convert_string(sent.metadata['text'], map_char)
        for tok in sent:
            tok['form'] = convert_string(tok['form'], map_char)
            tok['lemma'] = convert_string(tok['lemma'], map_char)
    return tb


def convert_lang(lang_path: str, map_char: dict) -> None:
    files = [f for f in os.listdir(lang_path) if os.path.isfile(os.path.join(lang_path, f)) and f.endswith('.conllu')]
    for file in files:
        tb = open_tb(os.path.join(lang_path, file))
        tb = change_chars(tb, map_char)
        with open(os.path.join(lang_path, file.replace('.conllu', '_charconverted.conllu')), 'w') as dest:
            for sent in tb:
                dest.write(sent.serialize())


if __name__ == '__main__':
    map_char = get_map('./charmap.txt')
    for lang in ['./data/UD_German-GSD']:
        convert_lang(lang, map_char)

import conllu
import sys


def open_tb(path: str) -> conllu.SentenceList:
    """
    Opens a file at the given path and parses it as a CoNLL-U format file using the `conllu` library.

    Args:
        path (str): The path to the CoNLL-U file to open.

    Returns:
        A `conllu.SentenceList` object representing the parsed CoNLL-U file.
    """
    with open(path) as file:
        tb = conllu.parse(file.read())
    return tb


def get_map(map_char: str) -> dict:
    """
    Opens a file at the given path and returns a dictionary containing the character map.

    Args:
        path (str): The path to the file to open.

    Returns:
        A `dict` object representing the character map.
    """
    with open(map_char) as file:
        lines = file.readlines()
    return {l.split('>')[0].strip(): l.split('>')[1].strip() for l in lines}


def convert_string(s: str, map_char: dict) -> str:
    """
    Replaces characters in a string `s` with their corresponding replacements in a dictionary `map_char`.

    Args:
        s (str): The string to be converted.
        map_char (dict): A dictionary containing key-value pairs of characters to be replaced and their corresponding replacements.

    Returns:
        str: The converted string.
    """
    for char in map_char:
        s = s.replace(char, map_char[char])
    return s


def change_chars(tb: conllu.SentenceList, map_char: dict) -> conllu.SentenceList:
    """
    Replaces characters in the text and token fields of each sentence in a conllu SentenceList `tb` with their corresponding
    replacements in a dictionary `map_char`.

    Args:
        tb (conllu.SentenceList): The SentenceList to be modified.
        map_char (dict): A dictionary containing key-value pairs of characters to be replaced and their corresponding replacements.

    Returns:
        conllu.SentenceList: The modified SentenceList.
    """
    for sent in tb:
        sent.metadata['text'] = convert_string(sent.metadata['text'], map_char)
        for tok in sent:
            tok['form'] = convert_string(tok['form'], map_char)
            tok['lemma'] = convert_string(tok['lemma'], map_char)
    return tb


if __name__ == '__main__':
    map_char = get_map('./charmap.txt')
    source = sys.argv[1]
    dest = sys.argv[2]

    # open the treebank
    tb = open_tb(source)

    # convert characters
    converted = change_chars(tb, map_char)

    # output
    with open(dest, 'w') as file:
        for sent in converted:
            file.write(sent.serialize())

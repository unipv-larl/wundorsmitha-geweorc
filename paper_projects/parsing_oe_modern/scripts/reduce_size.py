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


def reduce_size(tb: conllu.SentenceList, size: int) -> list:
    """
    Reduces the size of a CoNLL-U format file by reducing it to a smaller part containing a maximum of `size` tokens.

    Args:
        tb (conllu.SentenceList): A `conllu.SentenceList` object representing the CoNLL-U file to reduce in size.
        size (int): The maximum number of tokens to include in the smaller CoNLL-U file.

    Returns:
        A list of `conllu.SentenceList` objects representing the smaller CoNLL-U files.
    """
    count = 0
    sentlist = []
    for sent in tb:
        sentlist.append(sent)
        count += len(sent)
        if count > size:
            print(count)
            return sentlist
    print(count)
    return sentlist


def main(source: str, size: int, dest: str) -> None:
    """
    Reduces a CoNLL-U format file into a smaller part containing a maximum of `size` tokens and writes it to a separate file.

    Args:
        source (str): The path to the input CoNLL-U file.
        size (int): The maximum number of tokens to include in the reduced CoNLL-U file.
        dest (str): The path in which to write the output file.

    Returns:
        None.
    """
    tb = open_tb(source)
    reduced = reduce_size(tb, size)
    with open(dest, 'w') as file:
        for sent in reduced:
            file.write(sent.serialize())


if __name__ == '__main__':
    source = sys.argv[1]
    size = int(sys.argv[2])
    dest = sys.argv[3]
    main(source, size, dest)

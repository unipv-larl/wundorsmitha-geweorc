import conllu
import sys
from typing import Union


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


def export_tb(sentlist: Union[list, conllu.SentenceList], dest: str) -> None:
    with open(dest, 'w') as file:
        for sent in sentlist:
            file.write(sent.serialize())


def correct_tok(token: conllu.Token) -> conllu.Token:
    """
    Corrects the deprel of a token given certain conditions.

    Args:
        token (conllu.Token): The CoNLL-U token.

    Returns:
        A `conllu.Token` object representing the corrected CoNLL-U token.
    """
    # if the token is 'ne' the deprel must be 'cc' or 'advmod:neg' according to the upos of the token
    if token['form'] == 'ne':
        if token['upos'] == 'CCONJ':
            token['deprel'] = 'cc'
        elif token['upos'] == 'PART':
            token['deprel'] = 'advmod:neg'
        else:
            pass
    # if the xpos if a token startswith 'MD', then the deprel must be 'aux'
    elif token['xpos'].startswith('MD'):
        token['deprel'] = 'aux'
    # if the xpos if a token is 'ADV^L', then the deprel must be 'advmod:lmod'
    elif token['xpos'] == 'ADV^L':
        token['deprel'] = 'advmod:lmod'
    # if the xpos if a token is 'ADV^T', then the deprel must be 'advmod:tmod'
    elif token['xpos'] == 'ADV^T':
        token['deprel'] = 'advmod:tmod'
    else:
        pass
    return token


if __name__ == '__main__':
    source = sys.argv[1]
    dest = sys.argv[2]

    tb = open_tb(source)

    for sent in tb:
        for tok in sent:
            tok = correct_tok(tok)

    export_tb(tb, dest)

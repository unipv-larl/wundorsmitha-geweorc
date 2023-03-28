import conllu
import sys
from typing import Union


def open_tb(path: str) -> conllu.SentenceList:
    with open(path) as file:
        tb = conllu.parse(file.read())
    return tb


def export_set(sentlist: Union[list, conllu.SentenceList], dest: str, masked=False) -> None:
    with open(dest, 'w') as file:
        for sent in sentlist:
            if masked:
                for tok in sent:
                    for field in tok:
                        if field not in ['id', 'form']:
                            tok[field] = None
            file.write(sent.serialize())
    return None


def correct_tok(token: conllu.Token) -> conllu.Token:
    if token['form'] == 'ne':
        if token['upos'] == 'CCONJ':
            token['deprel'] = 'cc'
        elif token['upos'] == 'PART':
            token['deprel'] = 'advmod:neg'
        else:
            pass
    elif token['xpos'].startswith('MD'):
        token['deprel'] = 'aux'
    elif token['xpos'] == 'ADV^L':
        token['deprel'] = 'advmod:lmod'
    elif token['xpos'] == 'ADV^T':
        token['deprel'] = 'advmod:tmod'
    else:
        pass
    return token


if __name__ == '__main__':
    model = sys.argv[1]

    tb = open_tb(f'./parsed/{model}/out.conllu')

    for sent in tb:
        for tok in sent:
            tok = correct_tok(tok)
    
    export_set(tb, f'./parsed/{model}/out_corrected.conllu')

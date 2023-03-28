import conllu
import os


def open_tb(path: str) -> conllu.SentenceList:
    with open(path) as file:
        tb = conllu.parse(file.read())
    return tb


def reduce60(tb: conllu.SentenceList) -> list:
    count = 0
    sentlist = []
    for sent in tb:
        sentlist.append(sent)
        count += len(sent)
        if count > 60000:
            print(count)
            return sentlist
    print(count)
    return sentlist


def reduce_lang(lang_path: str) -> None:
    files = [f for f in os.listdir(lang_path) if os.path.isfile(os.path.join(lang_path, f)) and f.endswith('train.conllu')]
    for file in files:
        print(file)
        tb = open_tb(os.path.join(lang_path, file))
        tb = reduce60(tb)
        with open(os.path.join(lang_path, file.replace('.conllu', '_reduced.conllu')), 'w') as dest:
            for sent in tb:
                dest.write(sent.serialize())


if __name__ == '__main__':
    for lang in ['./data/UD_German-GSD', './data/UD_Icelandic-GC', './data/UD_Swedish-Talbanken']:
        print(lang)
        reduce_lang(lang)

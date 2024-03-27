import conllu


def get_tb(filepath):
    with open(filepath) as file:
        tb = conllu.parse(file.read())
    return tb


def find_root(sent):
    for tok in sent:
        if tok['deprel'] == 'root':
            return tok
    return None


if __name__ == '__main__':
    gold = get_tb('gold.conllu')
    test = get_tb('test.conllu')

    missing = 0
    correct = 0
    wrong = 0
    missing_tb = []
    correct_tb = []
    wrong_tb = []
    for sent in test:
        root = find_root(sent)
        if not root:
            missing += 1
            missing_tb.append(sent)
        else:
            for gold_sent in gold:
                if gold_sent.metadata['sent_id'] == sent.metadata['sent_id']:
                    gold_root = find_root(gold_sent)
                    if root['id'] == gold_root['id']:
                        correct += 1
                    else:
                        wrong += 1
                        wrong_tb.append(sent)
                    break
    print(correct, wrong, missing)
    with open('missing_tb.conllu', 'w') as file_miss:
        for sent in missing_tb:
            file_miss.write(sent.serialize())
    with open('wrong_tb.conllu', 'w') as file_wrong:
        for sent in wrong_tb:
            file_wrong.write(sent.serialize())

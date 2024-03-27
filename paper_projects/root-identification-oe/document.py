from sentence import Sentence
from phrase import Phrase


class Document(list):
    def __init__(self, iterable=[], **kwargs):
        super().__init__(elem for elem in iterable if
                         isinstance(elem, Sentence))
        self.add_attrs(**kwargs)
        for elem in self:
            elem.add_attrs(parent=id(self))

    def __str__(self):
        return '[' + ', '.join(str(x) for x in self) + ']'

    def add_attrs(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def get_rules(self, tokens=False):
        rules = {}
        for sent in self:
            sent_rules = sent.get_rules(tokens)
            for key in sent_rules:
                try:
                    rules[key] |= sent_rules[key]
                except KeyError:
                    rules[key] = sent_rules[key].copy()
        return rules

    def to_conllu(self, dest=None):
        conllu = ''
        for sentence in self:
            conllu += sentence.to_conllu()
        if dest:
            with open(dest, 'w') as file:
                file.write(conllu)
        return conllu

    def join_sentences(self, file_join):
        groups = []
        with open(file_join) as file:
            for line in file.readlines():
                group = tuple([sent.strip() for sent in line.split('+')])
                groups.append(group)
        remove_sents = []
        add_sents = []
        for sent in self:
            for group in groups:
                if sent.sent_id == group[0]:
                    # get the sentences of the group
                    target_sents = [sent]
                    remove_sents.append(sent)
                    for sent_in_group in group[1:]:
                        for other_sent in self:
                            if other_sent.sent_id == sent_in_group:
                                target_sents.append(other_sent)
                                remove_sents.append(other_sent)
                                break
                    # peal the sentences
                    pulp = []
                    for target in target_sents:
                        conjp = []
                        for element in target.peal():
                            if target_sents.index(target) == 0:
                                pulp.append(element)
                            else:
                                conjp.append(element)
                                pulp.append(Phrase('CONJP', conjp))
                    # add the content to a phrase IP-MAT
                    ip_mat = Phrase('IP-MAT', pulp)
                    # TODO remove the sentences from Document (self)
                    # TODO store the IP-MAT into a sentence joining IDs
                    new_sentence = Sentence(group[0], [ip_mat])
                    add_sents.append(new_sentence)
                    # TODO include the new sentence in the Document (self)
        new_doc = [sent for sent in self if sent not in remove_sents] + add_sents
        return Document(new_doc)

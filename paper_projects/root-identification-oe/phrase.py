from token import Token


class Phrase(list):
    def __init__(self, tag, iterable=[], **kwargs):
        super().__init__(elem for elem in iterable if isinstance(elem, Token)
                         or isinstance(elem, Phrase))
        self.tag = tag
        self.add_attrs(**kwargs)
        for elem in self:
            elem.add_attrs(parent=id(self))

    def __str__(self):
        return f'<Phrase ({self.tag}, [' + ', '.join([str(x) for x in self]) + '])>'

    def __hash__(self):
        return hash(id(self))

    def add_attrs(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def render_tree(self, indent=0):
        for item in self:
            if isinstance(item, Phrase):
                print("  " * indent + item.tag)
                item.render_tree(indent + 1)
            else:
                print("  " * indent + str(item))

    def get_isolated(self, exclude_punct=True):
        if exclude_punct:
            return [elem for elem in self if isinstance(elem, Token) and
                    elem.upos != 'PUNCT']
        else:
            return [elem for elem in self if isinstance(elem, Token)]

    def infinitive_dep(self, parent):
        if self.tag.startswith('IP-INF'):
            parent.add_attrs(deprel='root')
            vb = [tok for tok in self if isinstance(tok, Token) and tok.tag == 'VB^D']
            if len(vb) == 1:
                vb[0].add_attrs(deprel='xcomp', head=id(parent))
                to = [tok for tok in self if isinstance(tok, Token) and tok.tag == 'TO']
                if len(to) == 1:
                    to[0].add_attrs(deprel='mark', head=id(vb[0]))
            return True
        return False

    def get_nom_parent(self):
        if self.tag.startswith('NP'):
            nouns = [n for n in self if isinstance(n, Token) and n.upos == 'NOUN' and n.feats['Case'] == 'Nom']
            if len(nouns) == 1:
                return nouns[0]
            elif not nouns:
                np_phrases = [np for np in self if isinstance(np, Phrase) and np.tag == 'NP-NOM']
                if len(np_phrases) == 1:
                    return np_phrases[0].get_nom_parent()
                return None
            return None
        elif self.tag.startswith('ADJP'):
            adjs = [a for a in self if isinstance(a, Token) and a.upos == 'ADJ' and a.feats['Case'] == 'Nom']
            if len(adjs) == 1:
                return adjs[0]
            elif not adjs:
                adjp_phrases = [adjp for adjp in self if isinstance(adjp, Phrase) and adjp.tag == 'ADJP-NOM']
                if len(adjp_phrases) == 1:
                    return adjp_phrases[0].get_nom_parent()
                return None
            return None

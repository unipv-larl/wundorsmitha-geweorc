import ctypes


class TagError(Exception):
    def __init__(self, tag):
        self.tag = tag
        self.message = f"Invalid tag: {tag}"
        super().__init__(self.message)


def get_from_id(memory_id):
    return ctypes.cast(memory_id, ctypes.py_object).value


class Token:
    def __init__(self, tag: str, form: str, charmap: dict,
                 pos_table: dict, **kwargs):
        self.tag = tag[:]
        self.form = form
        for char in charmap:
            self.form = self.form.replace(char, charmap[char])

        kw = {}
        if '+' in tag:
            tag = tag.split('+')[1]
            if self.tag.startswith('NEG'):
                kw = {'Polarity': 'Neg'}
        try:
            morpho_feats = pos_table[tag]
            morpho_feats['feats'] = DualDict(morpho_feats['feats'], **kw)
        except KeyError:
            if tag == 'ID':
                morpho_feats = {}
            else:
                raise TagError(tag)

        self.add_attrs(**morpho_feats)
        self.add_attrs(**kwargs)

    def __str__(self):
        return f'<Token ({self.tag}, {self.form})>'

    def add_attrs(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __hash__(self):
        return hash(id(self))

    def get_sent(self):
        parent = get_from_id(self.parent)
        while type(parent).__name__ != 'Sentence':
            parent = get_from_id(parent.parent)
        return parent

    def next_tok(self):
        sent = self.get_sent()
        tokens = sent.get_tokens()
        try:
            i = tokens.index(self)
            return tokens[i + 1]
        except IndexError:
            return None

    def prev_tok(self):
        sent = self.get_sent()
        tokens = sent.get_tokens()
        try:
            i = tokens.index(self)
            return tokens[i - 1]
        except IndexError:
            return None

    def to_conllu(self, token_id, head=None):
        try:
            deprel = self.deprel
        except AttributeError:
            deprel = '_'
        if not head:
            head = '_'
        line = f'{token_id}\t{self.form}\t_\t{self.upos}\t{self.tag}\t{str(self.feats)}\t{head}\t{deprel}\t_\t_\n'
        return line


class DualDict(dict):
    def __init__(self, value=None, **kwargs):
        super().__init__()
        if not value:
            pass
        elif isinstance(value, str):
            if value == '_':
                pass
            else:
                pairs = value.split('|')
                for pair in pairs:
                    kv = pair.split('=')
                    self[kv[0]] = kv[1]
        elif isinstance(value, dict):
            for k in value:
                self[k] = value[k]
        else:
            pass
        for k in kwargs:
            self[k] = kwargs[k]

    def __str__(self):
        if not self:
            return '_'
        kv = [f'{k}={self[k]}' for k in self]
        kv.sort()
        return '|'.join(kv)

from phrase import Phrase
from token import Token, get_from_id
import dependencies


class Sentence(list):
    def __init__(self, sent_id: str, iterable=[], **kwargs):
        super().__init__(elem for elem in iterable if isinstance(elem, Phrase))
        self.sent_id = sent_id
        self.add_attrs(**kwargs)
        for elem in self:
            elem.add_attrs(parent=id(self))

    def __str__(self):
        return f'<Sentence ({self.sent_id}, [' + ', '.join([str(x) for x in self]) + '])>'

    def __hash__(self):
        return hash(id(self))

    def add_attrs(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def get_levels(self):
        levels = {}
        while True:
            if not levels:
                lev = [phrase for phrase in self]
                if lev:
                    levels[1] = lev
                else:
                    return levels
            else:
                lev = []
                for phrase in levels[len(levels)]:
                    if isinstance(phrase, Phrase):
                        lev += [elem for elem in phrase]
                    if lev:
                        levels[len(levels) + 1] = lev
                    else:
                        return levels

    def get_rules(self, tokens=False):
        levels = self.get_levels()
        rules = {}
        if levels:
            for i in range(1, len(levels) + 1):
                for elem in levels[i]:
                    if isinstance(elem, Phrase):
                        try:
                            if tokens:
                                all_tok = True
                                for child in elem:
                                    if not isinstance(child, Token):
                                        all_tok = False
                                    if all_tok:
                                        rules[elem.tag].add(tuple([child.tag for child in elem]))
                            else:
                                rules[elem.tag].add(tuple([child.tag for child in elem]))
                        except KeyError:
                            if tokens:
                                all_tok = True
                                for child in elem:
                                    if not isinstance(child, Token):
                                        all_tok = False
                                    if all_tok:
                                        rules[elem.tag] = {tuple([child.tag for child in elem])}
                            else:
                                rules[elem.tag] = {tuple([child.tag for child in elem])}
        return rules

    def get_tokens(self):
        tokens = []
        visited = set()
        stack = [self[0]]

        while stack:
            node = stack.pop()

            if node not in visited:
                visited.add(node)
                if isinstance(node, Token):
                    tokens.append(node)
                else:
                    stack.extend(child for child in node if child not in visited)
        tokens.reverse()
        return tokens

    def to_conllu(self):
        text = '# text ='
        sent_id = '# sent_id = ' + self.sent_id
        conllu = ''
        tokens = self.get_tokens()
        token_id = 0
        for tok in tokens:
            token_id += 1
            try:
                if hasattr(tok, 'head'):
                    head = str(tokens.index(get_from_id(tok.head)) + 1)
                elif tok.deprel == 'root':
                    head = '0'
                else:
                    head = None
            except AttributeError:
                head = None
            conllu += tok.to_conllu(token_id, head)
            text += ' ' + tok.form
        return sent_id + '\n' + text + '\n' + conllu + '\n'

    def render_tree(self, indent=0):
        print(self.sent_id, ': ', self.get_text(), sep='')
        print('isolated: ', ', '.join(str(tok) for tok in self.get_isolated()), sep='')
        for item in self:
            if isinstance(item, Phrase):
                print("  " * indent + item.tag)
                item.render_tree(indent + 1)
            else:
                print("  " * indent + str(item))

    def get_isolated(self, exclude_punct=True):
        if exclude_punct:
            return [elem for elem in self[0] if isinstance(elem, Token) and
                    elem.upos != 'PUNCT']
        else:
            return [elem for elem in self[0] if isinstance(elem, Token)]

    def find_root(self):
        isolated = self.get_isolated()
        if not isolated:
            if self.root_ipmat0():
                return True
            if self.cp_que():
                return True
        else:
            rules = ['vb', 'be_inf', 'be_copula', 'have', 'be_root', 'md']
            for rule in rules:
                func = getattr(dependencies, rule)
                if dependencies.trigger(func, isolated):
                    return True
        if self.cp_que():
            return True
        if self.coord_vb():
            return True
        return False

    def root_ipmat0(self):
        candidates = [p for p in self[0] if isinstance(p, Phrase) and p.tag in ['IP-MAT-0']]
        if len(candidates) == 1:
            ipmat = candidates[0]
            isolated = ipmat.get_isolated()
            rules = ['vb', 'be_inf', 'be_copula', 'have', 'be_root', 'md']
            for rule in rules:
                func = getattr(dependencies, rule)
                if dependencies.trigger(func, isolated):
                    return True
        return False

    def cp_que(self):
        first_level = [p for p in self if isinstance(p, Phrase) and p.tag.startswith('CP-QUE')]
        try:
            candidates = [p for p in first_level[0] if isinstance(p, Phrase) and p.tag in ['IP-SUB', 'IP-SUB-SPE']]
            if len(candidates) == 1:
                ipsub = candidates[0]
                isolated = ipsub.get_isolated()
                rules = ['vb', 'be_inf', 'be_copula', 'have', 'be_root', 'md']
                for rule in rules:
                    func = getattr(dependencies, rule)
                    if dependencies.trigger(func, isolated):
                        return True
        except IndexError:
            pass
        return False

    def coord_vb(self):
        vb_coord = [p for p in self[0] if isinstance(p, Phrase) and p.tag.startswith('VB')]
        if len(vb_coord) == 1:
            vbs = [tok for tok in vb_coord[0] if isinstance(tok, Token) and tok.tag.startswith('VB')]
            try:
                root = vbs[0]
                root.add_attrs(deprel='root')
                return True
            except IndexError:
                pass
        return False

    def get_root(self):
        for tok in self.get_tokens():
            try:
                if tok.deprel == 'root':
                    return tok
            except AttributeError:
                pass
        return None

    def get_text(self):
        text = ''
        for tok in self.get_tokens():
            if text:
                text += ' '
            text += tok.form
        return text

    def peal(self):
        return self[0]

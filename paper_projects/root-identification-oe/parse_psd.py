from document import Document
from sentence import Sentence
from phrase import Phrase
from token import Token, TagError


class ParserPSD:
    def __init__(self, psd_path, pos_table, charmap):
        # stores the content of the psd file into self.string
        with open(psd_path) as file:
            lines = [line.strip() for line in file.readlines() if not (line.strip().startswith('( (CODE') and line.strip().endswith('))'))]
            self.string = ' '.join(lines)

        with open(pos_table) as file:
            self.pos_table = {}
            for line in file.readlines()[1:]:
                fields = line.strip().split('\t')
                xpos = fields[0]
                upos = fields[1]
                try:
                    feats = fields[2]
                except IndexError:
                    feats = '_'
                self.pos_table[xpos] = {'upos': upos, 'feats': feats}

        with open(charmap) as file:
            self.charmap = {line.split('=')[0]: line.split('=')[1].strip() for line in file.readlines()}

        self.relevant_elements = []

    def get_elements(self):
        self.relevant_elements.clear()
        current = ''
        for char in self.string:
            if char == ' ':
                if current:
                    self.relevant_elements.append(current)
                    current = ''
            elif char == '(' or char == ')':
                if current:
                    self.relevant_elements.append(current)
                    current = ''
                self.relevant_elements.append(char)
            else:
                current += char
        if current:
            self.relevant_elements.append(current)

    def get_block_ind(self):
        start = 0
        end = 0
        i = -1
        is_open = False
        self.block_ind = []
        for elem in self.relevant_elements:
            i += 1
            if elem == '(':
                is_open = True
                start = i
            if elem == ')' and is_open:
                is_open = False
                end = i
                self.block_ind.append((start, end))

    def inside_blocks(self):
        for i in range(1, len(self.block_ind) + 1):
            start = self.block_ind[-i][0]
            end = self.block_ind[-i][1]
            self.elems2list(start, end)

    def elems2list(self, start, end):
        ins = self.relevant_elements[start + 1:end]
        if not ins:
            self.relevant_elements.pop(start)
            self.relevant_elements.pop(end)
        else:
            if isinstance(ins[0], str):
                if len(ins) == 2 and isinstance(ins[1], str) and ins[1] != '0':
                    try:
                        element = Token(ins[0], ins[1], self.charmap, self.pos_table)
                    except TagError:
                        element = None
                else:
                    element = Phrase(ins[0], ins[1:])
            elif isinstance(ins[0], Phrase):
                if ins[-1].tag == 'ID':
                    sent_id = ins.pop().form
                else:
                    sent_id = 'xxxx'
                element = Sentence(sent_id, ins)
            else:
                element = None
            for i in range(end, start-1, -1):
                self.relevant_elements.pop(i)
            if element:
                self.relevant_elements.insert(start, element)

    def get_document(self):
        self.get_elements()
        self.get_block_ind()
        while self.block_ind:
            self.inside_blocks()
            self.get_block_ind()
        return Document(self.relevant_elements)


if __name__ == '__main__':
    import sys
    treebank = sys.argv[1]
    parser = ParserPSD(treebank, 'pos_table.tsv', 'charmap.txt')
    doc = parser.get_document()
    joined_doc = doc.join_sentences('joined_sentences.txt')
    count = 0
    for sent in joined_doc:
        sent.find_root()
        if not sent.get_root():
            count += 1
            # sent.render_tree()
            # input()
    joined_doc.to_conllu(dest=sys.argv[1].replace('.psd', '.conllu'))
    print(f'sentences w/o root: {count}/{len(joined_doc)}')

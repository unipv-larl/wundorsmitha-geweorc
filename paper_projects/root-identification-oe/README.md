# root-dentification-oe

This is the repository containing the code for the paper
**From YCOE to UD: rule-based root identification in Old English**, submitted
to LREC-Coling 2024.

## Content of the repo

- test.psd: the treebank in the YCOE format
- gold.conllu: the gold conllu file annotated by the authors
- test.conllu: the test conllu file converted from test.psd
- joined_sentences.txt: the list of sentences that were joined during the
conversion process
- pos_table.tsv: a tsv file containig the conversion table from YCOE to UD
- charmap.txt: the combination of characters used in the YCOE treebank and the
correspondent character
- parse_psd.py: the main script used to convert the psd file to conllu and to
assign the roots
- *others*.py: modules imported in the main script


## Usage

```sh
python3 parse_psd.py test.psd
```

This command will take the test.psd file (the treebank in the original format)
and will produce a file called test.conllu assigning the roots to the sentences
using the rules described in the modules [`sentence.py`](sentence.py) and 
[`dependencies.py`](dependencies.py).

<div align="center">

# Using modern languages to parse ancient ones: a test on Old English

[![Workshop](https://img.shields.io/badge/workshop-SIGTYP%202023-blue)](https://sigtyp.github.io/ws2023-sigtyp.html)

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png

</div>

This repository contains the data and the scripts used for the study presented in the paper [*Using modern languages to parse ancient ones: a test on Old English*]() presented by Luca Brigada Villa and Martina Giarda at the [SIGTYP 2023 workshop](https://sigtyp.github.io/ws2023-sigtyp.html).

## Content of this repository

 * data: the treebanks used to train the models
 * models: the models analyzed in our paper
 * scripts: the scripts used to preprocess the training data

## Workflow

### Reducing the size of the support languages treebanks to 60k tokens

The script [reduce_size.py](scripts/reduce_size.py) reduces the size of a treebank to the desired number of tokens. Usage:

```sh
python3 reduce_size.py path/to/the/treebank size path/to/the/output
```

### Converting the characters in the support languages treebanks

The script [convert_chars.py](scripts/convert_chars.py) used in combination with the charmap in [charmap.txt](scripts/charmap.txt) takes as input a treebank file and converts the characters in the file to the correspondent character in the map. Usage:

```sh
python3 convert_chars.py path/to/the/treebank path/to/the/output
```

### Training the models

To train the models, we used [uuparser](https://github.com/UppsalaNLP/uuparser), a transition based dependency parser for Universal Dependencies that is able to train multilingual models. The isocode for Old English was not included in the isofile provided with the parser, then we used the [isofile](scripts/isofile.json) in the scripts folder.

#### Training monolingual models

```sh
uuparser --outdir path/to/modeldir --datadir data --include "isocode" --dynet-seed 13 --json-isos scripts/isofile.json --devfile data/oe/oe-ud-dev.conllu --dynet-mem 10000 --tbank-emb-size 0
```

#### Training multilingual models

```sh
uuparser --multiling --outdir path/to/modeldir --datadir data --include "isocode1 isocode2 isocoden" --dynet-seed 13 --json-isos scripts/isofile.json --devfile data/oe/oe-ud-dev.conllu --dynet-mem 10000 --tbank-emb-size 0
```

### Parsing OE data with the models

After training the models, we parsed OE test data using the option `--predict` of uuparser.

```sh
uuparser --predict --dynet-seed 13 --model barchybrid.model --modeldir path/to/modeldir --testfile data/oe/oe-ud-test.conllu --outdir path/to/outdir
```

### Cleaning the annotation

After parsing the OE test data, we correct the annotation of some dependency relations using the script [correct_deprels.py](scrpts/correct_deprels.py). Usage:

```sh
python3 correct_deprels.py path/to/treebank path/to/output
```

## Cite the paper

Luca Brigada Villa and Martina Giarda. 2023. [Using modern languages to parse ancient ones: a test on Old English](). In *Proceedings of the Fifth Workshop on Computational Typology and Multilingual NLP*, pages XX–YY, Dubrovnik, Croatia. Association for Computational Linguistics.

```bibtex
@inproceedings{brigada-villa-giarda-2023-using,
    title = "Using modern languages to parse ancient ones: a test on Old English",
    author = "Brigada Villa, Luca and
			Giarda, Martina",
    booktitle = "Proceedings of the Fifth Workshop on Computational Typology and Multilingual NLP",
    month = may,
    year = "2023",
    address = "Dubrovnik, Croatia",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.sigtyp-",
    doi = "",
    pages = "xx--yy",
    abstract = "",
}
```

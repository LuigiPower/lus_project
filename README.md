# Language Understanding Systems project

## Part 1

### Usage

Creation of a tool to tag concepts in sentences related to movies.

The tool's usage is simplified through a script that allows passing in parameters to each of the training steps:

```bash
usage:
    ./scripts/create_and_run.sh create_and_run.sh -e evalscript.pl -i input.txt [-f input.feats.txt] -t test.txt -b builddir -s tagger [-m method] [-o order] [-c number] [-n]

example:
    ./scripts/create_and_run.sh -i P1/data/NLSPARQL.train.data -f P1/data/NLSPARQL.train.feats.txt -t P1/data/NLSPARQL.test.data -s nofeats -b generated/nofeats -e P1/scripts/conlleval.pl -m witten_bell -o 3
```

### Folder structure

All the code is inside the "scripts" folder
The "generated" folder contains all manually run tests
The "all_tests" folder contains all tests run with different training parameters with the "run_all_tests.sh" script

Inside each test folder, a .result.txt file is present with the results of that specific test.



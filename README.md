# ArtBox

ArtBox is a tool set for handling multimedia files.

* Documentation: https://ggpedia.games
* License: BSD-3 Clause

## Features

TBD


## Troubleshoot

Before install artbox dependencies install the following packages

```bash
$ pip wheel --use-pep517 "playsound (==1.3.0)"
```

After installing with `poetry install`:

* Patch `pytube` (ref: https://github.com/pytube/pytube/issues/1773):
  `sed -i 's/(r"^\\w+\\W")/(r"^\w+\W")/' $CONDA_PREFIX/lib/python3.*/site-packages/pytube/cipher.py`
*

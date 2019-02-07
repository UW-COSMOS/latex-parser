### Setup
1. Clone this directory
2. pip install -r requirements.txt
3. cd katex
4. npm install
   
### Usage Example

```bash
python [path-to-this-repo]/variable_extractor.py --latex {a}_{b}
```
_Due to the limitation of the command line tool, please put an extra '\' to every existing '\'_
### Usage Description

```
Usage: variable_extractor.py [OPTIONS]

  Variable extractor that finds variables in the Latex code

Options:
  --latex TEXT  Source latex code to be parsed  [required]
  --help        Show this message and exit.
```

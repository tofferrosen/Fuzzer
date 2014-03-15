Fuzzer
======

The fabulous fuzzer project for software security:
http://yogi.se.rit.edu/~swen-331/projects/fuzzer/

Project Team:

CHRISTOFFER ROSEN			 <cbr4830@rit.edu>
ISIOMA NNODUM 				 <iun4534@rit.edu>
SAMANTHA SHANDROW 			 <ses6421@rit.edu>

## Installation
1. Clone this repository to an empty directory
2. Install all dependencies - we recommend using `pip`

## Dependencies
* Python 2.7
* requests (`pip install requests`)
* beautiful soup (`pip install beautifulsoup`)


## Example usage for discovery:

#### With Custom Authentication
`python fuzz.py discover http://127.0.0.1 --custom-auth=dvwa --common-words="Guessing/pageNames.txt"`
`python fuzz.py discover http://127.0.0.1 --custom-auth=bodgeit --common-words="Guessing/pageNames.txt"`

#### No Custom Authentication
`python fuzz.py discover http://127.0.0.1 --common-words="Guessing/pageNames.txt"`

## Example Usage for Test
`python fuzz.py test http://127.0.0.1 --common-words="Guessing/pageNames.txt" --vectors="FuzzVectors/sqlInjection.txt`

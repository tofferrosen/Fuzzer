Fuzzer
======

The fabulous fuzzer project for software security:
http://yogi.se.rit.edu/~swen-331/projects/fuzzer/

## Project Team:

* CHRISTOFFER ROSEN	<cbr4830@rit.edu>
* ISIOMA NNODUM <iun4534@rit.edu>
* SAMANTHA SHANDROW <ses6421@rit.edu>

## Installation
1. Clone this repository to an empty directory
2. Install all dependencies - we recommend using `pip`

## Project Setup
1. All input discovery functionality is in the discovery package.
2. All fuzzing/test functinality is in the fuzzing package. 
3. All resources/files used are in the Resources directory.

## Dependencies
* Python 2.7
* requests (`pip install requests`)
* beautiful soup (`pip install beautifulsoup`)


## Example usage for discovery:

#### With Custom Authentication
`python fuzz.py discover http://127.0.0.1 --custom-auth=dvwa --common-words="Resources/pageNames.txt"`
`python fuzz.py discover http://127.0.0.1 --custom-auth=bodgeit --common-words="Resources/pageNames.txt"`

#### No Custom Authentication
`python fuzz.py discover http://127.0.0.1 --common-words="Resources/pageNames.txt"`

## Example Usage for Test
`python fuzz.py test http://127.0.0.1 --common-words="resources/pageNames.txt" --vectors="resources/vectors.txt" --custom-auth=dvwa --sensitive="resources/sensitive.txt"`

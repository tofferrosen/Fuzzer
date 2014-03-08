"""
file: options.py
description: parsing options given in the command line interface
"""
from optparse import OptionParser

usage = "Usage: %prog [discover | test] url [OPTIONS]"
parser = OptionParser(usage=usage)

parser.add_option("--custom-auth", dest="app_to_auth", 
	help="Signal that the fuzzer should use hard-coded authentication for a \
	specific application (e.g. dvwa). Optional.", metavar="STRING" )

parser.add_option("--common-words", dest="common_words", 
	help="Newline-delimited file of common words to be used in page guessing \
	and input guessing. Required for discovery.", metavar="FILE")
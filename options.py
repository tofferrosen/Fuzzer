"""
file: options.py
description: parsing options given in the command line interface
"""
from optparse import OptionParser

usage = "Usage: %prog [discover | test] url [OPTIONS]"
parser = OptionParser(usage=usage)

# custom auth option
parser.add_option("--custom-auth", dest="app_to_auth", 
	help="Signal that the fuzzer should use hard-coded authentication for a \
	specific application (e.g. dvwa). Optional.", metavar="STRING" )

# common words option
parser.add_option("--common-words", dest="common_words", 
	help="Newline-delimited file of common words to be used in page guessing \
	and input guessing. Required for discovery.", metavar="FILE")

# vectors option
parser.add_option("--vectors", dest="vectors", 
	help="Newline-delimited file of common exploits to vulnerabilities. Required.", 
	metavar = "FILE")

# random option
parser.add_option("--random", dest="random", default= True,
	help="[true|false]  When off, try each input to each page systematically.  \
	When on, choose a random page, then a random input field and test all vectors. Default: false.",
	metavar = "BOOLEAN")

# slow option
parser.add_option("--slow", dest="slow_ms", default=500,
	help="Number of milliseconds considered when a response is considered 'slow' \
	Default is 500 milliseconds", metavar = "NUMBER")
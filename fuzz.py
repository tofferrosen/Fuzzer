"""
file: fuzz.py
description: base script to call.
usage: python fuzz [discover | test] url OPTIONS
"""
import sys 									# For system arguments
import requests								# requests HTTP library 
from custom_auth import *					# Read in all hardcoded authentication
from options import *						# Options parser


(options, args) = parser.parse_args()

if len(sys.argv) < 4:
	parser.error("incorrect number of arguments")

else:
	action = sys.argv[1]
	url = sys.argv[2]

	# authentice if applicable to site
	if options.app_to_auth is not None:

		try: 
			username = custom_auth[options.app_to_auth]["username"]
			password = custom_auth[options.app_to_auth]["password"]
		except:
			parser.error("application specified in --custom-auth does not exist!")

		# get the page
		page = requests.get(url, auth=(username, password))




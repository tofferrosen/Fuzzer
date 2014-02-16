"""
file: discover.py
description: Contains functions for performing discovery of a web page
"""

def page_discovery(page):
	"""
	craws and guesses pages, including link discovery and page 
	guessing
	"""
	urls = link_discovery(page)
	

def link_discovery(page):
	"""
	discovers all accessible links in the same domain
	given a page. Returns a list of urls found
	"""
	urls = []
	print page.text



	

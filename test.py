"""
file: test.py
description: Contains functions for performing testing/fuzzing of a web page
"""
from logger import *     		 			 # logging output
from exploit_strategy import *   			 # the exploit strategy
from sanitization_exploit import * 	 		 # the concrete sanitization exploit
from delayed_response_exploit import *		 # the concrete delayed response exploit
from http_response_exploit import *			 # the concrete http response code exploit
from sensitive_data_exploit import *		 # the concrete sensitive data exploit

def test_pages(pages, session, options):
  """
  test/fuzzes all given pages.

  @pages      an array of page objects to be fuzzed/tested. contains url property, and 
              inputs property that contain a list of forms.
  @session    the requests session objects
  @options    all options given. includes random, location of vectors, and delay time in ms
  """

  # set up all exploit strategies 
  sanitization = ExploitStrategy(pages, session, SanitizationExploit(), options)
 # delayed_response = ExploitStrategy(pages, session, DelayedResponseExploit(), options)
 # http_reponse = ExploitStrategy(pages, session, HttpResponseExploit(), options)
 # sensitive_data = ExploitStrategy(pages, session, SensitiveDataExploit(), options)

  # excute all exploit strategies
 # sanitization.execute()
 # delayed_response.execute()
 # http_response.execute()
 # sensitive_data.execute()

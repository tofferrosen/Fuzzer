"""
file: logger.py
description: Sets up the logging info for Fuzzer
"""
import logging	# Python logging module

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
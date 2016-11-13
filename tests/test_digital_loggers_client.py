#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_digital_loggers_client
----------------------------------

Tests for `digital_loggers_client` module.
"""


import sys
import unittest
from contextlib import contextmanager
from click.testing import CliRunner

from digital_loggers_client.digital_loggers_client import DigitalLoggers
from digital_loggers_client import cli



class test_digital_loggers_client(unittest.TestCase):

    def setUp(self):
        client = DigitalLoggers()
        assert True

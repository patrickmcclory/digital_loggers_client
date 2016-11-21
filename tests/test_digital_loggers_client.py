#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_digital_loggers_client
----------------------------------

Tests for `digital_loggers_client` module.
"""


import sys
import os
import unittest
from contextlib import contextmanager
from click.testing import CliRunner

from digital_loggers_client.digital_loggers_client import DigitalLoggers
from digital_loggers_client import cli



class test_digital_loggers_client(unittest.TestCase):

    def setUp(self):
        client = DigitalLoggers(config_file=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/.dl-client.ini'))
        assert True

    def statusCheck(self):
        client = DigitalLoggers(config_file=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/.dl-client.ini'))
        assert len(client.status_all()) == client.config.get(port_count, -1)

    def TurnOn(self):
        client = DigitalLoggers(config_file=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/.dl-client.ini'))

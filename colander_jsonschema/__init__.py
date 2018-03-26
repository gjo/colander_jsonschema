# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from .exceptions import ConversionError, NoSuchConverter
from . import draft4, draft4_stringdecimal

from .draft4 import convert  # b/w compat


__version__ = '0.3.dev1'

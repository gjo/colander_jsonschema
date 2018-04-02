# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from .exceptions import ConversionError, NoSuchConverter
from .draft4 import Draft4TypeDispatcher
from .draft4_decimalstring import Draft4DecimalStringTypeDispatcher
from .swagger2 import Swagger2TypeDispatcher


convert = Draft4TypeDispatcher()


__version__ = '0.3.dev2'
__all__ = (
    ConversionError,
    Draft4DecimalStringTypeDispatcher,
    Draft4TypeDispatcher,
    NoSuchConverter,
    Swagger2TypeDispatcher,
    convert,
)

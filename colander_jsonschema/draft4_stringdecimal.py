# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import colander
import decimal
from .draft4 import BaseStringTypeConverter, convert as _convert


class DecimalStringTypeConverter(BaseStringTypeConverter):
    def convert_validator(self, schema_node):
        """
        :type schema_node: colander.SchemaNode
        :rtype: dict
        """
        converted = {
            'pattern': r'^[-+]?[0-9]+(\.[0-9]*)?$'
        }
        typ = schema_node.typ
        if isinstance(typ, colander.Decimal):
            if isinstance(typ.quant, decimal.Decimal):
                (_, _, exponent) = typ.quant.as_tuple()
                if exponent < 0:
                    converted['pattern'] = \
                        r'^[-+]?[0-9]+(\.[0-9]{,' + str(abs(exponent)) + r'})?$'
        return converted


def convert(schema_node, converters=None):
    """
    :type schema_node: colander.SchemaNode
    :type converters: dict
    :rtype: dict
    """
    _conv = {
        colander.Decimal: DecimalStringTypeConverter,
    }
    if converters:
        _conv.update(converters)
    return _convert(schema_node, _conv)

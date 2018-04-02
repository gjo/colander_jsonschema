# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import colander
import decimal
from . import draft4


class Draft4DecimalStringTypeConverter(draft4.Draft4BaseStringTypeConverter):
    def convert_type(self, schema_node, cache):
        """
        :type schema_node: colander.SchemaNode
        :type cache: dict[str, object]
        :rtype: dict[str, object]
        """
        converted = super(Draft4DecimalStringTypeConverter,
                          self).convert_type(schema_node, cache)
        if converted:
            converted['pattern'] = r'^[-+]?[0-9]+(\.[0-9]*)?$'
            typ = schema_node.typ
            if isinstance(typ.quant, decimal.Decimal):
                (_, _, exponent) = typ.quant.as_tuple()
                if exponent < 0:
                    converted['pattern'] = r''.join([
                        r'^[-+]?[0-9]+(\.[0-9]{,',
                        str(abs(exponent)),
                        r'})?$'
                    ])
            return converted


class Draft4DecimalStringTypeDispatcher(draft4.Draft4TypeDispatcher):
    converters = {
        colander.Boolean: draft4.Draft4BooleanTypeConverter(),
        colander.Date: draft4.Draft4DateTypeConverter(),
        colander.DateTime: draft4.Draft4DateTimeTypeConverter(),
        colander.Decimal: Draft4DecimalStringTypeConverter(),
        colander.Float: draft4.Draft4NumberTypeConverter(),
        colander.Integer: draft4.Draft4IntegerTypeConverter(),
        colander.Mapping: draft4.Draft4ObjectTypeConverter(),
        colander.Money: Draft4DecimalStringTypeConverter(),
        colander.Sequence: draft4.Draft4ArrayTypeConverter(),
        colander.String: draft4.Draft4StringTypeConverter(),
        colander.Time: draft4.Draft4TimeTypeConverter(),
    }

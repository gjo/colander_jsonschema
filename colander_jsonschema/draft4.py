# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import colander
from . import base


class Draft4OneOfValidatorConverter(object):

    def __init__(self, null_values=(None,)):
        """
        :type null_values: iter
        """
        self.null_values = null_values

    def __call__(self, schema_node, validator):
        """
        :type schema_node: colander.SchemaNode
        :type validator: colander.interfaces.Validator
        :rtype: dict[str, object]
        """
        if isinstance(validator, colander.OneOf):
            converted = {'enum': list(validator.choices)}
            if not schema_node.required:
                converted['enum'].extend(list(self.null_values))
            return converted


class Draft4BaseTypeConverter(base.BaseTypeConverter):
    def convert_type(self, schema_node, cache):
        """
        :type schema_node: colander.SchemaNode
        :type cache: dict[str, object]
        :rtype: dict[str, object]
        """
        converted = super(Draft4BaseTypeConverter,
                          self).convert_type(schema_node, cache)
        if not schema_node.required:
            converted['type'] = [converted['type'], 'null']
        if schema_node.title:
            converted['title'] = schema_node.title
        return converted


class Draft4BaseStringTypeConverter(
    Draft4BaseTypeConverter,
    base.BaseStringTypeConverter,
):

    validator_converters = [
        base.convert_string_length,
        base.convert_regex,
        Draft4OneOfValidatorConverter(('', None)),
    ]

    def convert_type(self, schema_node, cache):
        """
        :type schema_node: colander.SchemaNode
        :type cache: dict[str, object]
        :rtype: dict[str, object]
        """
        converted = super(Draft4BaseStringTypeConverter,
                          self).convert_type(schema_node, cache)
        if schema_node.required:
            converted['minLength'] = 1
        return converted


class Draft4StringTypeConverter(
    Draft4BaseStringTypeConverter,
    base.StringTypeConverter,
):
    pass


class Draft4DateTypeConverter(
    Draft4BaseStringTypeConverter,
    base.DateTypeConverter,
):
    pass


class Draft4DateTimeTypeConverter(
    Draft4BaseStringTypeConverter,
    base.DateTimeTypeConverter,
):
    pass


class Draft4TimeTypeConverter(
    Draft4BaseStringTypeConverter,
    base.TimeTypeConverter,
):
    pass


class Draft4BooleanTypeConverter(
    Draft4BaseTypeConverter,
    base.BooleanTypeConverter,
):
    pass


class Draft4NumberTypeConverter(
    Draft4BaseTypeConverter,
    base.NumberTypeConverter,
):
    validator_converters = [
        base.convert_range,
        Draft4OneOfValidatorConverter(),
    ]


class Draft4IntegerTypeConverter(
    Draft4NumberTypeConverter,
    base.IntegerTypeAdapter,
):
    pass


class Draft4ObjectTypeConverter(
    Draft4BaseTypeConverter,
    base.ObjectTypeConverter,
):
    pass


class Draft4ArrayTypeConverter(
    Draft4BaseTypeConverter,
    base.ArrayTypeConverter,
):
    pass


class Draft4TypeDispatcher(base.TypeDispatcher):
    schema_id = 'http://json-schema.org/draft-04/schema#'
    converters = {
        colander.Boolean: Draft4BooleanTypeConverter(),
        colander.Date: Draft4DateTypeConverter(),
        colander.DateTime: Draft4DateTimeTypeConverter(),
        colander.Float: Draft4NumberTypeConverter(),
        colander.Integer: Draft4IntegerTypeConverter(),
        colander.Mapping: Draft4ObjectTypeConverter(),
        colander.Sequence: Draft4ArrayTypeConverter(),
        colander.String: Draft4StringTypeConverter(),
        colander.Time: Draft4TimeTypeConverter(),
    }

    def finalize(self, schema_node, cache, converted):
        """
        :type schema_node: colander.SchemaNode
        :type cache: dict[str, object]
        :type converted: dict[str, object]
        """
        super(Draft4TypeDispatcher,
              self).finalize(schema_node, cache, converted)
        if converted:
            converted['$schema'] = self.schema_id

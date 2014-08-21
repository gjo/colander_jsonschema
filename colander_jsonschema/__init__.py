# -*- coding: utf-8 -*-

import colander


__version__ = '0.1dev'


def iter_validators(schema_node):
    """
    :type schema_node: colander.SchemaNode
    :rtype: iter
    """
    if schema_node.validator is not None:
        if isinstance(schema_node.validator, colander.All):
            for validator in schema_node.validator.validators:
                yield validator
        else:
            yield schema_node.validator


class ConversionError(Exception):
    pass


class NoSuchConverter(ConversionError):
    pass


class TypeConverter(object):

    type = ''

    def __init__(self, dispatcher):
        """
        :type dispatcher: ConversionDispatcher
        """
        self.dispatcher = dispatcher

    def __call__(self, schema_node, converted=None):
        """
        :type schema_node: colander.SchemaNode
        :type converted: dict
        :rtype: dict
        """
        if converted is None:
            converted = {}
        converted['type'] = self.type
        if not schema_node.required:
            converted['type'] = [converted['type'], 'null']
        if schema_node.raw_title is not colander._marker:
            converted['title'] = schema_node.title
        if schema_node.description:
            converted['description'] = schema_node.description
        if schema_node.default is not colander.null:
            converted['default'] = schema_node.default
        return converted


class BaseStringTypeConverter(TypeConverter):

    type = 'string'
    format = None

    def __call__(self, schema_node, converted=None):
        """
        :type schema_node: colander.SchemaNode
        :type converted: dict
        :rtype: dict
        """
        converted = super(BaseStringTypeConverter,
                          self).__call__(schema_node, converted)
        if schema_node.required:
            converted['minLength'] = 1
        if self.format is not None:
            converted['format'] = self.format
        return converted


class BooleanTypeConverter(TypeConverter):
    type = 'boolean'


class DateTypeConverter(BaseStringTypeConverter):
    format = 'date'


class DateTimeTypeConverter(BaseStringTypeConverter):
    format = 'date-time'


class NumberTypeConverter(TypeConverter):

    type = 'number'

    def __call__(self, schema_node, converted=None):
        """
        :type schema_node: colander.SchemaNode
        :type converted: dict
        :rtype: dict
        """
        converted = super(NumberTypeConverter,
                          self).__call__(schema_node, converted)
        for validator in iter_validators(schema_node):
            if isinstance(validator, colander.Range):
                if validator.max is not None:
                    converted['maximum'] = validator.max
                if validator.min is not None:
                    converted['minimum'] = validator.min
            elif isinstance(validator, colander.OneOf):
                converted['enum'] = list(validator.choices)
                if not schema_node.required:
                    converted['enum'].append(None)
        return converted


class IntegerTypeConverter(NumberTypeConverter):
    type = 'integer'


class StringTypeConverter(BaseStringTypeConverter):

    def __call__(self, schema_node, converted=None):
        """
        :type schema_node: colander.SchemaNode
        :type converted: dict
        :rtype: dict
        """
        converted = super(StringTypeConverter,
                          self).__call__(schema_node, converted)
        for validator in iter_validators(schema_node):
            if isinstance(validator, colander.Length):
                if validator.max is not None:
                    converted['maxLength'] = validator.max
                if validator.min is not None:
                    converted['minLength'] = validator.min
            elif validator is colander.url:
                converted['format'] = 'uri'
            elif isinstance(validator, colander.Email):
                converted['format'] = 'email'
            elif isinstance(validator, colander.Regex):
                converted['pattern'] = validator.match_object.pattern
            elif isinstance(validator, colander.OneOf):
                converted['enum'] = list(validator.choices)
                if not schema_node.required:
                    converted['enum'].append(None)
        return converted


class TimeTypeConverter(BaseStringTypeConverter):
    format = 'time'


class ObjectTypeConverter(TypeConverter):

    type = 'object'

    def __call__(self, schema_node, converted=None):
        """
        :type schema_node: colander.SchemaNode
        :type converted: dict
        :rtype: dict
        """
        converted = super(ObjectTypeConverter,
                          self).__call__(schema_node, converted)
        properties = {}
        required = []
        for sub_node in schema_node.children:
            properties[sub_node.name] = self.dispatcher(sub_node)
            if sub_node.required:
                required.append(sub_node.name)
        converted['properties'] = properties
        if len(required) > 0:
            converted['required'] = required
        return converted


class ArrayTypeConverter(TypeConverter):

    type = 'array'

    def __call__(self, schema_node, converted=None):
        """
        :type schema_node: colander.SchemaNode
        :type converted: dict
        :rtype: dict
        """
        converted = super(ArrayTypeConverter,
                          self).__call__(schema_node, converted)
        converted['items'] = self.dispatcher(schema_node.children[0])
        for validator in iter_validators(schema_node):
            if isinstance(validator, colander.Length):
                if validator.max is not None:
                    converted['maxItems'] = validator.max
                if validator.min is not None:
                    converted['minItems'] = validator.min
        return converted


class ConversionDispatcher(object):

    converters = {
        colander.Boolean: BooleanTypeConverter,
        colander.Date: DateTypeConverter,
        colander.DateTime: DateTimeTypeConverter,
        colander.Float: NumberTypeConverter,
        colander.Integer: IntegerTypeConverter,
        colander.Mapping: ObjectTypeConverter,
        colander.Sequence: ArrayTypeConverter,
        colander.String: StringTypeConverter,
        colander.Time: TimeTypeConverter,
    }

    def __init__(self, converters=None):
        """
        :type converters: dict
        """
        if converters is not None:
            self.converters.update(converters)

    def __call__(self, schema_node):
        """
        :type schema_node: colander.SchemaNode
        :rtype: dict
        """
        schema_type = schema_node.typ
        schema_type = type(schema_type)
        converter_class = self.converters.get(schema_type)
        if converter_class is None:
            raise NoSuchConverter
        converter = converter_class(self)
        converted = converter(schema_node)
        return converted


def finalize_conversion(converted):
    """
    :type converted: dict
    :rtype: dict
    """
    converted['$schema'] = 'http://json-schema.org/draft-04/schema#'
    return converted


def convert(schema_node, converters=None):
    """
    :type schema_node: colander.SchemaNode
    :type converters: dict
    :rtype: dict
    """
    dispatcher = ConversionDispatcher(converters)
    converted = dispatcher(schema_node)
    converted = finalize_conversion(converted)
    return converted

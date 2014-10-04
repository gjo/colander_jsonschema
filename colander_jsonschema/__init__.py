# -*- coding: utf-8 -*-

import colander
import colander.interfaces


__version__ = '0.1dev'


class ConversionError(Exception):
    pass


class NoSuchConverter(ConversionError):
    pass


def convert_length_validator_factory(max_key, min_key):
    """
    :type max_key: str
    :type min_key: str
    """
    def validator_converter(schema_node, validator):
        """
        :type schema_node: colander.SchemaNode
        :type validator: colander.interfaces.Validator
        :rtype: dict
        """
        converted = None
        if isinstance(validator, colander.Length):
            converted = {}
            if validator.max is not None:
                converted[max_key] = validator.max
            if validator.min is not None:
                converted[min_key] = validator.min
        return converted
    return validator_converter


def convert_oneof_validator_factory(null_values=(None,)):
    """
    :type null_values: iter
    """
    def validator_converter(schema_node, validator):
        """
        :type schema_node: colander.SchemaNode
        :type validator: colander.interfaces.Validator
        :rtype: dict
        """
        converted = None
        if isinstance(validator, colander.OneOf):
            converted = {}
            converted['enum'] = list(validator.choices)
            if not schema_node.required:
                converted['enum'].extend(list(null_values))
        return converted

    return validator_converter


def convert_range_validator(schema_node, validator):
    """
    :type schema_node: colander.SchemaNode
    :type validator: colander.interfaces.Validator
    :rtype: dict
    """
    converted = None
    if isinstance(validator, colander.Range):
        converted = {}
        if validator.max is not None:
            converted['maximum'] = validator.max
        if validator.min is not None:
            converted['minimum'] = validator.min
    return converted


def convert_regex_validator(schema_node, validator):
    """
    :type schema_node: colander.SchemaNode
    :type validator: colander.interfaces.Validator
    :rtype: dict
    """
    converted = None
    if isinstance(validator, colander.Regex):
        converted = {}
        if hasattr(colander, 'url') and validator is colander.url:
            converted['format'] = 'uri'
        elif isinstance(validator, colander.Email):
            converted['format'] = 'email'
        else:
            converted['pattern'] = validator.match_object.pattern
    return converted


class ValidatorConversionDispatcher(object):

    def __init__(self, *converters):
        self.converters = converters

    def __call__(self, schema_node, validator=None):
        """
        :type schema_node: colander.SchemaNode
        :type validator: colander.interfaces.Validator
        :rtype: dict
        """
        if validator is None:
            validator = schema_node.validator
        converted = {}
        if validator is not None:
            for converter in (self.convert_all_validator,) + self.converters:
                ret = converter(schema_node, validator)
                if ret is not None:
                    converted = ret
                    break
        return converted

    def convert_all_validator(self, schema_node, validator):
        """
        :type schema_node: colander.SchemaNode
        :type validator: colander.interfaces.Validator
        :rtype: dict
        """
        converted = None
        if isinstance(validator, colander.All):
            converted = {}
            for v in validator.validators:
                ret = self(schema_node, v)
                converted.update(ret)
        return converted


class TypeConverter(object):

    type = ''
    convert_validator = lambda self, schema_node: {}

    def __init__(self, dispatcher):
        """
        :type dispatcher: TypeConversionDispatcher
        """
        self.dispatcher = dispatcher

    def convert_type(self, schema_node, converted):
        """
        :type schema_node: colander.SchemaNode
        :type converted: dict
        :rtype: dict
        """
        converted['type'] = self.type
        if not schema_node.required:
            converted['type'] = [converted['type'], 'null']
        if schema_node.title:
            converted['title'] = schema_node.title
        if schema_node.description:
            converted['description'] = schema_node.description
        if schema_node.default is not colander.null:
            converted['default'] = schema_node.default
        return converted

    def __call__(self, schema_node, converted=None):
        """
        :type schema_node: colander.SchemaNode
        :type converted: dict
        :rtype: dict
        """
        if converted is None:
            converted = {}
        converted = self.convert_type(schema_node, converted)
        converted.update(self.convert_validator(schema_node))
        return converted


class BaseStringTypeConverter(TypeConverter):

    type = 'string'
    format = None

    def convert_type(self, schema_node, converted):
        """
        :type schema_node: colander.SchemaNode
        :type converted: dict
        :rtype: dict
        """
        converted = super(BaseStringTypeConverter,
                          self).convert_type(schema_node, converted)
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
    convert_validator = ValidatorConversionDispatcher(
        convert_range_validator,
        convert_oneof_validator_factory(),
    )


class IntegerTypeConverter(NumberTypeConverter):
    type = 'integer'


class StringTypeConverter(BaseStringTypeConverter):
    convert_validator = ValidatorConversionDispatcher(
        convert_length_validator_factory('maxLength', 'minLength'),
        convert_regex_validator,
        convert_oneof_validator_factory(('', None)),
    )


class TimeTypeConverter(BaseStringTypeConverter):
    format = 'time'


class ObjectTypeConverter(TypeConverter):

    type = 'object'

    def convert_type(self, schema_node, converted):
        """
        :type schema_node: colander.SchemaNode
        :type converted: dict
        :rtype: dict
        """
        converted = super(ObjectTypeConverter,
                          self).convert_type(schema_node, converted)
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
    convert_validator = ValidatorConversionDispatcher(
        convert_length_validator_factory('maxItems', 'minItems'),
    )

    def convert_type(self, schema_node, converted):
        """
        :type schema_node: colander.SchemaNode
        :type converted: dict
        :rtype: dict
        """
        converted = super(ArrayTypeConverter,
                          self).convert_type(schema_node, converted)
        converted['items'] = self.dispatcher(schema_node.children[0])
        return converted


class TypeConversionDispatcher(object):

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
    dispatcher = TypeConversionDispatcher(converters)
    converted = dispatcher(schema_node)
    converted = finalize_conversion(converted)
    return converted

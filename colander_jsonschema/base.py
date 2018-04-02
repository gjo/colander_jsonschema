# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import colander
from .exceptions import NoSuchConverter


class LengthValidatorConverter(object):
    def __init__(self, max_key, min_key):
        """
        :type max_key: str
        :type min_key: str
        """
        self.max_key = max_key
        self.min_key = min_key

    def __call__(self, schema_node, validator):
        """
        :type schema_node: colander.SchemaNode
        :type validator: colander.interfaces.Validator
        :rtype: dict[str, object]
        """
        if isinstance(validator, colander.Length):
            converted = {}
            if validator.max is not None:
                converted[self.max_key] = validator.max
            if validator.min is not None:
                converted[self.min_key] = validator.min
            return converted


convert_string_length = LengthValidatorConverter('maxLength', 'minLength')
convert_array_length = LengthValidatorConverter('maxItems', 'minItems')


def convert_enum(schema_node, validator):
    """
    :type schema_node: colander.SchemaNode
    :type validator: colander.interfaces.Validator
    :rtype: dict[str, object]
    """
    if isinstance(validator, colander.OneOf):
        converted = {'enum': list(validator.choices)}
        return converted


def convert_range(schema_node, validator):
    """
    :type schema_node: colander.SchemaNode
    :type validator: colander.interfaces.Validator
    :rtype: dict[str, object]
    """
    if isinstance(validator, colander.Range):
        converted = {}
        if validator.max is not None:
            converted['maximum'] = validator.max
        if validator.min is not None:
            converted['minimum'] = validator.min
        return converted


def convert_regex(schema_node, validator):
    """
    :type schema_node: colander.SchemaNode
    :type validator: colander.interfaces.Validator
    :rtype: dict[str, object]
    """
    if isinstance(validator, colander.Regex):
        converted = {}
        if hasattr(colander, 'url') and validator is colander.url:
            converted['format'] = 'uri'
        elif isinstance(validator, colander.Email):
            converted['format'] = 'email'
        else:
            converted['pattern'] = validator.match_object.pattern
        return converted


class ValidatorDispatcher(object):

    def __init__(self, *converters):
        """
        :type converters: (colander.SchemaNode, colander.interfaces.Validator)
            -> dict[str, object]
        """
        self.converters = converters

    def __call__(self, schema_node, validator):
        """
        :type schema_node: colander.SchemaNode
        :type validator: colander.interfaces.Validator
        :rtype: dict[str, object]
        """
        if validator:
            for converter in (self.convert_all,) + self.converters:
                converted = converter(schema_node, validator)
                if converted:
                    return converted

    def convert_all(self, schema_node, validator):
        """
        :type schema_node: colander.SchemaNode
        :type validator: colander.interfaces.Validator
        :rtype: dict[str, object]
        """
        if isinstance(validator, colander.All):
            converted = {}
            for v in validator.validators:
                ret = self(schema_node, v)
                if ret:
                    converted.update(ret)
            if converted:
                return converted


class BaseTypeConverter(object):
    """
    :type type: str
    :type validator_dispatcher_class: ValidatorDispatcher
    :type validator_converters: list[
        (colander.SchemaNode, colander.interfaces.Validator)
        -> dict[str, object]
    ]
    """

    type = ''
    validator_dispatcher_class = ValidatorDispatcher
    validator_converters = []

    def __init__(self):
        self.validator_dispatcher = self.validator_dispatcher_class(
            *self.validator_converters
        )

    def convert_type(self, schema_node, cache):
        """
        :type schema_node: colander.SchemaNode
        :type cache: dict[str, object]
        :rtype: dict[str, object]
        """
        converted = {'type': self.type}
        if schema_node.description:
            converted['description'] = schema_node.description
        if schema_node.default is not colander.null:
            converted['default'] = schema_node.default
        return converted

    def convert_validator(self, schema_node):
        """
        :type schema_node: colander.SchemaNode
        :rtype: dict[str, object]
        """
        if schema_node.validator and self.validator_dispatcher:
            return self.validator_dispatcher(schema_node,
                                             schema_node.validator)

    def __call__(self, schema_node, cache):
        """
        :type schema_node: colander.SchemaNode
        :type cache: dict[str, object]
        :rtype: dict[str, object]
        """
        converted = self.convert_type(schema_node, cache)
        if converted:
            converted_validator = self.convert_validator(schema_node)
            if converted_validator:
                converted.update(converted_validator)
            return converted


class BaseStringTypeConverter(BaseTypeConverter):
    """
    :type format: str
    """

    type = 'string'
    format = None

    def convert_type(self, schema_node, cache):
        """
        :type schema_node: colander.SchemaNode
        :type cache: dict[str, object]
        :rtype: dict[str, object]
        """
        converted = super(BaseStringTypeConverter,
                          self).convert_type(schema_node, cache)
        if self.format is not None:
            converted['format'] = self.format
        return converted


class StringTypeConverter(BaseStringTypeConverter):
    validator_converters = [
        convert_string_length,
        convert_regex,
        convert_enum,
    ]


class DateTypeConverter(BaseStringTypeConverter):
    format = 'date'


class DateTimeTypeConverter(BaseStringTypeConverter):
    format = 'date-time'


class TimeTypeConverter(BaseStringTypeConverter):
    format = 'time'


class BooleanTypeConverter(BaseTypeConverter):
    type = 'boolean'


class NumberTypeConverter(BaseTypeConverter):
    type = 'number'
    validator_converters = [
        convert_range,
        convert_enum,
    ]


class IntegerTypeAdapter(NumberTypeConverter):
    type = 'integer'


class ArrayTypeConverter(BaseTypeConverter):
    type = 'array'
    validator_converters = [
        convert_array_length,
    ]


class ObjectTypeConverter(BaseTypeConverter):
    type = 'object'


class TypeDispatcher(object):

    converters = {}

    def __init__(self, converters=None):
        """
        :type converters: dist[
            type,
            (colander.SchemaNode, dict[str, object]) -> dict[str, object]
        ]
        """
        if converters:
            self.converters = self.converters.copy()
            self.converters.update(converters)

    def __call__(self, schema_node):
        """
        :type schema_node: colander.SchemaNode
        :type cache: dict[str, object]
        :rtype: dict[str, object]
        """
        cache = {}
        converted = self.convert_type(schema_node, cache)
        self.finalize(schema_node, cache, converted)
        return converted

    def convert_type(self, schema_node, cache):
        """
        :type schema_node: colander.SchemaNode
        :type cache: dict[str, object]
        :rtype: dict[str, object]
        """
        schema_type = schema_node.typ.__class__
        if schema_type not in self.converters:
            raise NoSuchConverter(schema_type)
        converter = self.converters[schema_type]
        converted = converter(schema_node, cache)
        if converted:
            if issubclass(schema_type, colander.Sequence):
                self.convert_array_children(schema_node, cache, converted)
            elif issubclass(schema_type, colander.Mapping):
                self.convert_object_children(schema_node, cache, converted)
            return converted

    def convert_array_children(self, schema_node, cache, converted):
        """
        :type schema_node: colander.SchemaNode
        :type cache: dict[str, object]
        :type converted: dict[str, object]
        """
        converted['items'] = self.convert_type(schema_node.children[0], cache)

    def convert_object_children(self, schema_node, cache, converted):
        """
        :type schema_node: colander.SchemaNode
        :type cache: dict[str, object]
        :type converted: dict[str, object]
        """
        properties = {}
        required = []
        for sub_node in schema_node.children:
            properties[sub_node.name] = self.convert_type(sub_node, cache)
            if sub_node.required:
                required.append(sub_node.name)
        converted['properties'] = properties
        if len(required) > 0:
            converted['required'] = required

    def finalize(self, schema_node, cache, converted):
        """
        :type schema_node: colander.SchemaNode
        :type cache: dict[str, object]
        :type converted: dict[str, object]
        """
        pass


class DefinitiveTypeDispatcher(TypeDispatcher):
    def convert_type(self, schema_node, cache):
        """
        :type schema_node: colander.SchemaNode
        :type cache: dict[str, object]
        :rtype: dict[str, object]
        """
        schema_type = schema_node.typ.__class__
        if not issubclass(schema_type, colander.Mapping):
            return super(DefinitiveTypeDispatcher,
                         self).convert_type(schema_node, cache)

        name = schema_node.__class__.__name__
        if name not in cache:
            cache[name] = super(DefinitiveTypeDispatcher,
                                self).convert_type(schema_node, cache)
        if cache[name]:
            return {'$ref': '#/definitions/' + name}

    def finalize(self, schema_node, cache, converted):
        """
        :type schema_node: colander.SchemaNode
        :type cache: dict[str, object]
        :type converted: dict[str, object]
        """
        super(DefinitiveTypeDispatcher,
              self).finalize(schema_node, cache, converted)
        if converted and cache:
            converted['definitions'] = cache

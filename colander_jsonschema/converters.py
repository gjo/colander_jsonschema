# -*- coding: utf-8 -*-

import logging
import colander


logger = logging.getLogger(__name__)


class ConversionError(Exception):
    pass


class Converter(object):

    type = ''

    def __init__(self, dispatcher):
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
        if schema_node.title:
            converted['title'] = schema_node.title
        if schema_node.description:
            converted['description'] = schema_node.description
        return converted


class IntegerConverter(Converter):
    type = 'integer'


class StringConverter(Converter):
    type = 'string'


class MappingConverter(Converter):

    type = 'object'

    def __call__(self, schema_node, converted=None):
        """
        :type schema_node: colander.SchemaNode
        :type converted: dict
        :rtype: dict
        """
        converted = super(MappingConverter, self).__call__(schema_node,
                                                           converted)
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


class ConversionDispatcher(object):

    converters = {
        colander.Integer: IntegerConverter,
        colander.Mapping: MappingConverter,
        colander.String: StringConverter,
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
        if isinstance(schema_type, colander.SchemaType):
            schema_type = type(schema_type)
        converter_class = self.converters.get(schema_type)
        if converter_class is None:
            raise ConversionError
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
    dispatcher = ConversionDispatcher(converters)
    converted = dispatcher(schema_node)
    converted = finalize_conversion(converted)
    return converted

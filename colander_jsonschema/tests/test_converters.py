# -*- coding: utf-8 -*-

import unittest
import colander


class ConvertTestCase(unittest.TestCase):

    def test_mapping(self):

        class CheckClass(colander.MappingSchema):
            var_b = colander.SchemaNode(colander.Bool)
            var_f = colander.SchemaNode(colander.Float)
            var_i = colander.SchemaNode(colander.Int)
            var_s = colander.SchemaNode(colander.Str)

        from ..converters import convert
        ret = convert(CheckClass())
        self.assertDictEqual(ret, {
            '$schema': 'http://json-schema.org/draft-04/schema#',
            'type': 'object',
            'properties': {
                'var_b': {'type': 'boolean', 'title': 'Var B'},
                'var_f': {'type': 'number', 'title': 'Var F'},
                'var_i': {'type': 'integer', 'title': 'Var I'},
                'var_s': {'type': 'string', 'title': 'Var S'}
            },
            'required': ['var_b', 'var_f', 'var_i', 'var_s']
        })
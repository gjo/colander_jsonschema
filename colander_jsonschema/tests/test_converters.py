# -*- coding: utf-8 -*-

import unittest
import colander


class ConvertTestCase(unittest.TestCase):

    def test(self):

        class CheckClass(colander.MappingSchema):
            var_i = colander.SchemaNode(colander.Int)
            var_s = colander.SchemaNode(colander.Str)

        from ..converters import convert
        ret = convert(CheckClass())
        self.assertDictEqual(ret, {
            '$schema': 'http://json-schema.org/draft-04/schema#',
            'type': 'object',
            'properties': {
                'var_i': {'type': 'integer', 'title': 'Var I'},
                'var_s': {'type': 'string', 'title': 'Var S'}
            },
            'required': ['var_i', 'var_s']
        })

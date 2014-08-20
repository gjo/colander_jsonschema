# -*- coding: utf-8 -*-

import unittest
import colander


class ConvertTestCase(unittest.TestCase):

    def test_mapping(self):

        class CheckMapping(colander.MappingSchema):
            var_b = colander.SchemaNode(colander.Bool())
            var_d = colander.SchemaNode(colander.Date())
            var_dt = colander.SchemaNode(colander.DateTime())
            var_f = colander.SchemaNode(colander.Float())
            var_i = colander.SchemaNode(colander.Int(), default=0)
            var_s = colander.SchemaNode(colander.Str())
            var_t = colander.SchemaNode(colander.Time())

        class CheckSequence(colander.SequenceSchema):
            var_m = CheckMapping()

        from ..converters import convert
        ret = convert(CheckSequence())
        self.assertDictEqual(ret, {
            '$schema': 'http://json-schema.org/draft-04/schema#',
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'var_b': {'type': 'boolean'},
                    'var_d': {'type': 'string', 'minLength': 1,
                              'format': 'date'},
                    'var_dt': {'type': 'string', 'minLength': 1,
                               'format': 'date-time'},
                    'var_f': {'type': 'number'},
                    'var_i': {'type': 'integer', 'default': 0},
                    'var_s': {'type': 'string', 'minLength': 1},
                    'var_t': {'type': 'string', 'minLength': 1,
                              'format': 'time'},
                },
                'required': ['var_b', 'var_d', 'var_dt', 'var_f', 'var_i',
                             'var_s', 'var_t'],
            }
        })

# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest


class DecimalNodeTestCase(unittest.TestCase):

    def test_string(self):
        import colander
        from colander_jsonschema.draft4_stringdecimal import convert
        node = colander.SchemaNode(colander.Decimal())
        ret = convert(node)
        self.assertDictEqual(ret, {
            '$schema': 'http://json-schema.org/draft-04/schema#',
            'type': 'string',
            'minLength': 1,
            'pattern': r'^[-+]?[0-9]+(\.[0-9]*)?$',
        })

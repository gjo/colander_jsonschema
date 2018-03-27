# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import decimal
import colander
import unittest


class DecimalNodeTestCase(unittest.TestCase):

    def test_string(self):
        from colander_jsonschema.draft4_stringdecimal import convert
        node = colander.SchemaNode(colander.Decimal())
        ret = convert(node)
        self.assertDictEqual(ret, {
            '$schema': 'http://json-schema.org/draft-04/schema#',
            'type': 'string',
            'minLength': 1,
            'pattern': r'^[-+]?[0-9]+(\.[0-9]*)?$',
        })

    def test_quant(self):
        from colander_jsonschema.draft4_stringdecimal import convert
        quant = decimal.Decimal('1.00')
        node = colander.SchemaNode(colander.Decimal(quant=quant))
        ret = convert(node)
        self.assertDictEqual(ret, {
            '$schema': 'http://json-schema.org/draft-04/schema#',
            'type': 'string',
            'minLength': 1,
            'pattern': r'^[-+]?[0-9]+(\.[0-9]{,2})?$',
        })


class ConvertTestCase(unittest.TestCase):

    def test_overwrite(self):
        from colander_jsonschema.draft4_stringdecimal import convert
        node = colander.SchemaNode(colander.String())
        ret = convert(node, {
            colander.String: lambda dp: lambda sn: {'test': 'TEST'},
        })
        self.assertDictEqual(ret, {
            '$schema': 'http://json-schema.org/draft-04/schema#',
            'test': 'TEST',
        })

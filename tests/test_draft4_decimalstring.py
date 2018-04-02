# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import colander
import decimal
import unittest


class DecimalNodeTestCase(unittest.TestCase):

    def test_string(self):
        from colander_jsonschema import Draft4DecimalStringTypeDispatcher
        convert = Draft4DecimalStringTypeDispatcher()
        node = colander.SchemaNode(colander.Decimal())
        ret = convert(node)
        self.assertDictEqual(ret, {
            '$schema': 'http://json-schema.org/draft-04/schema#',
            'type': 'string',
            'minLength': 1,
            'pattern': r'^[-+]?[0-9]+(\.[0-9]*)?$',
        })

    def test_quant(self):
        from colander_jsonschema import Draft4DecimalStringTypeDispatcher
        convert = Draft4DecimalStringTypeDispatcher()
        quant = decimal.Decimal('1.00')
        node = colander.SchemaNode(colander.Decimal(quant=quant))
        ret = convert(node)
        self.assertDictEqual(ret, {
            '$schema': 'http://json-schema.org/draft-04/schema#',
            'type': 'string',
            'minLength': 1,
            'pattern': r'^[-+]?[0-9]+(\.[0-9]{,2})?$',
        })

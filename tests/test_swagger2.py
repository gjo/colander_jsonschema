# -*- coding: utf-8 -*-

import colander
import unittest


class Swagger2ConverterTestCase(unittest.TestCase):

    def test(self):
        from colander_jsonschema import Swagger2TypeDispatcher
        convert = Swagger2TypeDispatcher()

        class NonNegativeIntNode(colander.SchemaNode):
            schema_type = colander.Integer
            validator = colander.Range(min=0)

        class PositiveIntNode(colander.SchemaNode):
            schema_type = colander.Integer
            validator = colander.Range(min=1)

        class DefaultTrueBoolNode(colander.SchemaNode):
            schema_type = colander.Boolean
            default = True
            missing = True

        class PreDefinedStringNode(colander.SchemaNode):
            schema_type = colander.String
            validator = colander.OneOf(['AAA', 'BBB'])

        class PreDefinedIntegerNode(colander.SchemaNode):
            schema_type = colander.Integer
            validator = colander.OneOf([0, 1, 2])

        class Inner(colander.Schema):
            a = colander.SchemaNode(colander.String())

        class SomeClass(colander.Schema):
            some_int = colander.SchemaNode(colander.Integer())
            other_int = colander.SchemaNode(colander.Integer(), missing=None)
            def_int = PreDefinedIntegerNode(missing=None)
            some_str = colander.SchemaNode(colander.String())
            other_str = colander.SchemaNode(colander.String(), missing=None)
            def_str = PreDefinedStringNode(missing=None)
            inner = Inner(missing=None)

        class Collection(colander.Schema):
            description = "open-social's `collection` compatible"
            start_index = NonNegativeIntNode(name='startIndex')
            items_per_page = PositiveIntNode(name='itemPerPage')
            total_results = NonNegativeIntNode(name='totalResults')
            filtered = DefaultTrueBoolNode()
            sorted = DefaultTrueBoolNode()
            updatedSince = DefaultTrueBoolNode()

        class SomeClassContainer(Collection):

            @colander.instantiate(name='list')
            class SomeClassList(colander.SequenceSchema):
                item = SomeClass()

        schema = SomeClassContainer()
        converted = convert(schema)
        self.maxDiff = None
        self.assertDictEqual(converted, {
            '$ref': '#/definitions/SomeClassContainer',
            'definitions': {
                'Inner': {
                    'type': 'object',
                    'properties': {'a': {'type': 'string'}},
                    'required': ['a'],
                },
                'SomeClass': {
                    'type': 'object',
                    'properties': {
                        'def_int': {'type': 'integer', 'enum': [0, 1, 2]},
                        'def_str': {'type': 'string', 'enum': ['AAA', 'BBB']},
                        'inner': {'$ref': '#/definitions/Inner'},
                        'other_int': {'type': 'integer'},
                        'other_str': {'type': 'string'},
                        'some_int': {'type': 'integer'},
                        'some_str': {'type': 'string'},
                    },
                    'required': ['some_int', 'some_str'],
                },
                'SomeClassContainer': {
                    'description': "open-social's `collection` compatible",
                    'type': 'object',
                    'properties': {
                        'filtered': {'type': 'boolean', 'default': True},
                        'itemPerPage': {'type': 'integer', 'minimum': 1},
                        'sorted': {'type': 'boolean', 'default': True},
                        'startIndex': {'type': 'integer', 'minimum': 0},
                        'totalResults': {'type': 'integer', 'minimum': 0},
                        'updatedSince': {'type': 'boolean', 'default': True},
                        'list': {
                            'type': 'array',
                            'items': {'$ref': '#/definitions/SomeClass'},
                        },
                    },
                    'required': [
                        'startIndex',
                        'itemPerPage',
                        'totalResults',
                        'list',
                    ],
                },
            },
        })

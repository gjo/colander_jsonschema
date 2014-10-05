# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest


class StringNodeTestCase(unittest.TestCase):

    def test_minimal(self):
        import colander
        from .. import convert
        node = colander.SchemaNode(colander.String())
        ret = convert(node)
        self.assertDictEqual(ret, {
            '$schema': 'http://json-schema.org/draft-04/schema#',
            'type': 'string',
            'minLength': 1,
        })

    def test_can_null(self):
        import colander
        from .. import convert
        node = colander.SchemaNode(colander.String(), missing=None)
        ret = convert(node)
        self.assertDictEqual(ret, {
            '$schema': 'http://json-schema.org/draft-04/schema#',
            'type': ['string', 'null'],
        })

    def test_has_default(self):
        import colander
        from .. import convert
        node = colander.SchemaNode(colander.String(), default='DEFAULT')
        ret = convert(node)
        self.assertDictEqual(ret, {
            '$schema': 'http://json-schema.org/draft-04/schema#',
            'type': 'string',
            'minLength': 1,
            'default': 'DEFAULT',
        })

    def test_can_null_has_default(self):
        import colander
        from .. import convert
        node = colander.SchemaNode(colander.String(), missing='DEFAULT',
                                   default='DEFAULT')
        ret = convert(node)
        self.assertDictEqual(ret, {
            '$schema': 'http://json-schema.org/draft-04/schema#',
            'type': ['string', 'null'],
            'default': 'DEFAULT',
        })

    def test_validate_length_both(self):
        import colander
        from .. import convert
        node = colander.SchemaNode(colander.String(),
                                   validator=colander.Length(11, 33))
        ret = convert(node)
        self.assertDictEqual(ret, {
            '$schema': 'http://json-schema.org/draft-04/schema#',
            'type': 'string',
            'maxLength': 33,
            'minLength': 11,
        })

    def test_validate_length_min_and_null(self):
        import colander
        from .. import convert
        node = colander.SchemaNode(colander.String(),
                                   validator=colander.Length(22),
                                   missing=None)
        ret = convert(node)
        self.assertDictEqual(ret, {
            '$schema': 'http://json-schema.org/draft-04/schema#',
            'type': ['string', 'null'],
            'minLength': 22,
        })

    def test_validate_length_max(self):
        import colander
        from .. import convert
        node = colander.SchemaNode(colander.String(),
                                   validator=colander.Length(max=44),
                                   missing=None)
        ret = convert(node)
        self.assertDictEqual(ret, {
            '$schema': 'http://json-schema.org/draft-04/schema#',
            'type': ['string', 'null'],
            'maxLength': 44,
        })

    def test_validate_length_max_and_null(self):
        import colander
        from .. import convert
        node = colander.SchemaNode(colander.String(),
                                   validator=colander.Length(max=55))
        ret = convert(node)
        self.assertDictEqual(ret, {
            '$schema': 'http://json-schema.org/draft-04/schema#',
            'type': 'string',
            'maxLength': 55,
            'minLength': 1,
        })

    def test_validate_regex(self):
        import colander
        from .. import convert
        node = colander.SchemaNode(colander.String(),
                                   validator=colander.Regex(r'TESTtestTEST'))
        ret = convert(node)
        self.assertDictEqual(ret, {
            '$schema': 'http://json-schema.org/draft-04/schema#',
            'type': 'string',
            'pattern': 'TESTtestTEST',
            'minLength': 1,
        })

    def test_validate_regex_email(self):
        import colander
        from .. import convert
        node = colander.SchemaNode(colander.String(),
                                   validator=colander.Email())
        ret = convert(node)
        self.assertDictEqual(ret, {
            '$schema': 'http://json-schema.org/draft-04/schema#',
            'type': 'string',
            'format': 'email',
            'minLength': 1,
        })

    def test_validate_oneof(self):
        import colander
        from .. import convert
        node = colander.SchemaNode(colander.String(),
                                   validator=colander.OneOf(["one", "two"]))
        ret = convert(node)
        self.assertDictEqual(ret, {
            '$schema': 'http://json-schema.org/draft-04/schema#',
            'type': 'string',
            'enum': ['one', 'two'],
            'minLength': 1,
        })

    def test_validate_oneof_null(self):
        import colander
        from .. import convert
        node = colander.SchemaNode(colander.String(),
                                   validator=colander.OneOf(["one", "two"]),
                                   missing=None)
        ret = convert(node)
        self.assertDictEqual(ret, {
            '$schema': 'http://json-schema.org/draft-04/schema#',
            'type': ['string', 'null'],
            'enum': ['one', 'two', '', None],
        })

    def test_title(self):
        import colander
        from .. import convert
        node = colander.SchemaNode(colander.String(), title='TITLEtitleTITLE')
        ret = convert(node)
        self.assertDictEqual(ret, {
            '$schema': 'http://json-schema.org/draft-04/schema#',
            'type': 'string',
            'minLength': 1,
            'title': 'TITLEtitleTITLE',
        })

    def test_description(self):
        import colander
        from .. import convert
        node = colander.SchemaNode(colander.String(),
                                   description='descriptionDESCRIPTION')
        ret = convert(node)
        self.assertDictEqual(ret, {
            '$schema': 'http://json-schema.org/draft-04/schema#',
            'type': 'string',
            'minLength': 1,
            'description': 'descriptionDESCRIPTION',
        })


class IntegerNodeTestCase(unittest.TestCase):

    def test_minimal(self):
        import colander
        from .. import convert
        node = colander.SchemaNode(colander.Integer())
        ret = convert(node)
        self.assertDictEqual(ret, {
            '$schema': 'http://json-schema.org/draft-04/schema#',
            'type': 'integer',
        })

    def test_null(self):
        import colander
        from .. import convert
        node = colander.SchemaNode(colander.Integer(), missing=None)
        ret = convert(node)
        self.assertDictEqual(ret, {
            '$schema': 'http://json-schema.org/draft-04/schema#',
            'type': ['integer', 'null'],
        })

    def test_default(self):
        import colander
        from .. import convert
        node = colander.SchemaNode(colander.Integer(), default=1)
        ret = convert(node)
        self.assertDictEqual(ret, {
            '$schema': 'http://json-schema.org/draft-04/schema#',
            'type': 'integer',
            'default': 1,
        })

    def test_default_null(self):
        import colander
        from .. import convert
        node = colander.SchemaNode(colander.Integer(), missing=None,
                                   default=None)
        ret = convert(node)
        self.assertDictEqual(ret, {
            '$schema': 'http://json-schema.org/draft-04/schema#',
            'type': ['integer', 'null'],
            'default': None,
        })

    def test_enum(self):
        import colander
        from .. import convert
        node = colander.SchemaNode(colander.Integer(),
                                   validator=colander.OneOf([1, 2, 3, 4]))
        ret = convert(node)
        self.assertDictEqual(ret, {
            '$schema': 'http://json-schema.org/draft-04/schema#',
            'type': 'integer',
            'enum': [1, 2, 3, 4],
        })

    def test_enum_null(self):
        import colander
        from .. import convert
        node = colander.SchemaNode(colander.Integer(), missing=None,
                                   default=None,
                                   validator=colander.OneOf([1, 2, 3, 4]))
        ret = convert(node)
        self.assertDictEqual(ret, {
            '$schema': 'http://json-schema.org/draft-04/schema#',
            'type': ['integer', 'null'],
            'default': None,
            'enum': [1, 2, 3, 4, None],
        })

    def test_range_both(self):
        import colander
        from .. import convert
        node = colander.SchemaNode(colander.Integer(),
                                   validator=colander.Range(111, 555))
        ret = convert(node)
        self.assertDictEqual(ret, {
            '$schema': 'http://json-schema.org/draft-04/schema#',
            'type': 'integer',
            'minimum': 111,
            'maximum': 555,
        })

    def test_range_min(self):
        import colander
        from .. import convert
        node = colander.SchemaNode(colander.Integer(),
                                   validator=colander.Range(222))
        ret = convert(node)
        self.assertDictEqual(ret, {
            '$schema': 'http://json-schema.org/draft-04/schema#',
            'type': 'integer',
            'minimum': 222,
        })

    def test_range_max(self):
        import colander
        from .. import convert
        node = colander.SchemaNode(colander.Integer(),
                                   validator=colander.Range(max=444))
        ret = convert(node)
        self.assertDictEqual(ret, {
            '$schema': 'http://json-schema.org/draft-04/schema#',
            'type': 'integer',
            'maximum': 444,
        })


class DateTimeNodeTestCase(unittest.TestCase):

    def test_minimal(self):
        import colander
        from .. import convert
        node = colander.SchemaNode(colander.DateTime())
        ret = convert(node)
        self.assertDictEqual(ret, {
            '$schema': 'http://json-schema.org/draft-04/schema#',
            'type': 'string',
            'format': 'date-time',
            'minLength': 1,
        })

    def test_null(self):
        import colander
        from .. import convert
        node = colander.SchemaNode(colander.DateTime(), missing=None)
        ret = convert(node)
        self.assertDictEqual(ret, {
            '$schema': 'http://json-schema.org/draft-04/schema#',
            'type': ['string', 'null'],
            'format': 'date-time',
        })


class SequenceSchemaTestCase(unittest.TestCase):

    def test(self):
        import colander
        from .. import convert

        class BaseMapping(colander.MappingSchema):
            name = colander.SchemaNode(colander.String())
            number = colander.SchemaNode(colander.Integer())

        class BaseMappings(colander.SequenceSchema):
            base_mapping = BaseMapping()

        schema = BaseMappings()
        ret = convert(schema)
        self.maxDiff = None
        self.assertDictEqual(ret, {
            '$schema': 'http://json-schema.org/draft-04/schema#',
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'name': {
                        'type': 'string',
                        'minLength': 1,
                        'title': 'Name',
                    },
                    'number': {
                        'type': 'integer',
                        'title': 'Number',
                    }
                },
                'required': ['name', 'number'],
                'title': 'Base Mapping',
            },
        })


class MappingSchemaTestCase(unittest.TestCase):

    def test(self):
        import colander
        from .. import convert

        class BaseMapping(colander.MappingSchema):
            title = 'unnumbered object'
            description = 'covered description'
            title_ = colander.SchemaNode(
                colander.String(),
                validator=colander.Length(max=255),
                name='title',
                title='name of object',
                description='one line string',
            )
            description_ = colander.SchemaNode(
                colander.String(),
                validator=colander.Length(max=4096),
                default='',
                missing='',
                name='description',
                title='description of object',
                description='multi line string'
            )
            can_publish = colander.SchemaNode(
                colander.Boolean(),
                default=False,
                name='canPublish',
                title='can publish object',
                description='object is shown in web if true',
            )

        class ExtendedMapping(BaseMapping):
            title = 'numbered object'
            description = 'the instanced object'
            id = colander.SchemaNode(
                colander.Integer(),
                validator=colander.Range(min=1),
                title='identity for mapping',
                description='1-origin 64bit signed integer'
            )
            created_at = colander.SchemaNode(
                colander.DateTime(),
                name='createdAt',
                title='timestamp of object creation',
                description='UTC time',
            )

        schema = ExtendedMapping()
        ret = convert(schema)
        self.maxDiff = None
        self.assertDictEqual(ret, {
            '$schema': 'http://json-schema.org/draft-04/schema#',
            'type': 'object',
            # 'title': 'numbered object',  # colander-1.0b1 hides this
            'description': 'the instanced object',  # colander-0.9.9 hide this
            'required': [
                'title',
                'canPublish',
                'id',
                'createdAt',
            ],
            'properties': {
                'title': {
                    'type': 'string',
                    'maxLength': 255,
                    'minLength': 1,
                    'title': 'name of object',
                    'description': 'one line string',
                },
                'description': {
                    'type': ['string', 'null'],
                    'maxLength': 4096,
                    'default': '',
                    'title': 'description of object',
                    'description': 'multi line string',
                },
                'canPublish': {
                    'type': 'boolean',
                    'default': False,
                    'title': 'can publish object',
                    'description': 'object is shown in web if true',
                },
                'id': {
                    'type': 'integer',
                    'minimum': 1,
                    'title': 'identity for mapping',
                    'description': '1-origin 64bit signed integer',
                },
                'createdAt': {
                    'type': 'string',
                    'format': 'date-time',
                    'minLength': 1,
                    'title': 'timestamp of object creation',
                    'description': 'UTC time',
                },
            }
        })

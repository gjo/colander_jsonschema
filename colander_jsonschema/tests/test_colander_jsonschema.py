# -*- coding: utf-8 -*-

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
                                   validator=colander.Regex(ur'TESTtestTEST'))
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


class ConvertTestCase(unittest.TestCase):

    def tes_mapping(self):
        import colander

        class CheckMapping(colander.MappingSchema):
            var_b = colander.SchemaNode(colander.Bool())
            var_d = colander.SchemaNode(colander.Date())
            var_dt = colander.SchemaNode(colander.DateTime())
            var_f = colander.SchemaNode(colander.Float())
            var_i = colander.SchemaNode(colander.Int(), default=0)
            var_s = colander.SchemaNode(colander.Str(),
                                        validator=colander.Length(max=100))
            var_t = colander.SchemaNode(colander.Time())

        class CheckSequence(colander.SequenceSchema):
            var_m = CheckMapping()

        from .. import convert
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
                    'var_s': {'type': 'string', 'minLength': 1,
                              'maxLength': 100},
                    'var_t': {'type': 'string', 'minLength': 1,
                              'format': 'time'},
                },
                'required': ['var_b', 'var_d', 'var_dt', 'var_f', 'var_i',
                             'var_s', 'var_t'],
            }
        })

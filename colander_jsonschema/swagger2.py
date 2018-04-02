# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import colander
from . import base


class Swagger2TypeDispatcher(base.DefinitiveTypeDispatcher):
    converters = {
        colander.Boolean: base.BooleanTypeConverter(),
        colander.Date: base.DateTypeConverter(),
        colander.DateTime: base.DateTimeTypeConverter(),
        colander.Float: base.NumberTypeConverter(),
        colander.Integer: base.IntegerTypeAdapter(),
        colander.Mapping: base.ObjectTypeConverter(),
        colander.Sequence: base.ArrayTypeConverter(),
        colander.String: base.StringTypeConverter(),
        colander.Time: base.TimeTypeConverter(),
    }

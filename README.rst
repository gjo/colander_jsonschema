===================
colander_jsonschema
===================


Convert colander schema to jsonschema compatible dictionary.

Inspired by "Audrey"'s `colanderutil.py`


Install
=======

from PyPI::

  pip install colander_jsonschema


from source::

  python setup.py install


Running
=======

In your source::

  import json
  from colander_jsonschema import convert

  converted = convert(YourColanderSchema())
  with open('some/path.json') as fp:
      json.dump(converted, fp)


TODO: create useful interfaces


Planned Features
================

* auto-discover schemas
* setuptools integration

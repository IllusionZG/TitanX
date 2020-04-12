from __future__ import unicode_literals

import logging
import re
import sys

PY3 = sys.version_info[0] == 3


def to_snake_case(text):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def to_camel_case(text):
    split = text.split('_')
    return split[0] + "".join(x.title() for x in split[1:])


def safe_compare_digest(val1, val2):
    if len(val1) != len(val2):
        return False

    result = 0
    if PY3 and isinstance(val1, bytes) and isinstance(val2, bytes):
        for i, j in zip(val1, val2):
            result |= i ^ j
    else:
        for i, j in zip(val1, val2):
            result |= (ord(i) ^ ord(j))

    return result == 0
import json
import re

import decimal
import importlib

import pandas as pd


def generate_key_value_query(query, key, value):
    return """
        select * from ({q}) t
        where t.{k}='{v}'
    """.format(q=query.replace("false", "0"),k=key, v=value)


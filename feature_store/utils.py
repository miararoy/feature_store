import json
import re

import decimal
import importlib

import pandas as pd

def is_schema_equal(a:dict, b:dict)->bool:
    differences = [k for k in a if k not in b]
    is_equal = len(differences) == 0
    return is_equal

def df_schema(df: pd.core.frame.DataFrame)->dict:
    return {c: str(t) for c,t in zip(df.columns, df.dtypes)}

def generate_key_value_query(query, key, value):
    return """
        select * from ({q}) t
        where t.{k}='{v}'
    """.format(q=query.replace("false", "0").replace("true", "1"),k=key, v=value)


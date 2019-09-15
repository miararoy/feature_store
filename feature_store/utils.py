import json
import re

import decimal
import importlib

import pandas as pd

def is_schema_equal(a:dict, b:dict)->bool:
    """compatres two feature_name->type dicts for schema comparison

    Args:
        a(dict): first schema
        b(dict): second schema
    
    Returns:
        is_equal(bool): true if schema equal else false
    """
    differences = [k for k in a if k not in b]
    is_equal = len(differences) == 0
    return is_equal

def df_schema(df: pd.core.frame.DataFrame)->dict:
    """returns the schema of a data frame

    Args:
        df(pd.DataFrame): dataframe
    
    Returns:
        schema(dict): a feature_name->type dict
    """
    return {c: str(t) for c,t in zip(df.columns, df.dtypes)}

def generate_key_value_query(query, key, value):
    """wraps a sql query with a select where caluse
    such that where key=value
    
    Args:
        query(str): sql query
        key(str): key for where clause
        value(str): value for where clause
    
    Returns:
        new_query(str): a wrapped query
    """
    return """
        select * from ({q}) t
        where t.{k}='{v}'
    """.format(q=query.replace("false", "0").replace("true", "1"),k=key, v=value)


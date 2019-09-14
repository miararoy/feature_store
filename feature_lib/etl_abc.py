import pandas as pd

from abc import abstractmethod, ABC

class AbstractEtl(ABC):
    
    def df_schema(self, df: pd.core.frame.DataFrame)->dict:
        return {c: str(t) for c,t in zip(df.columns, df.dtypes)}
    
    def __init__(self, df: pd.core.frame.DataFrame):
        self.df = df.copy()
        self.schema = self.df_schema(self.df)
        super(AbstractEtl, self).__init__()

    def schema_equals(self, other)-> bool:
        if isinstance(other, AbstractEtl):
            schema = other.schema
        elif isinstance(other, pd.core.frame.DataFrame):
            schema = self.df_schema(other)
        if len(self.schema.keys()) != len(schema.keys()):
            return False
        differences = {k: [self.schema[k], schema[k]] for k in self.schema if k in schema and self.schema[k] != schema[k]}
        is_equal = len(differences) == 0
        return is_equal

    @abstractmethod
    def extract(self) -> pd.core.frame.DataFrame:
        """developer will have to implement this function for feature extraction
        for self.df
        
        Returns:
            df(pf.DataFrame): dataframe after doing feature extraction
        """
        pass

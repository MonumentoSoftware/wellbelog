from pandas import DataFrame


class MnemonicFix:
    """
    Main class for fixing mnemonics.
    Searches for column values and replaces them.
    """
    @staticmethod
    def replace_columns_values(df: DataFrame, characters: set, default: str) -> str:
        """
        Replaces columns values from a given  dataframe, \n
        if it contains a charcter
        froma given set, and replaces it for a default value.
        """

        for original_chr in characters:
            if original_chr in df.columns.values:
                df.rename(columns={original_chr: default}, inplace=True)
        return df

    @staticmethod
    def replace_index(string: str) -> str:
        """
        Replaces index values from a given string.
        """
        if 'INDEX' in string:
            return 'DEPT'
        return string

    @staticmethod
    def depth_rename(df: DataFrame) -> DataFrame:
        """
        Depth rename utility.
        Searches for columns values with whitespaces and renames them.
        """
        if 'DEPT(0)' in df.columns.values:
            df.rename(columns={'DEPT(0)': 'DEPT'}, inplace=True)

        if 'DEPT ' in df.columns.values:
            df.rename(columns={'DEPT ': 'DEPT'}, inplace=True)

        return df

    @staticmethod
    def gamma_rename(df: DataFrame) -> DataFrame:
        """
        GR rename utility.
        Searches for columns values with whitespaces and renames them.
        """

        if 'GR  ' in df.columns.values:
            df.rename(columns={'GR  ': 'GR'}, inplace=True)

        if 'GR ' in df.columns.values:
            df.rename(columns={'GR ': 'GR'}, inplace=True)

        if ' GR ' in df.columns.values:
            df.rename(columns={' GR ': 'GR'}, inplace=True)

        if 'RGR  ' in df.columns.values:
            df.rename(columns={'RGR  ': 'RGR'}, inplace=True)

        if 'RGR ' in df.columns.values:
            df.rename(columns={'RGR ': 'RGR'}, inplace=True)

        if ' RGR ' in df.columns.values:
            df.rename(columns={' RGR ': 'RGR'}, inplace=True)

        return df

    @staticmethod
    def index_to_depth(df: DataFrame) -> DataFrame:
        """
        Index to depth utility.
        This function is specially usefull for Dlis files
        that have index in place of depth.
        """
        for col in df.columns.values:
            if 'INDEX' in col:
                target = col

                df.rename(columns={target: 'DEPT'}, inplace=True)

            if 'INDEX ' in col:
                target = col
                df.rename(columns={target: 'DEPT'}, inplace=True)

        return df

    @staticmethod
    def strip_column_names(df: DataFrame):
        """Rename cols of dataframe by cleaning whitespace"""
        for col in df.columns.values:
            col: str
            df.rename(columns={col: col.lstrip().rstrip()}, inplace=True)

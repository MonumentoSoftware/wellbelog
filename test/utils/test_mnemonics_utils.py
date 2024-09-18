from pathlib import Path

import pandas as pd

from wellbelog.utils.mnemonicfix import MnemonicFix


def test_replace_column_values():
    df = pd.DataFrame({'INDEX': [1, 2, 3, 4, 5]})
    characters = {'INDEX'}
    default = 'DEPT'
    assert MnemonicFix.replace_columns_values(df, characters, default).columns.values == ['DEPT']


def test_mnemonics_utils():
    string_to_fix = 'INDEX'
    assert MnemonicFix.replace_index(string_to_fix) == 'DEPT'


def test_dept_rename():
    df = pd.DataFrame({'DEPT(0)': [1, 2, 3, 4, 5]})
    assert MnemonicFix.depth_rename(df).columns.values == ['DEPT']


def test_gamma_rename():
    df = pd.DataFrame({'GR  ': [1, 2, 3, 4, 5]})
    assert MnemonicFix.gamma_rename(df).columns.values == ['GR']


def test_index_to_depth():
    df = pd.DataFrame({'INDEX': [1, 2, 3, 4, 5]})
    assert MnemonicFix.index_to_depth(df).columns.values == ['DEPT']


def test_strip_column_names():
    df = pd.DataFrame({' DEPT': [1, 2, 3, 4, 5]})
    assert MnemonicFix.strip_column_names(df).columns.values == ['DEPT']

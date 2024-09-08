import pandas as pd
from dlisio.dlis import Measurement, Parameter, Channel
from typing import Union

MetadataObject = Union[Measurement, Parameter, Channel]


def summarize(objs: list[MetadataObject], **kwargs):
    """
    Create a pd.DataFrame that summarize the content of 'objs',
    One object pr. row

    Parameters
    ----------

    objs : list()
        list of metadata objects

    **kwargs
        Keyword arguments
        Use kwargs to tell summarize() which fields (attributes) of the
        objects you want to include in the DataFrame. The parameter name
        must match an attribute on the object in 'objs', while the value
        of the parameters is used as a column name. Any kwargs are excepted,
        but if the object does not have the requested attribute, 'KeyError'
        is used as the value.

    Returns
    -------

    summary : pd.DataFrame
    """
    summary = []
    for key, label in kwargs.items():
        column = []
        for obj in objs:
            try:
                value = getattr(obj, key)
            except AttributeError:
                value = 'KeyError'

            column.append(value)
        summary.append(column)

    summary = pd.DataFrame(summary).T
    summary.columns = kwargs.values()
    return summary

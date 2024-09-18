from typing import Union

from dlisio.dlis import (
    Measurement, Parameter, Channel, LogicalFile,
    Fileheader
)
from rich.console import Console

from wellbelog.schemas.dlis import LogicalFileSummary


MetadataObject = Union[Measurement, Parameter, Channel]

console = Console()


def file_params_to_dict(objs: list[MetadataObject], **kwargs) -> list[dict]:
    """
    Create a a list of dictsthat summarize the content of 'objs',
    One dict per obj

    Parameters
    ----------

    objs : list()
        list of metadata objects

    **kwargs
        Keyword arguments
        Use kwargs to tell the function which fields (attributes) of the\n
        objects you want to include in the DataFrame. The parameter name\n
        must match an attribute on the object in 'objs', while the value\n
        of the parameters is used as a column name. Any kwargs are excepted,\n
        but if the object does not have the requested attribute, 'KeyError'\n
        is used as the value.\n

    Returns
    -------

    dicts_summary : list[dict]
    """
    dicts_summary: list[dict] = []

    for obj in objs:
        obj: Parameter
        obj_dict = {}
        obj_dict['name'] = getattr(obj, 'name')
        obj_dict['long_name'] = getattr(obj, 'long_name')

        try:
            # NOTE Main attribute acees method
            if getattr(obj, 'values').ndim == 1 and getattr(obj, 'values') is not None:  # noqa
                obj_dict['values'] = str(getattr(obj, 'values')[0])

        except IndexError:
            obj_dict['values'] = 'No values were found on this parameter'

        except Exception:
            obj_dict['values'] = 'Error while acessing attribute'

        dicts_summary.append(obj_dict)
    return dicts_summary


def file_tools_to_dict(objs: list[MetadataObject], **kwargs):
    """
    Create a a list of dicts that summarize the content of 'Tools'.

    Parameters
    ----------

    objs : list()
        list of metadata objects

    Returns
    -------

    dicts_summary : list[dict]
    """
    dicts_summary: list[dict] = []
    for obj in objs:
        obj_dict = {}

        obj_dict['name'] = getattr(obj, 'name')
        obj_dict['generic_name'] = getattr(obj, 'generic_name')
        obj_dict['trademark_name'] = getattr(obj, 'trademark_name')
        obj_dict['description'] = getattr(obj, 'description')

        dicts_summary.append(obj_dict)
    return dicts_summary


def file_remarks(logical_file: LogicalFile) -> dict:
    """
    Gets the remarks on a given logical file

    Args:
        logical_file (LogicalFile): The logical file to be searched

    Returns:
        list[dict]: a list of the remarks
    """
    remars_dict_list = {}
    try:
        remarks = logical_file.find('PARAMETER', '^R[0-9]{1,2}')
        remarks = sorted(remarks, key=lambda x: int(x.name[1:]))
        for remark in remarks:
            if remark.name == 'R8':
                continue
            remark_dict = {}
            if remark.values.ndim == 1 and remark.values is not None:
                remark_dict[remark.name] = " ".join(remark.values
                                                    ).encode('utf-8'
                                                             ).decode('utf-8')
                remars_dict_list.update(remark_dict)
    except Exception as e:
        console.log(f'[bold on red] {e}')
        pass

    return remars_dict_list


def get_logical_file_summary(logical_file: LogicalFile) -> LogicalFileSummary:
    """
    ## Master function
    It combines the previous functions, into a pipeline.\n
    This function creates various lists of dictionaries,
    that  reflects the objects that it contains.

    Args:
        logical_file (dlis.LogicalFile): A dlisio.dlis.LogicalFile.

        main_parameters (list[str]): A list of the main parameters
        that should be displayed

    Returns:
        LogicalFileSummary: A LogicalFile Summary object.
    """

    parameters_dict_list = file_params_to_dict(logical_file.parameters)

    # NOTE Creating the tools dict.
    tools_dict_list = file_tools_to_dict(logical_file.tools)

    # NOTE Getting the header
    header: Fileheader = logical_file.fileheader
    header = header.describe().__str__()

    # NOTE Creating the comments dict.
    comments = {'comment': co.text for co in logical_file.comments}

    # NOTE Creating the remarks dict.
    remars_dict_list = file_remarks(logical_file)

    return LogicalFileSummary(
        parameters=parameters_dict_list,
        tools=tools_dict_list,
        remarks=remars_dict_list,
        comments=comments,
        header=header
    )

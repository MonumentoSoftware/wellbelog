from typing import Union

from dlisio import lis
import pandas as pd


def read_lis_file(path_to_file: str) -> Union[lis.PhysicalFile, Exception]:
    """
    Read a LIS file and return a list of LogicalFile objects.

    Args:
        path_to_file (str): Path to the LIS file.

    Returns:
        list[lis.LogicalFile]: List of LogicalFile objects.
    """
    try:
        return lis.load(path_to_file)
    except Exception as e:
        return e


def parse_lis_physical_file(file: lis.PhysicalFile) -> list[lis.LogicalFile]:
    """
    Transform a LIS physical file into a list of LIS logical files.
    """
    *f, = file
    return f


def get_lis_data_spec(file: lis.LogicalFile) -> Union[lis.DataFormatSpec, list[lis.DataFormatSpec]]:
    """
    Get the data specification of a LIS file.

    Args:
        file (lis.LogicalFile): A LIS file.

    Returns:
        dict: Data specification of the LIS file.
    """
    try:
        dataspec = file.data_format_specs()
        if len(dataspec) == 1:
            return dataspec[0]
        return dataspec

    except Exception as e:
        print(e)


def get_physical_lis_specs(physical_file: lis.LogicalFile, attrs: list[str]) -> list[dict[str, str]]:
    """
    Get the attributes of a LIS file.

    Args:
        physical_file (lis.PhysicalFile): A LIS physical file.
        attrs (list[str]): List of attributes to be extracted.

    Returns:
        list[dict[str, str]]: A list of dictionaries, where each dictionary represents a block of attributes.
            Each dictionary contains the specified attributes as keys and their corresponding values as values.
    """
    result = []
    spec = get_lis_data_spec(physical_file)
    if not spec:
        return result
    if isinstance(spec, lis.DataFormatSpec):
        specs = [spec]
    elif isinstance(spec, list):
        specs = spec
    else:
        return result

    for s in specs:
        for block in s.specs:
            block_dict = {}
            for atr in attrs:
                if hasattr(block, atr):
                    value = getattr(block, atr)
                    if isinstance(value, str):
                        value = value.strip()
                    block_dict[atr] = value
            result.append(block_dict)

    result = [dict(t) for t in {tuple(d.items()) for d in result}]
    return result


def get_lis_wellsite_components(logical_file: lis.LogicalFile) -> list[dict]:
    """
    Retrieves the components of each record in a logical file.

    Args:
        logical_file (lis.LogicalFile): The logical file containing the records.

    Returns:
        list[dict]: A list of dictionaries, where each dictionary represents a component of a record.
            Each dictionary contains the following keys:
                - 'mnemonic': The mnemonic of the component.
                - 'units': The units of the component.
                - 'component': The component value.

    """
    records = logical_file.wellsite_data()
    file_records = []
    for record in records:
        component = record.components()
        component_dict = {}
        for c in component:
            component_dict['mnemonic'] = c.mnemonic.strip() if isinstance(c.mnemonic, str) else str(c.mnemonic).strip()
            component_dict['units'] = c.units.strip() if isinstance(c.units, str) else str(c.units).strip()
            component_dict['component'] = c.component.strip() if isinstance(c.component, str) else str(c.component).strip()
        file_records.append(component_dict)
    return file_records


def get_curves(logical_file: lis.LogicalFile) -> list[pd.DataFrame]:
    """
    Get the curves of a LIS file.

    Args:
        logical_file (lis.LogicalFile): A LIS file.

    Returns:
        pd.DataFrame: A DataFrame containing the curves.
    """
    try:
        format_specs = logical_file.data_format_specs()

        if len(format_specs) == 1:
            format_spec = format_specs[0]
            sample_rates = format_spec.sample_rates()
            if len(sample_rates) == 1:
                sample_rate = sample_rates
                data = lis.curves(logical_file, format_spec)
                df = pd.DataFrame(data)
                df.columns = df.columns.str.strip()
                return [df]
        else:
            dfs = []
            for format_spec in format_specs:
                sample_rates = format_spec.sample_rates()
                for sample_rate in sample_rates:
                    data = lis.curves(logical_file, format_spec, sample_rate)
                    df = pd.DataFrame(data)
                    df.columns = df.columns.str.strip()
                    dfs.append(df)
            return dfs
    except Exception as e:
        print(e)

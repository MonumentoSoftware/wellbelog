from dlisio import dlis


def open_dlis_file(file_path: str) -> dlis.PhysicalFile:
    """
    Opens the DLIS file at the specified file path and returns a dlis.PhysicalFile object.

    Parameters:
        file_path (str): The path to the DLIS file.

    Returns:
        dlis.PhysicalFile: The opened DLIS file.

        Exception: If there is an error while loading the DLIS file.
    """
    try:
        return dlis.load(file_path)

    except Exception as e:
        raise e


def unpack_physical_dlis(ph_file: dlis.PhysicalFile) -> list[dlis.LogicalFile]:
    """
    Unpacks the physical file and returns a list of logical files
    """
    *logical_files, = ph_file
    return logical_files

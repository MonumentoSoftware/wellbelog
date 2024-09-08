
from dlisio.dlis import PhysicalFile
from .sumaries import PhysicalFileSummary


def get_physical_file_summary(physical_file: PhysicalFile,
                              well: str,
                              file_path: str) -> PhysicalFileSummary:
    """
    This function transforms the .describe method of the PhisicalFile
    into a list of strings and a dict, made with the values
    from the descripition

    Args:
        physical_file (PhysicalFile): A dlis.PhysicalFile
        well (str): A sring representing the well
        file_path (str): The file_name

    Returns:
        PhysicalFileSummary: A PhysicalFile fast summary
    """
    master_dicts = {'well': well, 'file_path': file_path}

    # NOTE Getting the physical file descripition
    physical_desc = physical_file.describe().__str__()
    # - Splitting the lines
    lines = physical_desc.__str__().split('\n')
    for line in lines:
        try:
            line = line.split(':')
            # XXX This is strange but it works
            # It is a hacked whitespace tool, for enhancing the process
            key_ = line[0].replace('    ', '').replace(
                '     ', '').replace('  ', '').strip(
            ).lower().replace(' ', '_')

            master_dicts.update({key_: line[1]})

        except Exception:
            return None

    return PhysicalFileSummary(physical_desc, master_dicts)

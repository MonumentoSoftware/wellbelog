from pathlib import Path
from dlisio import lis

from wellbelog.belolis.functions import read_lis_file, parse_lis_physical_file

folder_path = Path(__file__).parent.parent / 'test_files'
file_path = f'{folder_path}/1-MPE-3-AL.lis'


def test_read_file():
    lis_physical = read_lis_file(file_path)
    assert isinstance(lis_physical, lis.PhysicalFile)


def test_parse_physical_file():
    lis_physical = read_lis_file(file_path)
    lis_logical = parse_lis_physical_file(lis_physical)
    assert isinstance(lis_logical, list)
    assert isinstance(lis_logical[0], lis.LogicalFile)
    assert len(lis_logical) > 0

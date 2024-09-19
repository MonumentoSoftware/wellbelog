from pathlib import Path

from dlisio import dlis

from wellbelog.belodlis.functions import unpack_physical_dlis, open_dlis_file

folder_path = Path(__file__).parent.parent / 'test_files'
file_path = folder_path / '1PIR1AL_conv_ccl_canhoneio.dlis'


def test_open_dlis_file():
    physical_file = open_dlis_file(file_path)
    assert isinstance(physical_file, dlis.PhysicalFile)
    logical_files = unpack_physical_dlis(physical_file)
    assert isinstance(logical_files, list)
    assert len(logical_files) > 0
    assert isinstance(logical_files[0], dlis.LogicalFile)

from pathlib import Path

from dlisio import dlis

from wellbelog.belodlis.reader import DlisReader

folder_path = Path(__file__).parent.parent / 'test_files'
file_path = folder_path / '1PIR1AL_conv_ccl_canhoneio.dlis'


def test_dlis_physical_schema():
    dlis_processor = DlisReader()
    physical_file = dlis_processor.process_physical_file(file_path)
    assert physical_file.file_name == '1PIR1AL_conv_ccl_canhoneio.dlis'
    assert physical_file.logical_files_count > 0

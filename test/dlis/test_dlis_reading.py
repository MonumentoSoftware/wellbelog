from pathlib import Path
from wellbelog.belodlis.reader import DlisReader

folder_path = Path(__file__).parent.parent / 'test_files'
file_path = folder_path / 'test_files' / '1PIR1AL_conv_ccl_canhoneio.dlis'


def test_search_files():
    dlis_processor = DlisReader()
    dlis_files = dlis_processor.search_files(folder_path)
    assert len(dlis_files) == 1
    assert dlis_files[0].name == '1PIR1AL_conv_ccl_canhoneio.dlis'


def test_read_dlis_file():
    dlis_processor = DlisReader()
    physical_file = dlis_processor.process_physical_file(file_path)
    assert physical_file.file_name == '1PIR1AL_conv_ccl_canhoneio.dlis'

from pathlib import Path

from dlisio import dlis

from wellbelog.belodlis.reader import DlisReader

folder_path = Path(__file__).parent.parent / 'test_files'
file_path = folder_path / '1PIR1AL_conv_ccl_canhoneio.dlis'


def test_search_files():
    dlis_processor = DlisReader()
    dlis_files = dlis_processor.search_files(folder_path)
    assert len(dlis_files) == 1
    assert dlis_files[0].name == '1PIR1AL_conv_ccl_canhoneio.dlis'


def test_read_dlis_file():
    dlis_processor = DlisReader()
    physical_file = dlis_processor.process_physical_file(file_path)
    assert physical_file.file_name == '1PIR1AL_conv_ccl_canhoneio.dlis'


def test_raw_read():
    dlis_processor = DlisReader()
    raw = dlis_processor.load_raw(file_path)
    assert isinstance(raw, dlis.PhysicalFile)


def load_raw_unpack():
    dlis_processor = DlisReader()
    logical = dlis_processor.load_raw(file_path, unpack=True)
    assert isinstance(logical, list)
    assert isinstance(logical[0], dlis.LogicalFile)
    assert len(logical) > 0

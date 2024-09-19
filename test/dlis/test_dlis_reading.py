from pathlib import Path

from dlisio import dlis
import pytest

from wellbelog.belodlis.reader import DlisReader

folder_path = Path(__file__).parent.parent / 'test_files'
file_path = folder_path / '1PIR1AL_conv_ccl_canhoneio.dlis'
error_file_path = folder_path / '1PIR1AL_conv_ccl_canhoneio-error.dlis'


def test_search_files():
    dlis_processor = DlisReader()
    dlis_files = dlis_processor.search_files(folder_path)
    assert len(dlis_files) == 2
    assert '1PIR1AL_conv_ccl_canhoneio.dlis' and '1PIR1AL_conv_ccl_canhoneio-error.dlis' in [file.name for file in dlis_files]

    # Testing the search_files method with a wrong path
    dlis_files = dlis_processor.search_files(folder_path / 'wrong_path')
    assert not len(dlis_files)


def test_read_dlis_file():
    dlis_processor = DlisReader()
    physical_file = dlis_processor.process_physical_file(file_path)
    assert physical_file.file_name == '1PIR1AL_conv_ccl_canhoneio.dlis'


def test_read_dlis_file_error():
    dlis_processor = DlisReader()
    physical_file = dlis_processor.process_physical_file(error_file_path)
    assert physical_file.error
    assert physical_file.error_message is not None
    assert physical_file.file_name == '1PIR1AL_conv_ccl_canhoneio-error.dlis'
    assert physical_file.logical_files_count == 0


def test_raw_read():
    dlis_processor = DlisReader()
    raw = dlis_processor.load_raw(file_path)
    assert isinstance(raw, dlis.PhysicalFile)


def test_raw_read_error():
    with pytest.raises(Exception):
        dlis_processor = DlisReader()
        dlis_processor.load_raw(error_file_path)


def load_raw_unpack():
    dlis_processor = DlisReader()
    logical = dlis_processor.load_raw(file_path, unpack=True)
    assert isinstance(logical, list)
    assert isinstance(logical[0], dlis.LogicalFile)
    assert len(logical) > 0

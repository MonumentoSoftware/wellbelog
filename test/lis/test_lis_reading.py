from pathlib import Path

from dlisio import lis

from wellbelog.belolis.reader import LisReader

folder_path = Path(__file__).parent.parent / 'test_files'
file_path = f'{folder_path}/1-MPE-3-AL.lis'


def test_search_files():
    lis_processor = LisReader()
    lis_files = lis_processor.search_files(folder_path)
    assert len(lis_files) == 1
    assert lis_files[0].name == '1-MPE-3-AL.lis'


def test_lis_reading():
    reader = LisReader()
    file = reader.process_physical_file(file_path)
    assert file.file_name == '1-MPE-3-AL.lis'
    assert file.folder_name is None
    assert file.error is False


def test_raw_reading():
    reader = LisReader()
    raw = reader.load_raw(file_path)
    assert isinstance(raw, lis.PhysicalFile)


def test_raw_unpacking():
    reader = LisReader()
    logical = reader.load_raw(file_path, unpack=True)
    assert isinstance(logical, list)
    assert isinstance(logical[0], lis.LogicalFile)
    assert len(logical) > 0

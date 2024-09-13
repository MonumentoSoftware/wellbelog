from pathlib import Path
from wellbelog.belolis.reader import LisReader

folder_path = Path(__file__).parent.parent / 'test_files'


def test_search_files():
    lis_processor = LisReader()
    lis_files = lis_processor.search_files(folder_path)
    assert len(lis_files) == 1
    assert lis_files[0].name == '1-MPE-3-AL.lis'


def test_lis_reading():
    reader = LisReader()
    file = reader.process_physical_file(f'{folder_path}/1-MPE-3-AL.lis')
    assert file.file_name == '1-MPE-3-AL.lis'
    assert file.folder_name is None
    assert file.error is False

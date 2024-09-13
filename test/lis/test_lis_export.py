import pathlib
import tempfile

from wellbelog.belolis.reader import LisReader

folder_path = pathlib.Path(__file__).parent.parent / 'test_files'
file_path = f'{folder_path}/1-MPE-3-AL.lis'


def test_lis_to_csv():
    reader = LisReader()
    file = reader.process_physical_file(file_path)
    assert file.file_name == '1-MPE-3-AL.lis'
    assert file.error is False

    logical_file = file.logical_files[1]
    assert logical_file.file_name == '1-MPE-3-AL.lis'
    assert logical_file.error is False

    curve_data = logical_file.frames[1]
    with tempfile.TemporaryDirectory() as tmpdirname:
        csv_path = f'{tmpdirname}/1-MPE-3-AL.csv'
        curve_data.to_csv(csv_path)
        assert pathlib.Path(csv_path).is_file()
        assert pathlib.Path(csv_path).stat().st_size > 0

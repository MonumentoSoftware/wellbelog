from wellbelog.main_reader import MainReader
from pathlib import Path

folder_path = Path(__file__).parent / 'test_files'
lis = f'{folder_path}/1-MPE-3-AL.lis'
dlis = f'{folder_path}/1PIR1AL_conv_ccl_canhoneio.dlis'
las = f'{folder_path}/1-MPE-3-AL.las'


def test_main_reader():

    reader = MainReader()
    lis_file = reader.load_file(lis)
    assert lis_file.file_name == '1-MPE-3-AL.lis'

    dlis_file = reader.load_file(dlis)
    assert dlis_file.file_name == '1PIR1AL_conv_ccl_canhoneio.dlis'

    las_file = reader.load_file(las)
    assert las_file.file_name == '1-MPE-3-AL.las'

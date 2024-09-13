from pathlib import Path
from wellbelog.belolas.reader import LasReader

folder_path = Path(__file__).parent.parent / 'test_files'


def test_search_files():
    las_processor = LasReader()
    las_files = las_processor.search_files(folder_path)
    assert len(las_files) == 1
    assert las_files[0].name == '1-MPE-3-AL_hals-dslt-tdd-hgns-gr_resistividade_repetida.las'


def test_las_reading():

    manager = LasReader()
    las_file = manager.process_las_file(folder_path / '1-MPE-3-AL_hals-dslt-tdd-hgns-gr_resistividade_repetida.las')
    assert las_file.file_name == '1-MPE-3-AL_hals-dslt-tdd-hgns-gr_resistividade_repetida.las'

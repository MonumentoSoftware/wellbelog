from pathlib import Path

from lasio import LASFile

from wellbelog.belolas.functions import open_las_file, process_curves_items
from wellbelog.schemas.las import LasCurvesSpecs


folder_path = Path(__file__).parent.parent / 'test_files'
file_path = folder_path / '1-MPE-3-AL_hals-dslt-tdd-hgns-gr_resistividade_repetida.las'


def test_open_las_file():
    las_file = open_las_file(file_path)
    assert isinstance(las_file, LASFile)


def test_process_curves_items():
    las_file = open_las_file(file_path)
    curves = process_curves_items(las_file)
    assert isinstance(curves, list)
    assert len(curves) > 0
    assert isinstance(curves[0], LasCurvesSpecs)

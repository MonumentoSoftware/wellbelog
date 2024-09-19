from pathlib import Path

from rich.table import Table

from wellbelog.belolas.reader import LasReader
from wellbelog.schemas.las import LasCurvesSpecs, LasFileModel

folder_path = Path(__file__).parent.parent / 'test_files'
file_path = folder_path / '1-MPE-3-AL_hals-dslt-tdd-hgns-gr_resistividade_repetida.las'


def test_lasfile_schema():
    reader = LasReader()
    las_file = reader.process_las_file(file_path)
    assert isinstance(las_file, LasFileModel)

    curves = las_file.curves_names
    assert isinstance(curves, list)
    assert 'DEPT' in las_file.curves_names

    gr_curve = las_file.get_curve('GR')
    assert isinstance(gr_curve, LasCurvesSpecs)


def test_tableview():
    reader = LasReader()
    las_file = reader.process_las_file(file_path)
    table = las_file.table_view()
    assert isinstance(table, Table)
    assert ['File Name', 'Curves', 'Error'] == [column.header for column in table.columns]

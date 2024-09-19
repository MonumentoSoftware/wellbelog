from pathlib import Path


from wellbelog.belolis.reader import LisReader
from wellbelog.schemas.lis import PhysicalLisFileModel, LogicalLisFileModel, FrameLisCurves

folder_path = Path(__file__).parent.parent / 'test_files'
file_path = f'{folder_path}/1-MPE-3-AL.lis'

# Lis File Curvs = ['SP', 'ABHV', 'ITT', 'TT4', 'GR', 'TT1', 'TT3', 'TT2', 'DEPT', 'DT', 'TBHV', 'XCAL', 'DIR', 'YCAL', 'SN']


def test_lis_physical_model_methods():
    reader = LisReader()
    file = reader.process_physical_file(file_path)

    assert isinstance(file, PhysicalLisFileModel)
    assert file.file_name == '1-MPE-3-AL.lis'
    assert file.folder_name is None
    assert file.error is False
    assert file.error_message is None
    assert file.logical_files_count > 0
    assert 'SP' in file.curves_names


def test_physical_file_table():
    reader = LisReader()
    file = reader.process_physical_file(file_path)
    table = file.logical_files_table()
    assert table.columns[0].header == 'File Name'
    assert table.columns[1].header == 'Curves'
    assert table.columns[2].header == 'Error'
    assert len(table.columns) == 3
    assert len(table.rows) == file.logical_files_count
    assert table.title == '1-MPE-3-AL.lis'


def test_lis_logical_file_methods():
    reader = LisReader()
    file = reader.process_physical_file(file_path)
    logical_file = file.logical_files[1]
    assert isinstance(logical_file, LogicalLisFileModel)
    assert logical_file.file_name == '1-MPE-3-AL.lis'
    assert logical_file.error is False
    assert logical_file.error_message is None

    sp_curve = logical_file.get_frame()
    assert sp_curve is not None
    assert isinstance(sp_curve, FrameLisCurves)

    assert logical_file.frames_count == len(logical_file.frames)


def test_lis_logical_file_table():
    reader = LisReader()
    file = reader.process_physical_file(file_path)
    logical_file = file.logical_files[1]
    table = logical_file.table_view()
    assert table.columns[0].header == 'Logical File ID'
    assert table.columns[1].header == 'Frames'
    assert table.columns[2].header == 'Curves'
    assert table.columns[3].header == 'Error'
    assert table.title == '1-MPE-3-AL.lis'

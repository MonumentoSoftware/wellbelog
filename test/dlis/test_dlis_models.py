from pathlib import Path

import pandas as pd

from wellbelog.belodlis.reader import DlisReader
from wellbelog.schemas.dlis import FrameModel

folder_path = Path(__file__).parent.parent / 'test_files'
file_path = folder_path / '1PIR1AL_conv_ccl_canhoneio.dlis'


def test_dlis_physical_schema():
    dlis_processor = DlisReader()
    physical_file = dlis_processor.process_physical_file(file_path)
    assert physical_file.file_name == '1PIR1AL_conv_ccl_canhoneio.dlis'

    assert physical_file.logical_files_count > 0

    assert physical_file.curves_names is not None

    # We already know that the file has the CCL curve
    # Test file curves = ['LTEN', 'TDEP', 'LSPD', 'MINMK', 'CCL']
    assert 'CCL' in physical_file.curves_names


def test_logical_files_table():
    dlis_processor = DlisReader()
    physical_file = dlis_processor.process_physical_file(file_path)
    table = physical_file.logical_files_table()
    assert table.columns[0].header == 'File Name'
    assert table.columns[1].header == 'Curves'
    assert table.columns[2].header == 'Error'
    assert len(table.columns) == 3
    assert len(table.rows) == physical_file.logical_files_count
    assert table.title == '1PIR1AL_conv_ccl_canhoneio.dlis'


def test_logical_file_schema_methods():
    reader = DlisReader()
    physical_file = reader.process_physical_file(file_path)
    logical_file = physical_file.logical_files[0]
    # Logical File curves names = ['TDEP', 'LSPD', 'LTEN', 'CCL', 'MINMK']
    assert logical_file.file_name == '1PIR1AL_conv_ccl_canhoneio.dlis'
    assert logical_file.error is False
    assert logical_file.error_message is None

    # NOTE Testing Curves names
    assert logical_file.curves_names is not None
    assert 'CCL' in logical_file.curves_names

    # NOTE Testing Frames counting
    assert logical_file.frames_count == len(logical_file.frames)

    assert isinstance(logical_file.frames[0], FrameModel)

    # NOTE Testing table view
    table = logical_file.table_view()
    assert table.columns[0].header == 'Logical File ID'
    assert table.columns[1].header == 'File Name'
    assert table.columns[2].header == 'Frames'
    assert table.columns[3].header == 'Curves'
    assert table.columns[4].header == 'Error'


def test_frame_schema_methods():
    reader = DlisReader()
    physical_file = reader.process_physical_file(file_path)
    logical_file = physical_file.logical_files[0]
    frame = logical_file.frames[0]

    assert frame.logical_file_id == logical_file.logical_id
    assert isinstance(frame.data.as_df(), pd.DataFrame)

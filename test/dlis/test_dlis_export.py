from pathlib import Path
from wellbelog.belodlis.reader import DlisReader
import tempfile


folder_path = Path(__file__).parent.parent / 'test_files'
file_path = folder_path / '1PIR1AL_conv_ccl_canhoneio.dlis'


def test_exports():
    dlis_processor = DlisReader()
    physical_file = dlis_processor.process_physical_file(file_path)
    assert physical_file.file_name == '1PIR1AL_conv_ccl_canhoneio.dlis'

    file_curves = physical_file.curves_names()
    # Getting the first curve
    frame = physical_file.logical_files[0].get_frame()
    assert frame is not None
    with tempfile.TemporaryDirectory() as temp_dir:

        csv_path = Path(temp_dir) / 'test.csv'
        physical_file.logical_files[0].get_frame().data.to_csv(csv_path)
        assert csv_path.exists()
        assert csv_path.is_file()
        assert csv_path.stat().st_size > 0

        # Check the column names
        with open(csv_path, 'r') as f:
            columns = f.readline().strip().split(',')
            if 'FRAMENO' in columns:
                columns.remove('FRAMENO')
            for _, column in enumerate(columns):
                assert file_curves.__contains__(column)

from pathlib import Path
from wellbelog.belolas.reader import LasReader
import tempfile


folder_path = Path(__file__).parent.parent / 'test_files'
file_path = folder_path / '1-MPE-3-AL_hals-dslt-tdd-hgns-gr_resistividade_repetida.las'


def test_exports():
    dlis_processor = LasReader()
    las_file = dlis_processor.process_las_file(file_path)
    assert las_file.file_name == '1-MPE-3-AL_hals-dslt-tdd-hgns-gr_resistividade_repetida.las'
    assert las_file.error is False

    las_data = las_file.data
    assert las_data is not None

    las_file_columns = las_data.columns
    with tempfile.TemporaryDirectory() as temp_dir:

        csv_path = Path(temp_dir) / 'test.csv'
        las_data.to_csv(csv_path)
        assert csv_path.exists()
        assert csv_path.is_file()
        assert csv_path.stat().st_size > 0

        # Check the column names
        with open(csv_path, 'r') as f:
            columns = f.readline().strip().split(',')
            for _, column in enumerate(columns):
                assert las_file_columns.__contains__(column)

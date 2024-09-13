
from wellbelog.belolas.reader import LasReader  # noqa


if __name__ == '__main__':
    PATH_TO_FILE = r'test\test_files\1-MPE-3-AL_hals-dslt-tdd-hgns-gr_resistividade_repetida.las'

    reader = LasReader()
    file = reader.process_las_file(PATH_TO_FILE)
    print(file.file_name)
    print(file.table_view())

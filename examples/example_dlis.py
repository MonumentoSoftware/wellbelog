
from wellbelog.belodlis.reader import DlisReader  # noqa


if __name__ == '__main__':
    PATH_TO_FILE = r'test\test_files\1PIR1AL_conv_ccl_canhoneio.dlis'

    reader = DlisReader()
    file = reader.process_physical_file(PATH_TO_FILE)
    print(file.file_name)
    print(file.logical_files_table())
    table = file.logical_files_table()

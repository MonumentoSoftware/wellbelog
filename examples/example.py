
from wellbelog.belolis.reader import LisReader  # noqa


if __name__ == '__main__':
    PATH_TO_FILE = r'test\test_files\1-MPE-3-AL.lis'

    reader = LisReader()
    file = reader.process_physical_file(PATH_TO_FILE)
    print(file.file_name)
    print(file.logical_files_table())

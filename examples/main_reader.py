from wellbelog.main_reader import MainReader


PATH_TO_FILE = r'test\test_files\1PIR1AL_conv_ccl_canhoneio.dlis'

if __name__ == '__main__':
    reader = MainReader()
    file = reader.load_file(PATH_TO_FILE)
    print(file.file_name)

import sys
sys.path.append('..')

from wellbelog.belodlis.reader import DlisReader  # noqa


if __name__ == '__main__':
    PATH_TO_FILE = r'C:\Users\Usuário\pedro\Monumento-master\well-belo-log\test\test_files\1PIR1AL_conv_ccl_canhoneio.dlis'

    reader = DlisReader()
    file = reader.process_physical_file(PATH_TO_FILE)
    print(file.logical_files[0].get_frame().data.data[0])

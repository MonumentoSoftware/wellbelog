import sys
import os

from rich.console import Console
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


if __name__ == '__main__':
    from webelog.belodlis.dlis import DlisManager

    PATH_TO_FILE = r'examples\test_files\1PIR1AL_conv_ccl_canhoneio.dlis'

    console = Console()
    manager = DlisManager()
    dlis_file = manager.process_physical_file(PATH_TO_FILE)
    console.log(dlis_file)

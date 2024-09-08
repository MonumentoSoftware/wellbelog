import sys
import os

from rich.console import Console
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


if __name__ == '__main__':
    from webelog.belolas.manager import LasDataManager

    PATH_TO_FILE = r'examples\test_files\1-MPE-3-AL_hals-dslt-tdd-hgns-gr_resistividade_repetida.las'

    console = Console()
    manager = LasDataManager()
    las_file = manager.process_las_file(PATH_TO_FILE)
    console.log(las_file)

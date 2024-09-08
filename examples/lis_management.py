import sys
import os

from rich.console import Console
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

if __name__ == '__main__':
    from webelog.belolis.manager import LisManager

    PATH_TO_FILE = r""

    console = Console()
    lis_manager = LisManager()
    lis_obj = lis_manager.process_physical_file(PATH_TO_FILE)
    console.log(lis_obj)

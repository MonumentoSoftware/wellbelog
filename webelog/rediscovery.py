
import sys
from dlisio import dlis


path_to_file = r"C:\Users\Usuário\pedro\Monumento-master\DATA\ALAGOAS\Categoria-1\1-BC-1-AL\Perfil Convencional\1BC__0001__AL_1BC__0001__AL.dlis"  # noqa

FOLDER_DIR = r"C:\Users\Usuário\pedro\Monumento-master\DATA\ALAGOAS\Categoria-1"

AGP_PATH = r'C:\Users\Usuário\pedro\pedrokpaxo_github\AGP_Parser'
sys.path.append(AGP_PATH)


def unpack_physical_dlis(ph_file: dlis.PhysicalFile) -> list[dlis.LogicalFile]:
    """
    Unpacks the physical file and returns a list of logical files
    """
    *logical_files, = ph_file
    return logical_files


if __name__ == '__main__':
    from webelog.utils.console import console
    from webelog.belodlis.dlis import DlisManager

    processor = DlisManager()
    physical_file = processor.process_physical_file(path_to_file)
    console.log(physical_file)

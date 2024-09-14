import pathlib
from typing import Callable, Union


from .belodlis.reader import DlisReader
from .belolas.reader import LasReader
from .belodlis.schemas import PhysicalFileModel
from .belolas.schemas import LasFileModel
from .belolis.reader import LisReader
from .belolis.schemas import PhysicalLisFileModel
from .utils.logging import setup_logger

ReaderReturnType = Union[PhysicalFileModel, LasFileModel, PhysicalLisFileModel]
ReaderMethod = Callable[[str], ReaderReturnType]


class MainReader:
    """
    Class responsible for managing LIS, LAS, DLIS, and TIFF files.
    """

    def __init__(self) -> None:
        self.logger = setup_logger(__class__.__name__)
        self.dlis_reader = DlisReader()
        self.las_reader = LasReader()
        self.lis_reader = LisReader()

    def load_file(self, path: str) -> ReaderReturnType:
        """
        Load a file and return a list of LogicalFile objects based on its extension.

        Args:
            path (str): Path to the file.

        Returns:
            list[LogicalFile]: List of LogicalFile objects.
        """
        file_extension = pathlib.Path(path).suffix.lower()

        if file_extension == '.lis':
            return self._attempt_reading(path, self.lis_reader.process_physical_file, self.dlis_reader.process_physical_file)
        elif file_extension == '.las':
            return self._attempt_reading(path, self.las_reader.process_las_file)
        elif file_extension == '.dlis':
            return self._attempt_reading(path, self.dlis_reader.process_physical_file, self.lis_reader.process_physical_file)
        elif file_extension == '.tiff':
            return self._attempt_reading(path, self.dlis_reader.process_physical_file, self.lis_reader.process_physical_file)
        else:
            self.logger.error(f"Unsupported file type: {file_extension}")
            raise ValueError(f"Unsupported file type: {file_extension}")

    def _attempt_reading(self, path: str, primary_reader: ReaderMethod, fallback_reader: ReaderMethod = None) -> ReaderReturnType:
        """
        Attempt to read the file with a primary reader. If it fails and a fallback is provided, try with the fallback.

        Args:
            path (str): Path to the file.
            primary_reader (callable): Primary function to read the file.
            fallback_reader (callable, optional): Fallback function if the primary fails.

        Returns:
            list[LogicalFile]: List of LogicalFile objects.
        """
        try:
            return primary_reader(path)

        except Exception as primary_error:
            self.logger.error(f"Primary reader failed for file {path}: {primary_error}")
            if fallback_reader:
                self.logger.info(f"Attempting to read {path} with fallback reader.")
                try:
                    return fallback_reader(path)
                except Exception as fallback_error:
                    self.logger.error(f"Fallback reader also failed for file {path}: {fallback_error}")
                    raise
            else:
                raise

    def read_tiff_file(self, path: str) -> ReaderReturnType:
        """
        Reads a TIFF file, first attempting with DLIS reader, then falling back to LIS reader.

        Args:
            path (str): Path to the TIFF file.

        Returns:
            list[LogicalFile]: List of LogicalFile objects.
        """
        return self._attempt_reading(path, self.dlis_reader.process_physical_file, self.lis_reader.process_physical_file)

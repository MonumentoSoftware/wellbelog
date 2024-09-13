import json
import pathlib

from wellbelog.utils.logging import setup_logger
from .schemas.las import LasFileModel, LasDataframe
from .functions import open_las_file, process_curves_items


class LasReader:
    """
    Class responsible for creating a LasFileModel object from a physical file.
    """

    def __init__(self) -> None:
        self.logger = setup_logger(__class__.__name__)

    def search_files(self, path: str) -> list[pathlib.Path]:
        """
        Search for LAS files in the given path and returns a list with the file paths.

        Args:
            path (str): The path to the folder where the LAS files are located.

        Returns:
            list[pathlib.Path]: A list with the file paths.

        Raises:
            None.
        """
        las_files = []
        try:
            for file in pathlib.Path(path).rglob('*.las'):
                las_files.append(file)
            return las_files
        except Exception as e:
            self.logger.error(f'Error while searching for LAS files: {e}')
            return las_files

    def process_las_file(self, path: str) -> LasFileModel:
        """
        Processes a physical file and returns a LasFileModel object.

        Args:
            path (str): The path to the file.

        Returns:
            LasFileModel: A LasFileModel object representing the file.

        Raises:
            None.
        """
        # Create a LasFileModel object with the file name
        file_name = pathlib.Path(path).name
        las_file_model = LasFileModel(file_name=file_name)

        # Open the LAS file
        file = open_las_file(path)

        # NOTE If the file has any error, return the error message
        if isinstance(file, Exception):
            las_file_model.error = True
            las_file_model.error_message = file
            return las_file_model

        try:
            las_data = file.df()
            shape_data = las_data.shape
            las_curves_specs = process_curves_items(file)
            las_file_model.specs = las_curves_specs

            las_dataframe = LasDataframe(
                data=json.loads(las_data.to_json(orient='records')),
                file_name=file_name,
                columns=file.keys(),
                shape=shape_data
            )
            las_file_model.data = las_dataframe
            return las_file_model

        except Exception as e:
            self.logger.error(f'Error while processing LAS file: {e}')
            las_file_model.error = True
            las_file_model.error_message = str(e)
            return las_file_model

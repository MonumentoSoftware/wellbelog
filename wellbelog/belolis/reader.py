import json
import pathlib
from typing import Union

from dlisio import lis

from wellbelog.utils.logging import setup_logger
from .functions import read_lis_file, parse_lis_physical_file, get_curves, get_physical_lis_specs, get_lis_wellsite_components
from ..schemas.lis import (
    FrameLisCurves, LisLogicalFileSpecsDict, LisLogicalFileWellSiteSpecDict,
    PhysicalLisFileModel, LisLogicalWellSiteSpec, LOGICAL_FILE_ATTR,
    LogicalLisFileModel, LisLogicalSpecs
)


class LisReader:
    """
    Class responsible for managing LIS files.

    Attributes:
        logger: The logger instance for logging messages.

    Methods:
        process_physical_file: Reads a LIS file and returns a list of LogicalFile objects.
    """

    def __init__(self) -> None:
        self.logger = setup_logger(__class__.__name__)

    def search_files(self, path: str) -> list[pathlib.Path]:
        """
        Search for LIS files in the given path and returns a list with the file paths.

        Args:
            path (str): The path to the folder where the LIS files are located.

        Returns:
            list[pathlib.Path]: A list with the file paths.
        """
        lis_files = []
        try:
            for file in pathlib.Path(path).rglob('*.lis'):
                lis_files.append(file)
            return lis_files
        except Exception as e:
            self.logger.error(f'Error while searching for LIS files: {e}')
            return lis_files

    def load_raw(self, path_to_file: str, unpack=False) -> Union[lis.PhysicalFile, list[lis.LogicalFile]]:
        """
        Load a LIS file and return the raw data.
        Optionally, unpack the file and return the logical files.

        Args:
            path_to_file (str): Path to the LIS file.

        Returns:
            Union[lis.PhysicalFile, list[lis.LogicalFile]]: The raw data.
        """
        file = read_lis_file(path_to_file)
        if isinstance(file, Exception):
            self.logger.error(f'Error while opening the LIS file: {file}')
            raise file
        if unpack:
            return parse_lis_physical_file(file)
        return file

    def process_physical_file(self, path_to_file: str, folder_name: str = None) -> PhysicalLisFileModel:
        """
        Read a LIS file and return a list of LogicalFile objects.

        Args:
            path_to_file(str): Path to the LIS file.

        Returns:
            list[lis.LogicalFile]: List of LogicalFile objects.
        """
        file_name = pathlib.Path(path_to_file)
        assert file_name.is_file(), f"File {file_name} not found."
        file = PhysicalLisFileModel(file_name=file_name.name, logical_files=[], folder_name=folder_name)

        # Reading the LIS file
        physical = read_lis_file(path_to_file)
        # NOTE Handling exceptions, if any, mark the file as errored and return it
        if isinstance(physical, Exception):
            self.logger.error(f"Error reading file: {physical}")
            self.logger.error(physical)
            file.error = True
            file.error_message = "Error reading file"
            return file

        # NOTE Unpacking the physical file
        logical_files = parse_lis_physical_file(physical)

        # XXX Creating LogicalFile objects
        for logical_file in logical_files:
            logical_file_id = logical_files.index(logical_file)

            logical_file_model = LogicalLisFileModel(
                file_name=file_name.name,
                logical_id=logical_file_id,
            )
            logical_file_model.header = logical_file.header()

            # NOTE Getting well site specifications
            well_specs = [d for d in get_lis_wellsite_components(logical_file)]
            _specs_dicts = [LisLogicalFileWellSiteSpecDict(**spec) for spec in well_specs]
            well_site_specs = LisLogicalWellSiteSpec(file_name=file_name.name, logical_id=logical_file_id, specs_dicts=_specs_dicts)  # noqa

            logical_file_model.well_site_specs = well_site_specs
            # NOTE Getting the curves
            try:
                # NOTE Getting the physical file specifications
                physical_specs = [LisLogicalFileSpecsDict(**spec) for spec in get_physical_lis_specs(logical_file, LOGICAL_FILE_ATTR)]  # noqa
                lis_logical_specs = LisLogicalSpecs(file_name=file_name.name, logical_id=logical_file_id, specs_dicts=physical_specs)  # noqa
                logical_file_model.specs = lis_logical_specs
                curves = get_curves(logical_file)
                curves_set_names = set()
                for curve in curves:
                    curve_model = FrameLisCurves(
                        file_name=file_name.name,
                        logical_file_id=logical_file_id,
                        data=json.loads(curve.to_json(orient="records")),
                    )
                    logical_file_model.frames.append(curve_model)
                    for curve_name in curve.columns:
                        curves_set_names.add(curve_name)
                logical_file_model.curves_names = list(curves_set_names)
                file.logical_files.append(logical_file_model)

            # NOTE Handling exceptions, if any, and appending the error to the error_files list
            except Exception as e:
                logical_file_model.error = True
                logical_file_model.error_message = str(e)
                file.error_files.append(logical_file_model)
                self.logger.error(f"Error processing file: {e}")
                continue

        return file

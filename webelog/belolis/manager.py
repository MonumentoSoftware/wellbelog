

import pathlib
from webelog.utils.logging import setup_logger
from .base import read_lis_file, parse_lis_physical_file, get_curves, get_physical_lis_specs, get_lis_wellsite_components
from .schemas.lis import (
    FrameLisCurves, LisLogicalFileSpecsDict, LisLogicalFileWellSiteSpecDict,
    PhysicalLisFileModel, LisLogicalWellSiteSpec, LOGICAL_FILE_ATTR,
    LogicalLisFileModel, LisLogicalSpecs
)


class LisManager:
    """
    Class responsible for managing LIS files.

    Attributes:
        logger: The logger instance for logging messages.

    Methods:
        __init__: Initializes the LisManager object.
        process_physical_file: Reads a LIS file and returns a list of LogicalFile objects.
    """

    def __init__(self) -> None:
        self.logger = setup_logger("LisManager")

    def process_physical_file(self, path_to_file: str, folder_name: str = None) -> PhysicalLisFileModel:
        """
        Read a LIS file and return a list of LogicalFile objects.

        Args:
            path_to_file (str): Path to the LIS file.

        Returns:
            list[lis.LogicalFile]: List of LogicalFile objects.
        """
        # NOTE Creating a file name from the path
        file_name = pathlib.Path(path_to_file).name
        file = PhysicalLisFileModel(file_name=file_name, logical_files=[], folder_name=folder_name)

        # Reading the LIS file
        physical = read_lis_file(path_to_file)

        # NOTE Handling exceptions, if any, mark the file as errored and return it
        if isinstance(physical, Exception):
            self.logger.error(f"Error reading file: {physical}")
            file.error = True
            file.error_message = "Error reading file"
            return file

        # NOTE Unpacking the physical file
        logical_files = parse_lis_physical_file(physical)

        # XXX Creating LogicalFile objects
        for logical_file in logical_files:
            logical_file_id = logical_files.index(logical_file)

            logical_file_model = LogicalLisFileModel(
                file_name=file_name,
                logical_id=logical_file_id,
            )
            logical_file_model.header = logical_file.header()

            # NOTE Getting well site specifications
            well_specs = [d for d in get_lis_wellsite_components(logical_file)]
            well_site_specs = LisLogicalWellSiteSpec(file_name=file_name, logical_id=logical_file_id, specs_dicts=[LisLogicalFileWellSiteSpecDict(**spec) for spec in well_specs])  # noqa

            logical_file_model.well_site_specs = well_site_specs
            # NOTE Getting the curves
            try:
                # NOTE Getting the physical file specifications
                physical_specs = [LisLogicalFileSpecsDict(**spec) for spec in get_physical_lis_specs(logical_file, LOGICAL_FILE_ATTR)]  # noqa
                lis_logical_specs = LisLogicalSpecs(file_name=file_name, logical_id=logical_file_id, specs_dicts=physical_specs)  # noqa
                logical_file_model.specs = lis_logical_specs
                curves = get_curves(logical_file)
                curve_model = FrameLisCurves(
                    file_name=file_name,
                    logical_file_id=logical_file_id,
                    data=curves.to_json(orient="records"),
                )
                logical_file_model.curves.append(curve_model)
                file.logical_files.append(logical_file_model)

            # NOTE Handling exceptions, if any, and appending the error to the error_files list
            except Exception as e:
                logical_file_model.error = True
                logical_file_model.error_message = str(e)
                file.error_files.append(logical_file_model)
                continue

        return file

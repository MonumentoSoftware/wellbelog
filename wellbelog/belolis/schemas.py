from typing import Any, Union, Optional

from pydantic import BaseModel, Field
from rich.table import Table

from wellbelog.utils.console import console
from ..db.base_schema import TimeStampedModelSchema, DataframeSchema

LOGICAL_FILE_ATTR = [
    'api_curve_class', 'api_curve_type', 'api_log_type',
    'api_modifier', 'filenr', 'mnemonic', 'process_level',
    'reprc', 'reserved_size', 'samples', 'service_id', 'service_order_nr', 'units'
]


class FrameLisCurves(DataframeSchema):
    """
    A class used to represent a BeloDlis object.

    Attributes:
        physical (dlis.PhysicalFile): The physical file.
        logical_files (list[dlis.LogicalFile]): The logical files.
        file_name (str): The name of the file.
        path_reference (str): The reference path.
    """

    file_name: str = Field(..., description="The name of the file.")
    logical_file_id: Union[str, int] = Field(..., description="The id of the logical file.")


class LisLogicalFileWellSiteSpecDict(BaseModel):
    """
    Represents the specification for a LIS logical file.
    Like the well name, wellbore name and wellbore number.
    """
    mnemonic: Optional[str] = Field(None, description="mnemonic")
    units: Optional[str] = Field(None, description="units")
    component: Optional[str] = Field(None, description="component information")


class LisLogicalWellSiteSpec(BaseModel):
    file_name: str = Field(..., description="The name of the file.")
    logical_id: Union[str, int] = Field(..., description="The id of the logical file.")
    specs_dicts: list[LisLogicalFileWellSiteSpecDict] = Field(default_factory=list, description="The specification of the file.")  # noqa


class SimpleLisLogicalFileSpec(BaseModel):
    """
    Represents the specification for a LIS logical file.
    Like the curve mnemonic, units and number of samples.
    """
    mnemonic: Optional[str] = Field(None, description="Mnemonic")
    units: Optional[str] = Field(None, description="Units")
    samples: Optional[int] = Field(None, description="Number of Samples")


class LisLogicalFileSpecsDict(BaseModel):
    """
    Represents the specification for a LIS logical file.
    But with more details.
    """
    api_curve_class: Optional[Union[str, int]] = Field(None, description="API Curve Class")
    api_curve_type: Optional[Union[str, int]] = Field(None, description="API Curve Type")
    api_log_type: Optional[Union[str, int]] = Field(None, description="API Log Type")
    api_modifier: Optional[Union[str, int]] = Field(None, description="API Modifier")
    filenr: Optional[int] = Field(None, description="File Number")
    mnemonic: Optional[str] = Field(None, description="Mnemonic")
    process_level: Optional[int] = Field(None, description="Process Level")
    reprc: Optional[Union[str, int]] = Field(None, description="Reprocessing")
    reserved_size: Optional[int] = Field(None, description="Reserved Size")
    samples: Optional[int] = Field(None, description="Number of Samples")
    service_id: Optional[Union[str, int]] = Field(None, description="Service ID")
    service_order_nr: Optional[Union[str, int]] = Field(None, description="Service Order Number")
    units: Optional[Union[str, int]] = Field(None, description="Units")

    def simple(self) -> SimpleLisLogicalFileSpec:
        return SimpleLisLogicalFileSpec(
            mnemonic=self.mnemonic,
            units=self.units,
            samples=self.samples
        )


class LisLogicalSpecs(BaseModel):
    file_name: str = Field(..., description="The name of the file.")
    logical_id: Union[str, int] = Field(..., description="The id of the logical file.")
    specs_dicts: list[LisLogicalFileSpecsDict] = Field(default_factory=list, description="The specification of the file.")


class LogicalLisFileModel(TimeStampedModelSchema):
    """
    Represents a logical LIS file.
    It can have multiple frames. But generally only one.

    Attributes:
        file_name (str): The name of the file.
        logical_id (str): The id of the logical file.
        frames (list[FrameLisCurves]): The frames of the file.
        error (bool): If the file has any error during opening.
        error_message (str): The error exception if any.
        well_site_specs (LisLogicalWellSiteSpec): The well site specifications.
        specs (list[Any]): The specification of the file.
        header (str): The header of the file.
    """

    file_name: str = Field(..., description="The name of the file.")
    logical_id: Optional[Any] = Field(..., description="The id of the logical file.")
    frames: list[FrameLisCurves] = Field(default_factory=list, description="The frames of the file.")
    curves_names: list[str] = Field(default_factory=list, description="The names of the curves.")
    error: bool = Field(False, description="If the file has any error during opening.")
    error_message: Optional[str] = Field(None, description="The error exception if any.")
    well_site_specs: Optional[LisLogicalWellSiteSpec] = Field(None, description="The well site specifications.")
    specs: list[Any] = Field(None, description="The specification of the file.")
    header: Optional[str] = Field(None, description="The header of the file.")

    @property
    def frames_count(self) -> int:
        return len(self.frames)

    def get_curve(self, index=0) -> FrameLisCurves:
        assert index < self.frames_count, f"Index {index} is out of range. The file has {self.frames_count} frames."
        if self.frames_count == 1:
            return self.frames[0]
        return self.frames[index]

    def table_view(self) -> Table:
        """
        Create a table view of the file.
        """
        table = Table(title=self.file_name)
        table.add_column("Logical File ID", style="cyan")
        table.add_column("Frame count", style="magenta")
        table.add_column("Curves", style="green")
        table.add_column("Error", style="red")
        table.add_row(str(self.logical_id), str(self.frames_count), str(self.curves_names), str(self.error))
        console.print(table)
        return table


class PhysicalLisFileModel(TimeStampedModelSchema):
    """
    Represents a physical LIS file.
    It can have multiple logical files. And each logical file can have multiple frames, but generally only one.

    Attributes:
        file_name (str): The name of the file.
        folder_name (str): The name of the folder.
        logical_files (list[LogicalLisFileModel]): The logical files.
        error_files (list[LogicalLisFileModel]): The error files.
        error (bool): If the file has any error during opening.
        error_message (str): The error exception if any.
    """

    file_name: str = Field(..., description="The name of the file.")
    folder_name: Optional[str] = Field(None, description="The name of the folder.")
    logical_files: Optional[list[LogicalLisFileModel]] = Field(default_factory=list, description="The logical files.")
    error_files: Optional[list[LogicalLisFileModel]] = Field(default_factory=list, description="The error files.")
    error: bool = Field(False, description="If the file has any error during opening.")
    error_message: Optional[str] = Field(None, description="The error exception if any.")

    @property
    def logical_files_count(self) -> int:
        return len(self.logical_files)

    def get_curves_names(self) -> list[str]:
        curves = []
        for logical_file in self.logical_files:
            for frame in logical_file.frames:
                curves.append(frame.file_name)
        return curves

    def logical_files_table(self) -> Table:
        """
        Get a table view of the logical files.
        """
        table = Table(title=self.file_name)
        table.add_column("File Name", style="green")
        table.add_column("Curves", style="cyan")
        table.add_column("Error", style="red")
        for file in self.logical_files:
            table.add_row(file.file_name, str(file.curves_names), str(file.error))
        console.print(table)
        return table

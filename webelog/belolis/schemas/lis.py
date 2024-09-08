from typing import Any, Union, Optional
from pydantic import BaseModel, Field

from webelog.base import TimeStampedModelSchema

LOGICAL_FILE_ATTR = [
    'api_curve_class', 'api_curve_type', 'api_log_type',
    'api_modifier', 'filenr', 'mnemonic', 'process_level',
    'reprc', 'reserved_size', 'samples', 'service_id', 'service_order_nr', 'units'
]


class FrameLisCurves(TimeStampedModelSchema):
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
    data: Union[list[dict], str] = Field(None, description="The dataframe of the file.")


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
    api_curve_class: Optional[Union[str, int]] = Field(..., description="API Curve Class")
    api_curve_type: Optional[Union[str, int]] = Field(..., description="API Curve Type")
    api_log_type: Optional[Union[str, int]] = Field(..., description="API Log Type")
    api_modifier: Optional[Union[str, int]] = Field(..., description="API Modifier")
    filenr: Optional[int] = Field(..., description="File Number")
    mnemonic: Optional[str] = Field(..., description="Mnemonic")
    process_level: Optional[int] = Field(..., description="Process Level")
    reprc: Optional[Union[str, int]] = Field(..., description="Reprocessing")
    reserved_size: Optional[int] = Field(..., description="Reserved Size")
    samples: Optional[int] = Field(..., description="Number of Samples")
    service_id: Optional[Union[str, int]] = Field(..., description="Service ID")
    service_order_nr: Optional[Union[str, int]] = Field(..., description="Service Order Number")
    units: Optional[Union[str, int]] = Field(..., description="Units")

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
    A class used to represent a BeloDlis object.

    Attributes:
        file_name (str): The name of the file.
        path_reference (str): The reference path
    """

    file_name: str = Field(..., description="The name of the file.")
    logical_id: Optional[Any] = Field(..., description="The id of the logical file.")
    curves: list[FrameLisCurves] = Field(default_factory=list, description="The frames of the file.")
    error: bool = Field(False, description="If the file has any error during opening.")
    error_message: Optional[str] = Field(None, description="The error exception if any.")
    well_site_specs: Optional[LisLogicalWellSiteSpec] = Field(None, description="The well site specifications.")
    specs: list[Any] = Field(None, description="The specification of the file.")
    header: Optional[str] = Field(None, description="The header of the file.")

    @property
    def frames_count(self) -> int:
        return len(self.curves)


class PhysicalLisFileModel(TimeStampedModelSchema):
    """
    A class used to represent a BeloDlis object.

    Attributes:
        file_name (str): The name of the file.
        logical_files (list[dlis.LogicalFile]): The logical files.
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

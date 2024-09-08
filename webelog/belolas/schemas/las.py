from typing import Any, Optional
from pydantic import BaseModel, Field

from mongoDriver.base import TimeStampedModelSchema


class LasDataframe(TimeStampedModelSchema):

    file_name: str = Field(..., description="The name of the file.")
    data: str = Field(..., description="The data of the curve.")
    columns: list[str] = Field(..., description="The columns of the curve.")
    shape: tuple = Field(..., description="The shape of the curve.")


class LasCurvesSpecs(BaseModel):
    """
    A class used to represent a BeloDlis object.

    Attributes:
        mnemonic (str): The mnemonic of the curve.
        unit (str): The unit of the curve.
        description (str): The description of the curve.
    """

    mnemonic: str = Field(..., description="The mnemonic of the curve.")
    unit: str = Field(..., description="The unit of the curve.")
    descr: str = Field(..., description="The description of the curve.")
    value: Optional[Any] = Field(None, description="The value of the curve.")
    original_mnemonic: Optional[str] = Field(None, description="The original mnemonic of the curve.")
    shape: Optional[tuple] = Field(None, description="The shape of the curve.")


class LasFileModel(TimeStampedModelSchema):
    """
    A class used to represent a BeloDlis object.

    Attributes:
        file_name (str): The name of the file.
        logical_files (list[dlis.LogicalFile]): The logical files.
    """

    file_name: str = Field(..., description="The name of the file.")
    folder_name: Optional[str] = Field(None, description="The name of the folder.")
    specs: list[LasCurvesSpecs] = Field([], description="The curves specs.")
    error: bool = Field(False, description="If the file has any error during opening.")
    error_message: Optional[str] = Field(None, description="The error exception if any.")

    data: Optional[LasDataframe] = Field(None, description="The data of the file.")

    @property
    def logical_files_count(self) -> int:
        return len(self.logical_files)

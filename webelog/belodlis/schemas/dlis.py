from typing import Any, Union, Optional
from pydantic import Field

from mongoDriver.base import TimeStampedModelSchema


class FrameChannel(TimeStampedModelSchema):
    """
    Dataclass to acess channel data from Frames objects.
    """

    long_name: str = Field(None, description="The long name of the channel")
    name: str = Field(None, description="The name of the channel")
    units: str = Field(None, description="The units of the channel")
    repr: str = Field(None, description="The representation of the channel")
    properties: Union[str, Any] = Field(None, description="The properties of the channel")

    data: Any = Field(None, description="The data of the channel")


ChannelsList = list[FrameChannel]


class FrameDataframe(TimeStampedModelSchema):
    """
    A class used to represent a BeloDlis object.

    Attributes:
        physical (dlis.PhysicalFile): The physical file.
        logical_files (list[dlis.LogicalFile]): The logical files.
        file_name (str): The name of the file.
        path_reference (str): The reference path.
    """

    file_name: str = Field(..., description="The name of the file.")
    logical_file_id: str = Field(..., description="The id of the logical file.")
    data: list[dict] = Field(None, description="The dataframe of the file.")


class FrameModel(TimeStampedModelSchema):
    """
    A class used to represent a BeloDlis object.

    Attributes:
        physical (dlis.PhysicalFile): The physical file.
        logical_files (list[dlis.LogicalFile]): The logical files.
        file_name (str): The name of the file.
        path_reference (str): The reference path.
    """

    file_name: str = Field(..., description="The name of the file.")
    logical_file_id: str = Field(..., description="The id of the logical file.")
    description: Optional[str] = Field(None, description="The description of the file.")
    channels: ChannelsList = Field(None, description="The channels of the file.")
    error: bool = Field(False, description="If the file has any error during opening.")
    error_message: Optional[str] = Field(None, description="The error exception if any.")
    data: Optional[FrameDataframe] = Field(None, description="The dataframe of the file.")


class LogicalFileSummary(TimeStampedModelSchema):
    """
    A class used to represent a a Logical File Summary.

    Attributes:
        file_id (Union[str, int]): The file id of the file.
        parameters (Optional[list]): List of dicts with the parameters of the file.
        tools (Optional[list]): List of dicts with the tools of the file.
        remarks (Optional[dict]): List of dicts with the remarks of the file.
        comments (Optional[dict]): List of dicts with the comments of the file.
        header (Optional[str]): String with the header of the file.
        frames (Optional[list]): List of dicts with the frames of the file.
    """
    tools: Optional[list] = Field(None, alias='tools', help='List of dicts with the tools of the file')
    remarks: Optional[dict] = Field(None, alias='remarks', help='List of dicts with the remarks of the file')
    comments: Optional[dict] = Field(None, alias='comments', help='List of dicts with the comments of the file')
    header: Optional[str] = Field(None, alias='header', help='String with the header of the file')

    class Config:

        arbitrary_types_allowed = True
        description = "The summary of the file."


class LogicalFileModel(TimeStampedModelSchema):
    """
    A class used to represent a BeloDlis object.

    Attributes:
        file_name (str): The name of the file.
        path_reference (str): The reference path
    """

    file_name: str = Field(..., description="The name of the file.")
    logical_id: Any = Field(..., description="The id of the logical file.")
    summary: LogicalFileSummary = Field(..., description="The summary of the file.")
    frames: list[FrameModel] = Field(None, description="The frames of the file.")
    error: bool = Field(False, description="If the file has any error during opening.")
    error_message: Optional[str] = Field(None, description="The error exception if any.")

    @property
    def frames_count(self) -> int:
        return len(self.frames)


class PhysicalFileModel(TimeStampedModelSchema):
    """
    A class used to represent a BeloDlis object.

    Attributes:
        file_name (str): The name of the file.
        logical_files (list[dlis.LogicalFile]): The logical files.
    """

    file_name: str = Field(..., description="The name of the file.")
    error: bool = Field(False, description="If the file has any error during opening.")
    error_message: Optional[str] = Field(None, description="The error exception if any.")
    logical_files: Optional[list[LogicalFileModel]] = Field(default_factory=list, description="The logical files.")
    error_files: Optional[list[LogicalFileModel]] = Field(default_factory=list, description="The error files.")

    @property
    def logical_files_count(self) -> int:
        return len(self.logical_files)

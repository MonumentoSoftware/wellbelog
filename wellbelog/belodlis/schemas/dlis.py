from typing import Any, Union, Optional

import pandas as pd
from pydantic import Field
from rich.table import Table

from wellbelog.db.base import TimeStampedModelSchema
from wellbelog.utils.console import console


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
"""List of FrameChannel objects."""


class FrameDataframe(TimeStampedModelSchema):
    """
    The Dlis frame data.

    Attributes:
        file_name (str): The name of the file.
        logical_file_id (str): The id of the logical file.
        data (list[dict]): The dataframe of the file.
    """

    file_name: str = Field(..., description="The name of the file.")
    logical_file_id: str = Field(..., description="The id of the logical file.")
    data: list[dict] = Field(None, description="The dataframe of the file.")

    def as_df(self):
        """
        Convert the FrameDataframe to a pandas DataFrame.

        Returns:
            pd.DataFrame: The pandas DataFrame.
        """

        try:
            return pd.DataFrame(self.data)
        except Exception as e:
            raise e


class FrameModel(TimeStampedModelSchema):
    """
    A class used to represent a Dlis Frame.

    Attributes:
        file_name (str): The name of the file.
        logical_file_id (str): The id of the logical file.
        description (Optional[str]): The description of the file.
        channels (ChannelsList): The channels of the file.
        error (bool): If the file has any error during opening.
        error_message (Optional[str]): The error exception if any.
        data (Optional[FrameDataframe]): The dataframe of the file.
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
    tools: Optional[list] = Field(None, alias='tools')
    remarks: Optional[dict] = Field(None, alias='remarks')
    comments: Optional[dict] = Field(None, alias='comments')
    header: Optional[str] = Field(None, alias='header')

    model_config = {
        'arbitrary_types_allowed': True,
    }


class LogicalFileModel(TimeStampedModelSchema):
    """
    A Logical File Model.
    It contains the frames and the file name.Also, the summary of the file is included.
    If any error occurs during the opening, the error flag is set to True. The error message is also set.

    Attributes:
        file_name (str): The name of the file.
        logical_id (Any): The id of the logical file.
        summary (LogicalFileSummary): The summary of the file.
        frames (list[FrameModel]): The frames of the file.
        error (bool): If the file has any error during opening.
        error_message (Optional[str]): The error exception if any.
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

    def get_frame(self, index: int = 0) -> FrameModel:
        """
        Get the frame by index.
        In the vast majority of the cases, the file has only one frame.
        """
        if self.frames_count == 1:
            return self.frames[0]
        return self.frames[index]

    def to_csv(self, index: int = 0, **kwargs) -> str:
        """
        Convert the frame to a csv file.
        Args:
            index (int): The index of the frame.
            **kwargs: The arguments to pass to the pandas to_csv method.
        Returns:
            str: The csv file.
        """
        assert index < self.frames_count, f"Index {index} out of range. The file has {self.frames_count} frames."
        return self.get_frame(index).data.as_df().to_csv(**kwargs)

    def table_view(self) -> Table:
        """
        Get a table view of the file.
        """
        table = Table(title=self.file_name)
        table.add_column("Logical File ID", style="cyan")
        table.add_column("File Name", style="magenta")
        table.add_column("Frames", style="green")
        table.add_column("Error", style="red")
        table.add_row(str(self.logical_id), self.file_name, str(self.frames_count), str(self.error))
        console.print(table)
        return table


class PhysicalFileModel(TimeStampedModelSchema):
    """
    A representation of a Physical File.
    It contains the logical files and the file name.
    If any error occurs during the opening, the error flag is set to True. The error message is also set.

    Attributes:
        file_name (str): The name of the file.
        logical_files (list[dlis.LogicalFile]): The logical files.
        error (bool): If the file has any error during opening.
        error_message (Optional[str]): The error exception if any.
    """

    file_name: str = Field(..., description="The name of the file.")
    error: bool = Field(False, description="If the file has any error during opening.")
    error_message: Optional[str] = Field(None, description="The error exception if any.")
    logical_files: Optional[list[LogicalFileModel]] = Field(default_factory=list, description="The logical files.")
    error_files: Optional[list[LogicalFileModel]] = Field(default_factory=list, description="The error files.")
    mnemonics: Optional[list[str]] = Field(default_factory=list, description="The mnemonics of the file.")

    @property
    def logical_files_count(self) -> int:
        return len(self.logical_files)

    def curves_names(self) -> list[str]:
        """"
        Returns a set with the names of the curves in the file.
        """
        if not self.logical_files or self.error:
            return None
        curves = [channel.name for file in self.logical_files for frame in file.frames for channel in frame.channels]
        return list(set(curves))

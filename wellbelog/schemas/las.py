from functools import cached_property
from typing import Any, Optional

from pydantic import BaseModel, Field
from rich.table import Table

from wellbelog.utils.console import console
from wellbelog.schemas.base_schema import TimeStampedModelSchema, DataframeSchema


class LasDataframe(DataframeSchema):
    """
    A class that represents the data of a LAS file.

    Attributes:
        file_name (str): The name of the file.
        data (str): The data of the curve.
        columns (list[str]): The columns of the curve.
        shape (tuple): The shape of the curve.
    """
    file_name: str = Field(..., description="The name of the file.")
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

    def __str__(self) -> str:
        return f"LasFileModel: {self.file_name}"

    def get_curve(self, column: str) -> Optional[LasCurvesSpecs]:
        """
        Get the curve by the column name.
        If the column is not found, return None.
        Args:
            column (str): The column name.

        Returns:
            Optional[LasCurvesSpecs]: The curve.
        """
        for spec in self.specs:
            if spec.mnemonic == column:
                return spec
        return None

    @cached_property
    def curves_names(self) -> list[str]:
        return [spec.mnemonic for spec in self.specs]

    def table_view(self) -> Table:
        """
        Create a table view of the file.
        """
        table = Table(title=self.file_name)
        table.add_column("File Name", style="green")
        table.add_column("Curves", style="cyan")
        table.add_column("Error", style="red")
        table.add_row(self.file_name, str(self.curves_names), str(self.error),)
        console.print(table)
        return table

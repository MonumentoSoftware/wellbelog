# BeloLis

The BeloLis module is responsible for reading and processing Lis files. The Lis file format is quite old and was the first of the three to be created. Nowadays, it's not so common to find .lis files, but we offer support to it as well. Also, there are some .Tiff files that use the .lis extension.

- [BeloLis](#belolis)
- [Reader](#reader)
- [Models](#models)
  - [PhysicalLisFileModel](#physicallisfilemodel)
  - [LogicalLisFileModel](#logicallisfilemodel)

# Reader

The main class to search and read the lis files.

```python
from webelog.belolis import LisReader

reader = LisReader()
lis_files = reader.search_files('path/to/your/folder')
lis_file = reader.process_lis_file('path/to/your/file.lis')
```

# Models

We make use of Pydantic to create the models.

## PhysicalLisFileModel

The main model, that contains all the information about the sections, curves, etc.

```python
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

```
## LogicalLisFileModel

```python
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
```
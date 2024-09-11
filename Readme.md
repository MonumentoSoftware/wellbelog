![icon](icon.png)
# Well Belo Log
[![Python Package Test](https://github.com/MonumentoSoftware/webelog/actions/workflows/push/badge.svg)](https://github.com/MonumentoSoftware/webelog/actions/workflows/push.yml)

The aim of Well Belo Log is to ease the workflow of dealing with large ammounts of files. It's quite common the need to restart your kernel while trying to acess some data in a closed file. Or maybe the boiler code is just too much, to merge the logical files, extract the frames... Anyway, enjoy...



- [Well Belo Log](#well-belo-log)
- [Installation](#installation)
- [Usage](#usage)
  - [Working with Dlis files](#working-with-dlis-files)
    - [Searching for Dlis Files](#searching-for-dlis-files)
    - [Reading Dlis Files](#reading-dlis-files)
    - [Dlis File Models](#dlis-file-models)
      - [PhysicalFileModel](#physicalfilemodel)
      - [LogicalFileModel](#logicalfilemodel)
      - [FrameModel](#framemodel)
      - [FrameDataframe](#framedataframe)
  - [Working with Las files](#working-with-las-files)
    - [Searching for Las Files](#searching-for-las-files)
    - [Reading Las Files](#reading-las-files)
    - [Las File Models](#las-file-models)
  - [Working with Lis files](#working-with-lis-files)
    - [Searching for Lis Files](#searching-for-lis-files)
    - [Reading Lis Files](#reading-lis-files)


# Installation

You can install the package using pip directly from the github repository:

```bash
pip install https://github.com/MonumentoSoftware/webelog
```

or you can clone the repository and install it locally:

```bash
git clone https://github.com/MonumentoSoftware/webelog
cd webelog
pip install .
```

# Usage
The main objective of WellBeLog is to ease the workflow when working with .dlis, .las and .dlis files. So, there are three main classes that you can use to work with these files. Also, we offer support to .tiff files, via the DlisReader and the LisReader classes.

- DlisReader: to read .dlis files
- LasReader: to read .las files
- LisReader: to read .lis files

## Working with Dlis files
In the [Belodlis](./wellbelog/belodlis/) folder you can find all the tools to work with Dlis files.
The DlisReader class reads the physical file and returns a PhysicalFileModel object, that  contains all the information about the logical files, logical records, channels, frames, etc.

### Searching for Dlis Files
A simple way to search for Dlis files is to use the search_files method. It returns a list of all the Dlis files in the folder.

```python
from webelog.belodlis import DlisReader

reader = DlisReader()
dlis_files = reader.search_files('path/to/your/folder')
```

### Reading Dlis Files
The process_physical_file method returns a PhysicalFileModel object, that contains all the information about the logical files, logical records, channels, frames, etc.

```python
from webelog.belodlis import DlisReader

reader = DlisReader()
dlis_file = reader.process_physical_file('path/to/your/file.dlis')
```

### Dlis File Models
- [Schemas Folder](./wellbelog/belodlis/schemas/)
We make use of Pydantic to create the models. The PhysicalFileModel is the main model, but we have LogicalFileModel to represent the logical files, FrameModel to represent the frames.

#### PhysicalFileModel
The main model, that contains all the information about the logical files, logical records, channels, frames, etc.

```python
class PhysicalFileModel(TimeStampedModelSchema):
    file_name: str = Field(..., description="The name of the file.")
    error: bool = Field(False, description="If the file has any error during opening.")
    error_message: Optional[str] = Field(None, description="The error exception if any.")
    logical_files: Optional[list[LogicalFileModel]] = Field(default_factory=list, description="The logical files.")
    error_files: Optional[list[LogicalFileModel]] = Field(default_factory=list, description="The error files.")
    mnemonics: Optional[list[str]] = Field(default_factory=list, description="The mnemonics of the file.")
```

#### LogicalFileModel
To represent the logical files.

```python	
class LogicalFileModel(TimeStampedModelSchema):
    file_name: str = Field(..., description="The name of the file.")
    logical_id: Any = Field(..., description="The id of the logical file.")
    summary: LogicalFileSummary = Field(..., description="The summary of the file.")
    frames: list[FrameModel] = Field(None, description="The frames of the file.")
    error: bool = Field(False, description="If the file has any error during opening.")
    error_message: Optional[str] = Field(None, description="The error exception if any.")
```
#### FrameModel
To represent the frames.

```python
class FrameModel(TimeStampedModelSchema):
    file_name: str = Field(..., description="The name of the file.")
    logical_file_id: str = Field(..., description="The id of the logical file.")
    description: Optional[str] = Field(None, description="The description of the file.")
    channels: ChannelsList = Field(None, description="The channels of the file.")
    error: bool = Field(False, description="If the file has any error during opening.")
    error_message: Optional[str] = Field(None, description="The error exception if any.")
    data: Optional[FrameDataframe] = Field(None, description="The dataframe of the file.")
```

#### FrameDataframe
To represent the Dataframe.

```python
class FrameDataframe(TimeStampedModelSchema):

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
```

## Working with Las files
In the [Belolas](./wellbelog/belolas/) folder you can find all the tools to work with Las files.
The .las extension is newer than the .dlis extension, and it's a lot simpler to work with. The LasReader class reads the physical file and returns a LasFileModel object, that contains all the information about the sections, curves, etc.

### Searching for Las Files
Use the search_files method to search for Las files in a folder. It returns a list of all the Las files in the folder.

```python
from webelog.belolas import LasReader

reader = LasReader()
las_files = reader.search_files('path/to/your/folder')
```

### Reading Las Files
The process_las_file method returns a LasFileModel object.

```python
from webelog.belolas import LasReader

reader = LasReader()
las_file = reader.process_las_file('path/to/your/file.las')
```

### Las File Models
- [Schemas Folder](./wellbelog/belolas/schemas/)
  
We make use of Pydantic to create the models. The LasFileModel is the main model, but we have SectionModel to represent the sections, CurveModel to represent the curves, etc.

```python
class LasFileModel(TimeStampedModelSchema):
    file_name: str = Field(..., description="The name of the file.")
    folder_name: Optional[str] = Field(None, description="The name of the folder.")
    specs: list[LasCurvesSpecs] = Field([], description="The curves specs.")
    error: bool = Field(False, description="If the file has any error during opening.")
    error_message: Optional[str] = Field(None, description="The error exception if any.")

    data: Optional[LasDataframe] = Field(None, description="The data of the file.")

    def __str__(self) -> str:
        return f"LasFileModel: {self.file_name}"

    def column_search(self, column: str) -> Optional[LasCurvesSpecs]:
        for spec in self.specs:
            if spec.mnemonic == column:
                return spec
        return None
```

## Working with Lis files
Similar do the .Dlis file extension, the lis format is quite old and was the first of the three to be created.
The [BeloLis](./wellbelog/belolis/) folder contains all the tools to work with Lis files.
Nowadays, it's not so common to find .lis files, but we offer support to it as well. Also, there are some .Tiff files that uses the .lis extension.

### Searching for Lis Files
A simple way to search for Lis files is to use the search_files method. It returns a list of all the Lis files in the folder.

```python
from webelog.belolas import LisReader

reader = LisReader()
lis_files = reader.search_files('path/to/your/folder')
```

### Reading Lis Files
The process_lis_file method returns a LisFileModel object.
```python
from webelog.belolas import LisReader

reader = LisReader()
lis_file = reader.process_physical_file('path/to/your/file.lis')
```
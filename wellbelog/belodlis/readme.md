# BelodDLis

Here are all the code to work with the dlis files.

- [BelodDLis](#beloddlis)
- [Reader](#reader)
- [Models](#models)
  - [PhysicalFileModel](#physicalfilemodel)
  - [LogicalFileModel](#logicalfilemodel)
  - [FrameModel](#framemodel)
- [FrameDataframe](#framedataframe)
  - [as\_df](#as_df)
  - [to\_csv](#to_csv)
  - [to\_excel](#to_excel)


# Reader
The main class to search and read the dlis files.

```python
from webelog.belodlis import DlisReader

reader = DlisReader()
dlis_files = reader.search_files('path/to/your/folder')
dlis_file = reader.process_physical_file('path/to/your/file.dlis')
```

# Models
We make use of Pydantic to create the models. 

## PhysicalFileModel
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

## LogicalFileModel
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
## FrameModel
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

# FrameDataframe
To represent the Dataframe.
The data is a list of dictionaries.
```python
class FrameDataframe(TimeStampedModelSchema):

    file_name: str = Field(..., description="The name of the file.")
    logical_file_id: str = Field(..., description="The id of the logical file.")
    data: list[dict] = Field(None, description="The dataframe of the file.")

```

## as_df 
To convert the data to a pandas dataframe.

```python
import pandas as pd
from webelog.belodlis import DlisReader

reader = DlisReader()
dlis_file = reader.process_physical_file('path/to/your/file.dlis')
frame = dlis_file.logical_files[0].get_frame()
df: pd.DataFrame = frame.data.as_df()
```

## to_csv
To save the data to a CSV file.

```python
import pandas as pd
from webelog.belodlis import DlisReader

reader = DlisReader()
dlis_file = reader.process_physical_file('path/to/your/file.dlis')
frame = dlis_file.logical_files[0].get_frame()
frame.data.to_csv('path/to/your/file.csv')

# NOTE the function returns the path to the file.
path_to_csv = frame.data.to_csv('path/to/your/file.csv')
```

## to_excel
To save the data to an Excel file.

```python
import pandas as pd
from webelog.belodlis import DlisReader


reader = DlisReader()
dlis_file = reader.process_physical_file('path/to/your/file.dlis')
frame = dlis_file.logical_files[0].get_frame()
frame.data.to_excel('path/to/your/file.xlsx')

# NOTE the function returns the path to the file.
path_to_excel = frame.data.to_excel('path/to/your/file.xlsx')
```



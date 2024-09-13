![icon](icon.png)
# Well Belo Log
[![Python Package Test](https://github.com/MonumentoSoftware/wellbelog/actions/workflows/push.yml/badge.svg)](https://github.com/MonumentoSoftware/wellbelog/actions/workflows/push.yml)

The aim of Well Belo Log is to ease the workflow of dealing with large ammounts of files. It's quite common the need to restart your kernel while trying to acess some data in a closed file. Or maybe the boiler code is just too much, to merge the logical files, extract the frames... Anyway, enjoy...



- [Well Belo Log](#well-belo-log)
- [Installation](#installation)
- [Usage](#usage)
  - [Working with Dlis files](#working-with-dlis-files)
    - [Searching for Dlis Files](#searching-for-dlis-files)
    - [Reading Dlis Files](#reading-dlis-files)
    - [to dataframe](#to-dataframe)
    - [to csv](#to-csv)
    - [to excel](#to-excel)
    - [Dlis File Models](#dlis-file-models)
      - [PhysicalFileModel](#physicalfilemodel)
      - [LogicalFileModel](#logicalfilemodel)
      - [FrameModel](#framemodel)
      - [FrameDataframe](#framedataframe)
  - [Working with Las files](#working-with-las-files)
    - [Searching for Las Files](#searching-for-las-files)
    - [Reading Las Files](#reading-las-files)
    - [Frame data to dataframe](#frame-data-to-dataframe)
    - [Frame data to csv](#frame-data-to-csv)
    - [Frame data to excel](#frame-data-to-excel)
    - [Las File Models](#las-file-models)
      - [LasFileModel](#lasfilemodel)
      - [LasDataframe](#lasdataframe)
  - [Working with Lis files](#working-with-lis-files)
    - [Searching for Lis Files](#searching-for-lis-files)
    - [Reading Lis Files](#reading-lis-files)
    - [Frame data to dataframe](#frame-data-to-dataframe-1)
    - [Frame data to csv](#frame-data-to-csv-1)
    - [Frame data to excel](#frame-data-to-excel-1)
- [Developing the project](#developing-the-project)
- [Academic Sponsors](#academic-sponsors)


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
### to dataframe 
To convert the data to a pandas dataframe.

```python
import pandas as pd
from webelog.belodlis import DlisReader

reader = DlisReader()
dlis_file = reader.process_physical_file('path/to/your/file.dlis')
frame = dlis_file.logical_files[0].get_frame()
df: pd.DataFrame = frame.data.as_df()
```

### to csv
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

### to excel
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

### Dlis File Models
- [Schemas Folder](./wellbelog/belodlis/schemas/)
We make use of Pydantic to create the models. The PhysicalFileModel is the main model, but we have LogicalFileModel to represent the logical files, FrameModel to represent the frames.
Here are the main models:

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
The FrameDataframe class extends the DataframeSchema, that has a method to convert the data to a pandas DataFrame.
And exports the data to a CSV file or to a Excel file.
```python
class FrameDataframe(DataframeSchema):

    file_name: str = Field(..., description="The name of the file.")
    logical_file_id: str = Field(..., description="The id of the logical file.")
    data: list[dict] = Field(None, description="The dataframe of the file.")

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
### Frame data to dataframe
To convert the data to a pandas dataframe.

```python
import pandas as pd
from webelog.belolas import LasReader

reader = LasReader()
las_file = reader.process_las_file('path/to/your/file.las')
df: pd.DataFrame = las_file.data.as_df()
```

### Frame data to csv
To save the data to a CSV file.

```python
import pandas as pd
from webelog.belolas import LasReader

reader = LasReader()
las_file = reader.process_las_file('path/to/your/file.las')
las_file.data.to_csv('path/to/your/file.csv')

# NOTE the function returns the path to the file.
path_to_csv = las_file.data.to_csv('path/to/your/file.csv')
```

### Frame data to excel
To save the data to an Excel file.

```python
import pandas as pd
from webelog.belolas import LasReader

reader = LasReader()
las_file = reader.process_las_file('path/to/your/file.las')
las_file.data.to_excel('path/to/your/file.xlsx')

# NOTE the function returns the path to the file.
path_to_excel = las_file.data.to_excel('path/to/your/file.xlsx')
```

### Las File Models
- [Schemas](./wellbelog/belolas/schemas/las.py)
  
We make use of Pydantic to create the models. The LasFileModel is the main model, but we have SectionModel to represent the sections, CurveModel to represent the curves, etc.

#### LasFileModel
A class to represent the Las file.
It contains the file name, the folder name, the specs, the data, and some error handling.

```python
class LasFileModel(TimeStampedModelSchema):
    file_name: str = Field(..., description="The name of the file.")
    folder_name: Optional[str] = Field(None, description="The name of the folder.")
    specs: list[LasCurvesSpecs] = Field([], description="The curves specs.")
    error: bool = Field(False, description="If the file has any error during opening.")
    error_message: Optional[str] = Field(None, description="The error exception if any.")

    data: Optional[LasDataframe] = Field(None, description="The data of the file.")

    def column_search(self, column: str) -> Optional[LasCurvesSpecs]:
        for spec in self.specs:
            if spec.mnemonic == column:
                return spec
        return None
```
#### LasDataframe
A class to represent the Dataframe.
It extends the DataframeSchema, that has a method to convert the data to a pandas DataFrame.
And exports the data to a CSV file or to a Excel file.

```python
class LasDataframe(DataframeSchema):
    file_name: str = Field(..., description="The name of the file.")
    columns: list[str] = Field(..., description="The columns of the curve.")
    shape: tuple = Field(..., description="The shape of the curve.")
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

### Frame data to dataframe
To convert the data to a pandas dataframe.

```python
import pandas as pd
from webelog.belolas import LisReader

reader = LisReader()
lis_file = reader.process_lis_file('path/to/your/file.lis')
df: pd.DataFrame = lis_file.logical_files[0].curves_data[0].as_df()
```

### Frame data to csv
To save the data to a CSV file.

```python
import pandas as pd
from webelog.belolas import LisReader

reader = LisReader()
lis_file = reader.process_lis_file('path/to/your/file.lis')
lis_file.logical_files[0].curves_data[0].to_csv('path/to/your/file.csv')

# NOTE the function returns the path to the file.
path_to_csv = lis_file.logical_files[0].curves_data[0].to_csv('path/to/your/file.csv')
```

### Frame data to excel
To save the data to an Excel file.

```python
import pandas as pd
from webelog.belolas import LisReader

reader = LisReader()
lis_file = reader.process_lis_file('path/to/your/file.lis')
lis_file.logical_files[0].curves_data[0].to_excel('path/to/your/file.xlsx')

# NOTE the function returns the path to the file.
path_to_excel = lis_file.logical_files[0].curves_data[0].to_excel('path/to/your/file.xlsx')
```
# Developing the project
To develop the project, you can clone the repository and install the requirements:

```bash
git clone https://github.com/MonumentoSoftware/wellbelog
cd wellbelog
poetry install
```
You can develop the project by creating new classes, methods, etc.
Then you can run examples inside the poetry shell, let's say the dlis_example.py:

```bash
poetry shell
python examples/dlis_example.py
```

Then you can run the tests:

```bash
poetry run pytest
```

# Academic Sponsors
Thus project was developed to support the research of [LAGESE](https://sites.ufpe.br/litpeg/lagese_equipe/) - LaboratórioLaboratório de Geologia Sedimentar e Ambiental, da Universidade Federal de Pernambuco (UFPE) , located on the [LITPEG](https://www.ufpe.br/litpeg) - Instituto de Pesquisa em Petróleo e Energia.
<div style="display: flex;flex-direction:row; justify-content: space-around; align-items: center; gap: 20px; flex-wrap: wrap;">
  <img src="./images/images.png" alt="Lagese logo" style=" max-width: 150px;height: auto;">
  <img src="./images/Logo-i-Litpeg-Horizontal-Colorida-vinho-e-chumbo-com-fundo-transparente.png" alt="Monumento logo" style="max-width: 150px; height: auto;">
</div>
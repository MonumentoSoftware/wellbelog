# BeloLas

Here we have all the code to work with the las files.
- [BeloLas](#belolas)
- [Reader](#reader)
- [Models](#models)
  - [LasFileModel](#lasfilemodel)

# Reader
The main class to search and read the las files.

```python
from webelog.belolas import LasReader

reader = LasReader()
las_files = reader.search_files('path/to/your/folder')
las_file = reader.process_las_file('path/to/your/file.las')
```

# Models
We make use of Pydantic to create the models.

## LasFileModel

The main model, that contains all the information about the sections, curves, etc.

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
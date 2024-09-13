# Schemas

We make use of Pydantic to create the models and validate the data.

# HasIdModel

Basic model with an id.

```python
class HasIdSchema(BaseModel):
    '''
    Base class for all models that have an id field.

    Attributes:
        id: str: Unique identifier for the model.
    '''
    id: Union[str, ObjectId] = Field(None, alias='_id')

    model_config = {
        'arbitrary_types_allowed': True,
    }
```

# TimeStampedModel

Model with timestamps.

```python
class TimeStampedModelSchema(HasIdSchema):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        'arbitrary_types_allowed': True,
    }
```

# GeoJsonSchema

Model for GeoJson.

```python
class GeoJSONSchema(TimeStampedModelSchema):
    """
    Base class for all models that have a geometry field.
    Specialized for GeoJSON geometries.

    Attributes:
        geometry: dict: GeoJSON geometry object.
    """
    geometry: dict = None

    def as_shape(self):
        return shape(self.geometry)
```

# DataframeModel

To represent the Dataframe.

```python
class DataframeSchema(TimeStampedModelSchema):
    """
    Base class for all models that have a dataframe field.
    Specialized for pandas dataframes.

    Attributes:
        dataframe: dict: Pandas dataframe object.
    """
    data: list = None

    def as_df(self) -> pd.DataFrame:
        """
        Convert the data to a pandas dataframe.
        """
        return pd.DataFrame(self.data)

    def to_csv(self, path: str, **kwargs,) -> str:
        """
        Save the data to a CSV file.

        Args:
            path (str): The path to save the file.
            **kwargs: Additional keyword arguments to pass to pandas.to_csv.

        Returns:
            str: the path to the file.
        """
        self.as_df().to_csv(path, index=False, **kwargs)
        return path

    def to_excel(self, path: str, **kwargs) -> str:
        """
        Save the data to an Excel file.

        Args:
            path (str): The path to save the file.
            **kwargs: Additional keyword arguments to pass to pandas.to_excel.

        Returns:
            str: the path to the file.
        """
        self.as_df().to_excel(path, index=False, **kwargs)
        return path
```
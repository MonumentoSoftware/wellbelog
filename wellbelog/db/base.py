
from datetime import datetime
from typing import Union

from bson import ObjectId
from shapely.geometry import shape
import pandas as pd
from pydantic import BaseModel, Field


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


class TimeStampedModelSchema(HasIdSchema):
    '''
    Base class for all models that have a created_at and updated_at fields.

    Attributes:
        created_at: datetime: Date and time the model was created.
        updated_at: datetime: Date and time the model was last updated.
    '''
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


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

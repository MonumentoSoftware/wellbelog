
from dataclasses import dataclass
from datetime import datetime
import json
import math
from typing import Union

from bson import ObjectId
from shapely.geometry import shape
from pydantic import BaseModel, Field


class MongoResponse(BaseModel):
    '''Base class for all responses from the MongoDB database.
    It must be open  for new fields to be added to the response.
    '''
    id: Union[str, ObjectId] = Field(None, alias='_id')

    class Config:
        arbitrary_types_allowed = True


class TimeStampedModelSchema(MongoResponse):
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class GeoJSONSchema(TimeStampedModelSchema):
    geometry: dict = None

    def as_shape(self):
        return shape(self.geometry)


@dataclass
class TimeStampedModel:
    base_last_updated: datetime = None
    base_created_at: datetime = None

    def as_dict_safe(self):
        copy = self.__dict__.copy()
        copy.pop('base_created_at')
        copy.pop('base_last_updated')
        return copy

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.base_created_at = datetime.now()
        return instance

    def as_serializable(self):
        """
        Ensures that all values in a dictionary are JSON serializable.

        Returns:
            dict: The dictionary with JSON serializable values.
        """
        processed_dict = {}

        for key, value in self.__dict__.items():
            try:
                json.dumps(value)
                processed_dict[key] = value
            except (TypeError, OverflowError):
                processed_dict[key] = str(value)

        return {key: None if (isinstance(value, float) and math.isnan(value)) else value for key, value in processed_dict.items()}  # noqa

# XXX This should be implemented using Pydantic


@dataclass
class BaseGeoJSON(TimeStampedModel):
    """
    Base class for all models that have a GeoJSON attribute.
    """
    geojson: dict = None

    def as_shape(self):
        geo_json_dict: dict = json.loads(self.geojson)
        return shape(geo_json_dict.get('geometry'))

    def as_geojson_dict(self) -> dict:
        return json.loads(self.geojson)

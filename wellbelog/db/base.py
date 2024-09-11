
from dataclasses import dataclass
from datetime import datetime
import json
import math
from typing import Union

from bson import ObjectId
from shapely.geometry import shape
from pydantic import BaseModel, Field


class HasIdSchema(BaseModel):
    '''
    Base class for all models that have an id field.
    '''
    id: Union[str, ObjectId] = Field(None, alias='_id')

    model_config = {
        'arbitrary_types_allowed': True,
    }


class TimeStampedModelSchema(HasIdSchema):
    '''Base class for all models that have a created_at and updated_at fields.'''
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class GeoJSONSchema(TimeStampedModelSchema):
    geometry: dict = None

    def as_shape(self):
        return shape(self.geometry)

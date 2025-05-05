from typing import Optional
from pydantic import BaseModel, Field as PydanticField
from typing import List
import numpy as np


class NDVI(BaseModel):
  ndvi: List[List[float]] = PydanticField(..., description="NDVI values")
  ndvi_mean: float = PydanticField(..., description="Mean NDVI value for the field")
  ndvi_std: float = PydanticField(..., description="Standard deviation of NDVI values")
  ndvi_valid_pixel_count: int = PydanticField(..., description="Number of valid pixels used for NDVI computation")

  @classmethod
  def from_array(cls, array: List[List[float]]) -> "NDVI":
    array = array.astype("float32")  # type: ignore
    valid_pixels = array[~np.isnan(array)]

    return cls(
      ndvi=array,
      ndvi_mean=float(np.mean(valid_pixels)),
      ndvi_std=float(np.std(valid_pixels)),
      ndvi_valid_pixel_count=int(valid_pixels.size),  # type: ignore
    )


class Field(BaseModel):
  id: str = PydanticField(..., description="ID of the field")
  is_new: bool = PydanticField(default=False, description="Whether the field is new")
  plant_type: str = PydanticField(..., description="Type of plant")
  plant_date: str = PydanticField(..., description="Date of planting")
  geom: dict = PydanticField(..., description="GeoJSON representation of the geometry")

  ndvi: Optional[NDVI] = PydanticField(default=None, description="NDVI values")

from typing import Any
import uuid
import json
from shapely.geometry import mapping
import geopandas as gpd
from uuid import UUID
from pydantic import BaseModel, Field


class Bbox(BaseModel):
  id: UUID = Field(..., description="UUIDv5 derived from the geometry")
  bbox: Any = Field(..., description="GeoDataFrame containing the bbox")
  geom: dict = Field(..., description="GeoJSON representation of the geometry")

  @staticmethod
  def get_id_from_geom(geometry) -> UUID:
    geojson = json.dumps(mapping(geometry), sort_keys=True)
    return uuid.uuid5(uuid.NAMESPACE_URL, geojson)

  @classmethod
  def from_geodataframe(cls, gdf: gpd.GeoDataFrame) -> "Bbox":
    geometry = gdf.geometry.iloc[0]
    geom_json = mapping(geometry)
    bbox_id = cls.get_id_from_geom(geometry)
    return cls(id=bbox_id, bbox=gdf, geom=geom_json)

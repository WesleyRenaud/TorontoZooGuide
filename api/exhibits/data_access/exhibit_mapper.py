from __future__ import annotations

from .region_exhibit_record import RegionExhibitRecord
from ...types import Row


class ExhibitMapper():
   @classmethod
   def map_region_exhibit_row( cls, row: Row ) -> RegionExhibitRecord:
      return RegionExhibitRecord(
         region_name=row[ 'REGION_NAME' ],
         exhibit_name=row[ 'EXHIBIT_NAME' ] )


   @classmethod
   def map_region_exhibit_rows( cls, rows: list[ Row ] ) -> list[ RegionExhibitRecord ]:
      return [
         cls.map_region_exhibit_row( row )
         for row in rows
      ]

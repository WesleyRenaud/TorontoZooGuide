from __future__ import annotations

from collections.abc import Iterable

from .region_exhibit_record import RegionExhibitRecord
from ...types import Row


def map_region_exhibit_row( row: Row ) -> RegionExhibitRecord:
   return RegionExhibitRecord(
      region_name=row[ 'REGION_NAME' ],
      exhibit_name=row[ 'EXHIBIT_NAME' ] )


def map_region_exhibit_rows( rows: Iterable[ Row ] ) -> list[ RegionExhibitRecord ]:
   return [
      map_region_exhibit_row( row )
      for row in rows
   ]

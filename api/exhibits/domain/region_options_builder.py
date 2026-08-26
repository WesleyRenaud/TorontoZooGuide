from __future__ import annotations

from ..data_access.region_exhibit_record import RegionExhibitRecord
from ...models import Region


class RegionOptionsBuilder():
   @classmethod
   def build( cls, region_exhibit_rows: list[ RegionExhibitRecord ] ) -> list[ Region ]:
      exhibits_by_region: dict[ str, list[ str ] ] = {}

      for region_exhibit in region_exhibit_rows:
         region_name = region_exhibit.region_name
         exhibit_name = region_exhibit.exhibit_name

         if region_name not in exhibits_by_region:
            exhibits_by_region[ region_name ] = []

         if exhibit_name != None:
            exhibits_by_region[ region_name ].append( exhibit_name )

      return [
         Region(
            name=region_name,
            has_exhibits=not (
               len( exhibits ) == 1
               and exhibits[ 0 ] == region_name
            ) )
         for region_name, exhibits in exhibits_by_region.items()
         if len( exhibits ) > 0
      ]

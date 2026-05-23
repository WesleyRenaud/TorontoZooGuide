from __future__ import annotations

from ...models import RegionWithExhibits
from ..data_access.region_exhibit_record import RegionExhibitRecord


def build_regions_with_exhibits(
      region_exhibit_records: list[ RegionExhibitRecord ] ) -> list[ RegionWithExhibits ]:
   regions: list[ RegionWithExhibits ] = []
   current_region: RegionWithExhibits | None = None

   for record in region_exhibit_records:
      region_name = record.region_name
      exhibit_name = record.exhibit_name

      if current_region == None or current_region.name != region_name:
         current_region = RegionWithExhibits(
            name=region_name,
            exhibits=[] )
         regions.append( current_region )

      if exhibit_name == None:
         continue

      current_region.exhibits.append( exhibit_name )

   return [
      region for region in regions
      if len( region.exhibits ) > 0
   ]

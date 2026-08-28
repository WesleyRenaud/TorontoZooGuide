from __future__ import annotations

from api.exhibits.data_access.region_exhibit_record import RegionExhibitRecord
from api.exhibits.domain.regions_with_exhibits_builder import RegionsWithExhibitsBuilder


REGION_NAME = 'Africa'
OTHER_REGION_NAME = 'Eurasia'
EXHIBIT_NAME = 'Africa Savanna'
OTHER_EXHIBIT_NAME = 'Eurasia Wilds'


def Test_Build_TestMultipleRegions_ExpectExhibitsGroupedByRegion() -> None:
   rows = [
      RegionExhibitRecord( region_name=REGION_NAME, exhibit_name=EXHIBIT_NAME ),
      RegionExhibitRecord( region_name=OTHER_REGION_NAME, exhibit_name=OTHER_EXHIBIT_NAME ),
   ]

   regions = RegionsWithExhibitsBuilder.build( rows )

   assert [ ( region.name, region.exhibits ) for region in regions ] == [
      ( REGION_NAME, [ EXHIBIT_NAME ] ),
      ( OTHER_REGION_NAME, [ OTHER_EXHIBIT_NAME ] ),
   ]


def Test_Build_TestNullExhibitName_ExpectSkippedAndRegionExcludedWhenOnlyNull() -> None:
   rows = [
      RegionExhibitRecord( region_name=REGION_NAME, exhibit_name=None ),
   ]

   assert RegionsWithExhibitsBuilder.build( rows ) == []


def Test_Build_TestNullExhibitName_ExpectNamedExhibitsRetained() -> None:
   rows = [
      RegionExhibitRecord( region_name=REGION_NAME, exhibit_name=None ),
      RegionExhibitRecord( region_name=REGION_NAME, exhibit_name=EXHIBIT_NAME ),
      RegionExhibitRecord( region_name=REGION_NAME, exhibit_name=OTHER_EXHIBIT_NAME ),
   ]

   regions = RegionsWithExhibitsBuilder.build( rows )

   assert [ ( region.name, region.exhibits ) for region in regions ] == [
      ( REGION_NAME, [ EXHIBIT_NAME, OTHER_EXHIBIT_NAME ] ),
   ]

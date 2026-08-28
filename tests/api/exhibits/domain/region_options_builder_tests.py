from __future__ import annotations

from api.exhibits.data_access.region_exhibit_record import RegionExhibitRecord
from api.exhibits.domain.region_options_builder import RegionOptionsBuilder


REGION_NAME = 'Africa'
EXHIBIT_NAME = 'Africa Savanna'
PAVILION_ONLY_REGION = 'Americas Pavilion'
OTHER_EXHIBIT_NAME = 'Eurasia Wilds'


def Test_Build_TestMultipleExhibitsInRegion_ExpectHasExhibitsTrue() -> None:
   rows = [
      RegionExhibitRecord( region_name=REGION_NAME, exhibit_name=EXHIBIT_NAME ),
      RegionExhibitRecord( region_name=REGION_NAME, exhibit_name=OTHER_EXHIBIT_NAME ),
   ]

   regions = RegionOptionsBuilder.build( rows )

   assert [ ( region.name, region.has_exhibits ) for region in regions ] == [
      ( REGION_NAME, True ),
   ]


def Test_Build_TestSingleExhibitNamedAfterRegion_ExpectHasExhibitsFalse() -> None:
   rows = [
      RegionExhibitRecord(
         region_name=PAVILION_ONLY_REGION,
         exhibit_name=PAVILION_ONLY_REGION ),
   ]

   regions = RegionOptionsBuilder.build( rows )

   assert [ ( region.name, region.has_exhibits ) for region in regions ] == [
      ( PAVILION_ONLY_REGION, False ),
   ]


def Test_Build_TestNullExhibitName_ExpectRegionExcludedWhenOnlyNullExhibits() -> None:
   rows = [
      RegionExhibitRecord( region_name=REGION_NAME, exhibit_name=None ),
   ]

   assert RegionOptionsBuilder.build( rows ) == []


def Test_Build_TestNullExhibitName_ExpectListedWhenRegionHasNamedExhibits() -> None:
   rows = [
      RegionExhibitRecord( region_name=REGION_NAME, exhibit_name=None ),
      RegionExhibitRecord( region_name=REGION_NAME, exhibit_name=EXHIBIT_NAME ),
   ]

   regions = RegionOptionsBuilder.build( rows )

   assert [ ( region.name, region.has_exhibits ) for region in regions ] == [
      ( REGION_NAME, True ),
   ]

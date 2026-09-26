from __future__ import annotations

from api.itinerary.data_access.itinerary_name_key_builder import ItineraryNameKeyBuilder


def Test_Build_TestMixedCaseAndWhitespace_ExpectNormalizedKey() -> None:
   species = 'African Lion'
   value = f'  { species }  '

   key = ItineraryNameKeyBuilder.build( value )

   assert key == species.lower()

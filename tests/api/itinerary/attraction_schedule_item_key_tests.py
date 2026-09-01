from __future__ import annotations

from api.itinerary.attraction_schedule_item_key import AttractionScheduleItemKey


CAROUSEL = 'Conservation Carousel'


def Test_FromWire_TestName_ExpectAttractionKey() -> None:
   key = AttractionScheduleItemKey.from_wire( CAROUSEL )

   assert key == AttractionScheduleItemKey( name=CAROUSEL )


def Test_FromWire_TestBlankName_ExpectNone() -> None:
   assert AttractionScheduleItemKey.from_wire( '' ) is None
   assert AttractionScheduleItemKey.from_wire( '   ' ) is None


def Test_ToWire_TestName_ExpectTrimmedWire() -> None:
   key = AttractionScheduleItemKey( name=f'  { CAROUSEL }  ' )

   assert key.to_wire() == CAROUSEL

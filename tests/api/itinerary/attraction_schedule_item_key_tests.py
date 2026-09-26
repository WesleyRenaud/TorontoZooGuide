from __future__ import annotations

from api.itinerary.attraction_schedule_item_key import AttractionScheduleItemKey


CAROUSEL = 'Conservation Carousel'


def Test_FromWire_TestName_ExpectAttractionKey() -> None:
   wire = CAROUSEL

   key = AttractionScheduleItemKey.from_wire( wire )

   assert key == AttractionScheduleItemKey( name=wire )


def Test_FromWire_TestEmptyName_ExpectNone() -> None:
   wire = ''

   key = AttractionScheduleItemKey.from_wire( wire )

   assert key is None


def Test_FromWire_TestBlankName_ExpectNone() -> None:
   wire = '   '

   key = AttractionScheduleItemKey.from_wire( wire )

   assert key is None


def Test_ToWire_TestName_ExpectTrimmedWire() -> None:
   name = CAROUSEL
   key = AttractionScheduleItemKey( name=f'  { name }  ' )

   wire = key.to_wire()

   assert wire == name

from __future__ import annotations

from api.itinerary.transportation_schedule_item_key import TransportationScheduleItemKey


ZOOMOBILE = 'Zoomobile'


def Test_FromWire_TestTransitMode_ExpectAddedAsAttractionFalse() -> None:
   key = TransportationScheduleItemKey.from_wire( f'{ ZOOMOBILE }||0' )

   assert key == TransportationScheduleItemKey(
      name=ZOOMOBILE,
      added_as_attraction=False )


def Test_FromWire_TestAttractionMode_ExpectAddedAsAttractionTrue() -> None:
   key = TransportationScheduleItemKey.from_wire( f'{ ZOOMOBILE }||1' )

   assert key == TransportationScheduleItemKey(
      name=ZOOMOBILE,
      added_as_attraction=True )


def Test_FromWire_TestInvalidWire_ExpectNone() -> None:
   assert TransportationScheduleItemKey.from_wire( ZOOMOBILE ) is None
   assert TransportationScheduleItemKey.from_wire( f'{ ZOOMOBILE }||2' ) is None
   assert TransportationScheduleItemKey.from_wire( '||0' ) is None


def Test_ToWire_TestModes_ExpectFlagSuffix() -> None:
   assert TransportationScheduleItemKey(
      name=ZOOMOBILE,
      added_as_attraction=False ).to_wire() == f'{ ZOOMOBILE }||0'
   assert TransportationScheduleItemKey(
      name=ZOOMOBILE,
      added_as_attraction=True ).to_wire() == f'{ ZOOMOBILE }||1'

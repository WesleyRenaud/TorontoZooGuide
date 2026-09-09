from __future__ import annotations

from api.itinerary.transportation_schedule_item_key import TransportationScheduleItemKey
from api.shared.enums.transportation_name import TransportationName


def Test_FromWire_TestTransitMode_ExpectAddedAsAttractionFalse() -> None:
   key = TransportationScheduleItemKey.from_wire(
      f'{ TransportationName.ZOOMOBILE.value }||0' )

   assert key == TransportationScheduleItemKey(
      name=TransportationName.ZOOMOBILE.value,
      added_as_attraction=False )


def Test_FromWire_TestAttractionMode_ExpectAddedAsAttractionTrue() -> None:
   key = TransportationScheduleItemKey.from_wire(
      f'{ TransportationName.ZOOMOBILE.value }||1' )

   assert key == TransportationScheduleItemKey(
      name=TransportationName.ZOOMOBILE.value,
      added_as_attraction=True )


def Test_FromWire_TestInvalidWire_ExpectNone() -> None:
   assert TransportationScheduleItemKey.from_wire(
      TransportationName.ZOOMOBILE.value ) is None
   assert TransportationScheduleItemKey.from_wire(
      f'{ TransportationName.ZOOMOBILE.value }||2' ) is None
   assert TransportationScheduleItemKey.from_wire( '||0' ) is None


def Test_ToWire_TestModes_ExpectFlagSuffix() -> None:
   assert TransportationScheduleItemKey(
      name=TransportationName.ZOOMOBILE.value,
      added_as_attraction=False ).to_wire() == (
      f'{ TransportationName.ZOOMOBILE.value }||0' )
   assert TransportationScheduleItemKey(
      name=TransportationName.ZOOMOBILE.value,
      added_as_attraction=True ).to_wire() == (
      f'{ TransportationName.ZOOMOBILE.value }||1' )

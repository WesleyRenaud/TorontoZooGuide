from __future__ import annotations

from api.itinerary.schedule_item_key_separator import ScheduleItemKeySeparator
from api.itinerary.transportation_schedule_item_key import TransportationScheduleItemKey
from api.shared.enums.transportation_name import TransportationName


def Test_FromWire_TestTransitMode_ExpectAddedAsAttractionFalse() -> None:
   name = TransportationName.ZOOMOBILE.value
   added_as_attraction = False
   wire = (
      f'{ name }'
      f'{ ScheduleItemKeySeparator.VALUE }'
      f'{ "1" if added_as_attraction else "0" }' )

   key = TransportationScheduleItemKey.from_wire( wire )

   assert key == TransportationScheduleItemKey(
      name=name,
      added_as_attraction=added_as_attraction )


def Test_FromWire_TestAttractionMode_ExpectAddedAsAttractionTrue() -> None:
   name = TransportationName.ZOOMOBILE.value
   added_as_attraction = True
   wire = (
      f'{ name }'
      f'{ ScheduleItemKeySeparator.VALUE }'
      f'{ "1" if added_as_attraction else "0" }' )

   key = TransportationScheduleItemKey.from_wire( wire )

   assert key == TransportationScheduleItemKey(
      name=name,
      added_as_attraction=added_as_attraction )


def Test_FromWire_TestMissingFlag_ExpectNone() -> None:
   wire = TransportationName.ZOOMOBILE.value

   key = TransportationScheduleItemKey.from_wire( wire )

   assert key is None


def Test_FromWire_TestInvalidFlag_ExpectNone() -> None:
   name = TransportationName.ZOOMOBILE.value
   wire = f'{ name }{ ScheduleItemKeySeparator.VALUE }2'

   key = TransportationScheduleItemKey.from_wire( wire )

   assert key is None


def Test_FromWire_TestEmptyName_ExpectNone() -> None:
   wire = f'{ ScheduleItemKeySeparator.VALUE }0'

   key = TransportationScheduleItemKey.from_wire( wire )

   assert key is None


def Test_ToWire_TestTransitMode_ExpectFalseFlag() -> None:
   name = TransportationName.ZOOMOBILE.value
   key = TransportationScheduleItemKey(
      name=name,
      added_as_attraction=False )

   wire = key.to_wire()

   assert wire == (
      f'{ key.name }'
      f'{ ScheduleItemKeySeparator.VALUE }'
      f'{ "1" if key.added_as_attraction else "0" }' )


def Test_ToWire_TestAttractionMode_ExpectTrueFlag() -> None:
   name = TransportationName.ZOOMOBILE.value
   key = TransportationScheduleItemKey(
      name=name,
      added_as_attraction=True )

   wire = key.to_wire()

   assert wire == (
      f'{ key.name }'
      f'{ ScheduleItemKeySeparator.VALUE }'
      f'{ "1" if key.added_as_attraction else "0" }' )

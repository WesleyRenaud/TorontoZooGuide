from __future__ import annotations

from api.itinerary.animal_schedule_item_key import AnimalScheduleItemKey
from api.itinerary.attraction_schedule_item_key import AttractionScheduleItemKey
from api.itinerary.scheduling.items.schedule_item_key_mapper import ScheduleItemKeyMapper
from api.itinerary.transportation_schedule_item_key import TransportationScheduleItemKey
from api.shared.enums import ItineraryEventType


LION_KEY = 'African Lion||Africa Savanna'
PENGUIN_KEY = 'African Penguin||Africa Savanna||Outdoor'


def Test_FromWire_TestAnimalKey_ExpectAnimalScheduleItemKey() -> None:
   schedule_item_key = ScheduleItemKeyMapper.from_wire( 'animals', LION_KEY )

   assert schedule_item_key == AnimalScheduleItemKey(
      species='African Lion',
      exhibit='Africa Savanna' )


def Test_FromWire_TestAnimalKeyWithEnclosure_ExpectAnimalScheduleItemKey() -> None:
   schedule_item_key = ScheduleItemKeyMapper.from_wire( 'animals', PENGUIN_KEY )

   assert schedule_item_key == AnimalScheduleItemKey(
      species='African Penguin',
      exhibit='Africa Savanna',
      enclosure_name='Outdoor' )


def Test_FromWire_TestEventTypeAsItemType_ExpectLunchEvent() -> None:
   schedule_item_key = ScheduleItemKeyMapper.from_wire( 'lunch', '' )

   assert schedule_item_key == ItineraryEventType.LUNCH


def Test_FromWire_TestAttractionKey_ExpectAttractionScheduleItemKey() -> None:
   schedule_item_key = ScheduleItemKeyMapper.from_wire(
      'attractions',
      'Conservation Carousel' )

   assert schedule_item_key == AttractionScheduleItemKey(
      name='Conservation Carousel' )


def Test_FromWire_TestTransportationKeys_ExpectTransitOrAttractionMode() -> None:
   schedule_item_key = ScheduleItemKeyMapper.from_wire(
      'transportations',
      'Zoomobile||0' )

   assert schedule_item_key == TransportationScheduleItemKey(
      name='Zoomobile',
      added_as_attraction=False )
   assert ScheduleItemKeyMapper.from_wire(
      'transportations',
      'Zoomobile' ) is None
   assert ScheduleItemKeyMapper.from_wire(
      'transportations',
      'Zoomobile||1' ) == TransportationScheduleItemKey(
         name='Zoomobile',
         added_as_attraction=True )

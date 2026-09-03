from __future__ import annotations

from api.itinerary.animal_schedule_item_key import AnimalScheduleItemKey
from api.itinerary.attraction_schedule_item_key import AttractionScheduleItemKey
from api.itinerary.guardians_talk_schedule_item_key import GuardiansTalkScheduleItemKey
from api.itinerary.scheduling.items.schedule_item_key_mapper import ScheduleItemKeyMapper
from api.itinerary.transportation_schedule_item_key import TransportationScheduleItemKey
from api.itinerary.wild_encounter_schedule_item_key import WildEncounterScheduleItemKey
from api.shared.enums import ItineraryEventType
from api.shared.enums import ScheduleItemKind


LION_KEY = 'African Lion||Africa Savanna'
PENGUIN_KEY = 'African Penguin||Africa Savanna||Outdoor'


def Test_FromWire_TestEmptyItemType_ExpectNone() -> None:
   assert ScheduleItemKeyMapper.from_wire( '   ', LION_KEY ) is None


def Test_FromWire_TestUnknownItemType_ExpectNone() -> None:
   assert ScheduleItemKeyMapper.from_wire( 'unknown', LION_KEY ) is None


def Test_FromWire_TestEventItemType_ExpectEventFromWireKey() -> None:
   schedule_item_key = ScheduleItemKeyMapper.from_wire( 'event', 'lunch' )

   assert schedule_item_key == ItineraryEventType.LUNCH


def Test_FromWire_TestEntranceItemType_ExpectNone() -> None:
   assert ScheduleItemKeyMapper.from_wire( 'entrance', 'entrance' ) is None


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


def Test_FromWire_TestGuardiansTalkKey_ExpectGuardiansTalkScheduleItemKey() -> None:
   schedule_item_key = ScheduleItemKeyMapper.from_wire(
      ScheduleItemKind.GUARDIANS_TALK.item_type,
      'Gorilla Guardians||10:00' )

   assert schedule_item_key == GuardiansTalkScheduleItemKey(
      name='Gorilla Guardians',
      start_time='10:00' )


def Test_FromWire_TestWildEncounterKey_ExpectWildEncounterScheduleItemKey() -> None:
   schedule_item_key = ScheduleItemKeyMapper.from_wire(
      ScheduleItemKind.WILD_ENCOUNTER.item_type,
      'African Rainforest||14:00' )

   assert schedule_item_key == WildEncounterScheduleItemKey(
      name='African Rainforest',
      start_time='2:00 PM' )

from __future__ import annotations

from api.itinerary.animal_schedule_item_key import AnimalScheduleItemKey
from api.itinerary.attraction_schedule_item_key import AttractionScheduleItemKey
from api.itinerary.guardians_talk_schedule_item_key import GuardiansTalkScheduleItemKey
from api.itinerary.scheduling.items.schedule_item_key_mapper import ScheduleItemKeyMapper
from api.itinerary.transportation_schedule_item_key import TransportationScheduleItemKey
from api.itinerary.wild_encounter_schedule_item_key import WildEncounterScheduleItemKey
from api.shared.enums import ItineraryEventType
from api.shared.enums import ScheduleItemKind
from api.shared.enums.transportation_name import TransportationName


LION_KEY = 'African Lion||Africa Savanna'
PENGUIN_KEY = 'African Penguin||Africa Savanna||Outdoor'
ZOOMOBILE_TRANSIT_WIRE = TransportationScheduleItemKey(
   name=TransportationName.ZOOMOBILE,
   added_as_attraction=False ).to_wire()
ZOOMOBILE_ATTRACTION_WIRE = TransportationScheduleItemKey(
   name=TransportationName.ZOOMOBILE,
   added_as_attraction=True ).to_wire()


def Test_FromWire_TestEmptyItemType_ExpectNone() -> None:
   schedule_item_key = ScheduleItemKeyMapper.from_wire( '   ', LION_KEY )

   assert schedule_item_key is None


def Test_FromWire_TestUnknownItemType_ExpectNone() -> None:
   schedule_item_key = ScheduleItemKeyMapper.from_wire( 'unknown', LION_KEY )

   assert schedule_item_key is None


def Test_FromWire_TestEventItemType_ExpectEventFromWireKey() -> None:
   event_key = 'lunch'

   schedule_item_key = ScheduleItemKeyMapper.from_wire( 'event', event_key )

   assert schedule_item_key == ItineraryEventType.normalize( event_key )


def Test_FromWire_TestEntranceItemType_ExpectNone() -> None:
   schedule_item_key = ScheduleItemKeyMapper.from_wire( 'entrance', 'entrance' )

   assert schedule_item_key is None


def Test_FromWire_TestAnimalKey_ExpectAnimalScheduleItemKey() -> None:
   schedule_item_key = ScheduleItemKeyMapper.from_wire( 'animals', LION_KEY )

   assert schedule_item_key == AnimalScheduleItemKey.from_wire( LION_KEY )


def Test_FromWire_TestAnimalKeyWithEnclosure_ExpectAnimalScheduleItemKey() -> None:
   schedule_item_key = ScheduleItemKeyMapper.from_wire( 'animals', PENGUIN_KEY )

   assert schedule_item_key == AnimalScheduleItemKey.from_wire( PENGUIN_KEY )


def Test_FromWire_TestEventTypeAsItemType_ExpectLunchEvent() -> None:
   event_type = 'lunch'

   schedule_item_key = ScheduleItemKeyMapper.from_wire( event_type, '' )

   assert schedule_item_key == ItineraryEventType.normalize( event_type )


def Test_FromWire_TestAttractionKey_ExpectAttractionScheduleItemKey() -> None:
   attraction_name = 'Conservation Carousel'

   schedule_item_key = ScheduleItemKeyMapper.from_wire(
      'attractions',
      attraction_name )

   assert schedule_item_key == AttractionScheduleItemKey.from_wire( attraction_name )


def Test_FromWire_TestTransportationTransitKey_ExpectTransitMode() -> None:
   schedule_item_key = ScheduleItemKeyMapper.from_wire(
      'transportations',
      ZOOMOBILE_TRANSIT_WIRE )

   assert schedule_item_key == TransportationScheduleItemKey.from_wire(
      ZOOMOBILE_TRANSIT_WIRE )


def Test_FromWire_TestTransportationBareName_ExpectNone() -> None:
   schedule_item_key = ScheduleItemKeyMapper.from_wire(
      'transportations',
      TransportationName.ZOOMOBILE )

   assert schedule_item_key is None


def Test_FromWire_TestTransportationAttractionKey_ExpectAttractionMode() -> None:
   schedule_item_key = ScheduleItemKeyMapper.from_wire(
      'transportations',
      ZOOMOBILE_ATTRACTION_WIRE )

   assert schedule_item_key == TransportationScheduleItemKey.from_wire(
      ZOOMOBILE_ATTRACTION_WIRE )


def Test_FromWire_TestGuardiansTalkKey_ExpectGuardiansTalkScheduleItemKey() -> None:
   talk_wire = 'Gorilla Guardians||10:00'

   schedule_item_key = ScheduleItemKeyMapper.from_wire(
      ScheduleItemKind.GUARDIANS_TALK.item_type,
      talk_wire )

   assert schedule_item_key == GuardiansTalkScheduleItemKey.from_wire( talk_wire )


def Test_FromWire_TestWildEncounterKey_ExpectWildEncounterScheduleItemKey() -> None:
   encounter_wire = 'African Rainforest||14:00'

   schedule_item_key = ScheduleItemKeyMapper.from_wire(
      ScheduleItemKind.WILD_ENCOUNTER.item_type,
      encounter_wire )

   assert schedule_item_key == WildEncounterScheduleItemKey.from_wire( encounter_wire )

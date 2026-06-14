from __future__ import annotations

from dataclasses import dataclass

from ....shared.enums import ItineraryEventType
from ....shared.enums import ScheduleItemKind

SCHEDULE_ITEM_ANIMAL_KEY_SEPARATOR = '||'


@dataclass( frozen=True )
class ParsedScheduleItemRequest:
   kind: ScheduleItemKind
   species: str | None = None
   exhibit: str | None = None
   attraction_name: str | None = None
   event_type: ItineraryEventType | None = None
   talk_name: str | None = None
   wild_encounter_name: str | None = None


def _parse_animal_key( key: str ) -> tuple[ str, str ] | None:
   parts = key.split( SCHEDULE_ITEM_ANIMAL_KEY_SEPARATOR, 1 )

   if len( parts ) != 2:
      return None

   species = parts[ 0 ].strip()
   exhibit = parts[ 1 ].strip()

   if not species or not exhibit:
      return None

   return species, exhibit


def parse_schedule_item_request(
      item_type: str,
      key: str ) -> ParsedScheduleItemRequest | None:
   normalized_type = item_type.strip().lower()
   normalized_key = key.strip()

   if not normalized_type:
      return None

   event_type_from_type = ItineraryEventType.normalize( normalized_type )

   if event_type_from_type is not None:
      return ParsedScheduleItemRequest(
         kind=ScheduleItemKind.EVENT,
         event_type=event_type_from_type )

   item_kind = ScheduleItemKind.from_item_type( normalized_type )

   if item_kind is None:
      return None

   if item_kind == ScheduleItemKind.EVENT:
      event_type = ItineraryEventType.normalize( normalized_key )

      if event_type is None:
         return None

      return ParsedScheduleItemRequest(
         kind=ScheduleItemKind.EVENT,
         event_type=event_type )

   if item_kind == ScheduleItemKind.ANIMAL:
      animal_key = _parse_animal_key( normalized_key )

      if animal_key is None:
         return None

      species, exhibit = animal_key

      return ParsedScheduleItemRequest(
         kind=ScheduleItemKind.ANIMAL,
         species=species,
         exhibit=exhibit )

   if item_kind == ScheduleItemKind.ATTRACTION:
      if not normalized_key:
         return None

      return ParsedScheduleItemRequest(
         kind=ScheduleItemKind.ATTRACTION,
         attraction_name=normalized_key )

   if item_kind == ScheduleItemKind.GUARDIANS_TALK:
      if not normalized_key:
         return None

      return ParsedScheduleItemRequest(
         kind=ScheduleItemKind.GUARDIANS_TALK,
         talk_name=normalized_key )

   if item_kind == ScheduleItemKind.WILD_ENCOUNTER:
      if not normalized_key:
         return None

      return ParsedScheduleItemRequest(
         kind=ScheduleItemKind.WILD_ENCOUNTER,
         wild_encounter_name=normalized_key )

   return None

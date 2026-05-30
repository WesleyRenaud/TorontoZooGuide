from __future__ import annotations

from dataclasses import dataclass

from ...shared.enums import ItineraryEventType

SCHEDULE_ITEM_ANIMAL_KEY_SEPARATOR = '||'

_ITEM_TYPE_ALIASES = {
   'animals': 'animal',
   'attractions': 'attraction',
}


@dataclass( frozen=True )
class ParsedScheduleItemRequest:
   kind: str
   species: str | None = None
   exhibit: str | None = None
   attraction_name: str | None = None
   event_type: ItineraryEventType | None = None


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
         kind='event',
         event_type=event_type_from_type )

   normalized_type = _ITEM_TYPE_ALIASES.get( normalized_type, normalized_type )

   if normalized_type == 'event':
      event_type = ItineraryEventType.normalize( normalized_key )

      if event_type is None:
         return None

      return ParsedScheduleItemRequest(
         kind='event',
         event_type=event_type )

   if normalized_type == 'animal':
      animal_key = _parse_animal_key( normalized_key )

      if animal_key is None:
         return None

      species, exhibit = animal_key

      return ParsedScheduleItemRequest(
         kind='animal',
         species=species,
         exhibit=exhibit )

   if normalized_type == 'attraction':
      if not normalized_key:
         return None

      return ParsedScheduleItemRequest(
         kind='attraction',
         attraction_name=normalized_key )

   return None

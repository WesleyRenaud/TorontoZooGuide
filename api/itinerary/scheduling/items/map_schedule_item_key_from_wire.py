from __future__ import annotations

from ...animal_item_key import AnimalScheduleItemKey
from ...attraction_item_key import AttractionScheduleItemKey
from ...guardians_talk_item_key import GuardiansTalkScheduleItemKey
from .schedule_item_key import ScheduleItemKey
from ....shared.enums import ItineraryEventType
from ....shared.enums import ScheduleItemKind
from ...wild_encounter_item_key import WildEncounterScheduleItemKey


def map_schedule_item_key_from_wire(
      item_type: str,
      wire_key: str ) -> ScheduleItemKey | None:
   normalized_type = item_type.strip().lower()
   normalized_key = wire_key.strip()

   if not normalized_type:
      return None

   event_type_from_type = ItineraryEventType.normalize( normalized_type )

   if event_type_from_type is not None:
      return event_type_from_type

   item_kind = ScheduleItemKind.from_item_type( normalized_type )

   if item_kind is None:
      return None

   if item_kind == ScheduleItemKind.EVENT:
      return ItineraryEventType.normalize( normalized_key )

   if item_kind == ScheduleItemKind.ANIMAL:
      return AnimalScheduleItemKey.from_wire( normalized_key )

   if item_kind == ScheduleItemKind.ATTRACTION:
      return AttractionScheduleItemKey.from_wire( normalized_key )

   if item_kind == ScheduleItemKind.GUARDIANS_TALK:
      return GuardiansTalkScheduleItemKey.from_wire( normalized_key )

   if item_kind == ScheduleItemKind.WILD_ENCOUNTER:
      return WildEncounterScheduleItemKey.from_wire( normalized_key )

   return None

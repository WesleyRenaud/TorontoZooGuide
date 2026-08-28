from __future__ import annotations

from typing import TypeAlias

from ...animal_schedule_item_key import AnimalScheduleItemKey
from ...attraction_schedule_item_key import AttractionScheduleItemKey
from ...guardians_talk_schedule_item_key import GuardiansTalkScheduleItemKey
from ....shared.enums import ItineraryEventType
from ...transportation_schedule_item_key import TransportationScheduleItemKey
from ...wild_encounter_schedule_item_key import WildEncounterScheduleItemKey


class ScheduleItemKey():
   Key: TypeAlias = (
      AnimalScheduleItemKey
      | AttractionScheduleItemKey
      | TransportationScheduleItemKey
      | GuardiansTalkScheduleItemKey
      | WildEncounterScheduleItemKey
      | ItineraryEventType
   )

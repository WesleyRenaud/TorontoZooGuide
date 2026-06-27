from __future__ import annotations

from ...animal_item_key import AnimalScheduleItemKey
from ...attraction_item_key import AttractionScheduleItemKey
from ...guardians_talk_item_key import GuardiansTalkScheduleItemKey
from ....shared.enums import ItineraryEventType
from ...wild_encounter_item_key import WildEncounterScheduleItemKey

ScheduleItemKey = (
   AnimalScheduleItemKey
   | AttractionScheduleItemKey
   | GuardiansTalkScheduleItemKey
   | WildEncounterScheduleItemKey
   | ItineraryEventType
)

ListedScheduleItemKey = AnimalScheduleItemKey | AttractionScheduleItemKey

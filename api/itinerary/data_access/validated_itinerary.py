from dataclasses import dataclass

from ...models import ItineraryEvent
from ...models.animal_diff import AnimalDiff
from ...models.attraction_diff import AttractionDiff
from ...models.guardians_talk_diff import GuardiansTalkDiff
from ...models.wild_encounter_diff import WildEncounterDiff
from ...types import ScheduleTimeKey


@dataclass( frozen=True )
class ValidatedItinerary:
   arrival_time: ScheduleTimeKey
   departure_time: ScheduleTimeKey
   animals: list[ AnimalDiff ]
   attractions: list[ AttractionDiff ]
   guardians_talks: list[ GuardiansTalkDiff ]
   wild_encounters: list[ WildEncounterDiff ]
   events: list[ ItineraryEvent ]

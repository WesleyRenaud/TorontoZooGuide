from dataclasses import dataclass

from ...models.animal_diff import AnimalDiff
from ...models.attraction_diff import AttractionDiff
from ...models.guardians_talk_diff import GuardiansTalkDiff
from ...models.wild_encounter_diff import WildEncounterDiff


@dataclass( frozen=True )
class ValidatedItinerary:
   animals: list[ AnimalDiff ]
   attractions: list[ AttractionDiff ]
   guardians_talks: list[ GuardiansTalkDiff ]
   wild_encounters: list[ WildEncounterDiff ]

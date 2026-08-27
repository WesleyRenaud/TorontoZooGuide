from __future__ import annotations

from dataclasses import dataclass

from ...models.guardians_talk_diff import GuardiansTalkDiff
from ...models.wild_encounter_diff import WildEncounterDiff


@dataclass( frozen=True )
class ItineraryUnscheduleRequirements:
   talks: list[ GuardiansTalkDiff ]
   encounters: list[ WildEncounterDiff ]

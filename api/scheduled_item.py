from __future__ import annotations

from typing import TypeAlias

from .models.guardians_talk_diff import GuardiansTalkDiff
from .models.wild_encounter_diff import WildEncounterDiff


class ScheduledItem():
   Item: TypeAlias = GuardiansTalkDiff | WildEncounterDiff

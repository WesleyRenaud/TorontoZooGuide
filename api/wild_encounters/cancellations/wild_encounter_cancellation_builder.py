from __future__ import annotations

from ...types import DateKey
from .wild_encounter_cancellation_input import WildEncounterCancellationInput


class WildEncounterCancellationBuilder():
   @classmethod
   def build(
         cls,
         wild_encounter: str,
         date: DateKey,
         time: str ) -> WildEncounterCancellationInput:
      return WildEncounterCancellationInput(
         wild_encounter=wild_encounter,
         cancellation_date=date,
         encounter_time=time )

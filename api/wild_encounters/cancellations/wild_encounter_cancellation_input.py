from dataclasses import dataclass


@dataclass( frozen=True )
class WildEncounterCancellationInput:
   wild_encounter: str
   cancellation_date: str
   encounter_time: str

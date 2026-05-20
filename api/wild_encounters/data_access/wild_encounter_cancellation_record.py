from dataclasses import dataclass


@dataclass( frozen=True )
class WildEncounterCancellationRecord:
   cancellation_date: str
   encounter_time: str

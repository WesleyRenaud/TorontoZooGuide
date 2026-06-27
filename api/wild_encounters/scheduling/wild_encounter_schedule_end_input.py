from dataclasses import dataclass


@dataclass( frozen=True )
class WildEncounterScheduleEndInput:
   wild_encounter: str
   schedule_end_date: str
   encounter_time: str

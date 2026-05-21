from dataclasses import dataclass


@dataclass( frozen=True )
class WildEncounterScheduleInput:
   wild_encounter: str
   start_date: str
   end_date: object
   encounter_time: str
   monday: bool
   tuesday: bool
   wednesday: bool
   thursday: bool
   friday: bool
   saturday: bool
   sunday: bool
   message: str

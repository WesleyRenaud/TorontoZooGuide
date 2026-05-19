from dataclasses import dataclass


@dataclass( frozen=True )
class WildEncounterScheduleRecord:
   name: object
   meeting_spot: object
   link: object
   maximum_duration: object
   x_coord: object
   y_coord: object
   schedule_start_date: object
   schedule_end_date: object
   monday: object
   tuesday: object
   wednesday: object
   thursday: object
   friday: object
   saturday: object
   sunday: object
   encounter_time: object
   is_cancelled: object

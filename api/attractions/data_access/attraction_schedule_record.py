from dataclasses import dataclass


@dataclass( frozen=True )
class AttractionScheduleRecord:
   attraction: object
   schedule_start_date: object
   schedule_end_date: object
   monday: object
   tuesday: object
   wednesday: object
   thursday: object
   friday: object
   saturday: object
   sunday: object
   holidays_only: object
   schedule_message: object

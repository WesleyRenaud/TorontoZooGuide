from dataclasses import dataclass


@dataclass( frozen=True )
class GuardiansTalkScheduleRecord:
   name: object
   location: object
   x_coord: object
   y_coord: object
   maximum_duration: object
   schedule_start_date: object
   schedule_end_date: object
   monday: object
   tuesday: object
   wednesday: object
   thursday: object
   friday: object
   saturday: object
   sunday: object
   talk_time: object

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
   monday_time: object
   tuesday_time: object
   wednesday_time: object
   thursday_time: object
   friday_time: object
   saturday_time: object
   sunday_time: object

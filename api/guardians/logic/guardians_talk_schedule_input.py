from dataclasses import dataclass


@dataclass( frozen=True )
class GuardiansTalkScheduleInput:
   talk_name: str
   location: str
   start_date: str
   end_date: object
   monday_time: object
   tuesday_time: object
   wednesday_time: object
   thursday_time: object
   friday_time: object
   saturday_time: object
   sunday_time: object
   message: str

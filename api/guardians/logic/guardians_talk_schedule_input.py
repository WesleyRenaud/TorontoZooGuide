from dataclasses import dataclass


@dataclass( frozen=True )
class GuardiansTalkScheduleInput:
   talk_name: str
   location: str
   start_date: str
   end_date: object
   talk_time: str
   monday: bool
   tuesday: bool
   wednesday: bool
   thursday: bool
   friday: bool
   saturday: bool
   sunday: bool
   message: str

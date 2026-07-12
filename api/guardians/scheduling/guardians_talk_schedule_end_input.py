from dataclasses import dataclass


@dataclass( frozen=True )
class GuardiansTalkScheduleEndInput:
   talk_name: str
   location: str
   schedule_end_date: str
   talk_time: str

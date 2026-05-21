from dataclasses import dataclass


@dataclass( frozen=True )
class GuardiansTalkCancellationInput:
   talk_name: str
   location: str
   cancellation_date: str
   talk_time: str

from dataclasses import dataclass


@dataclass( frozen=True )
class AnimalViewabilityContext:
   calendar_month: int
   day_of_month: int
   target_date: object
   temp: float
   sigma: int

from dataclasses import dataclass


@dataclass( frozen=True )
class DrinkingFountainClosedStatus:
   start_date: object
   end_date: object
   message: str

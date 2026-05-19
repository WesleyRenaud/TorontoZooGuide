from dataclasses import dataclass


@dataclass( frozen=True )
class DrinkingFountainStatusRecord:
   is_closed: object
   start_date: object
   end_date: object
   closed_message: object

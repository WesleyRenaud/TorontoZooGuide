from dataclasses import dataclass


@dataclass( frozen=True )
class WildEncounterRecord:
   name: object
   meeting_spot: object
   link: object
   maximum_duration: object
   x_coord: object
   y_coord: object

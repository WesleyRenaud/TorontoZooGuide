from dataclasses import dataclass


@dataclass( frozen=True )
class ExhibitClosureRecord:
   exhibit: object
   closed_start: object
   closed_end: object

from dataclasses import dataclass


@dataclass( frozen=True )
class ItineraryAnimalInput:
   species: str
   exhibit: str
   is_added: bool = False

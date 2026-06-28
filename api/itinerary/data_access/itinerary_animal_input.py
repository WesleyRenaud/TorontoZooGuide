from dataclasses import dataclass


@dataclass( frozen=True )
class ItineraryAnimalInput:
   species: str
   exhibit: str
   enclosure_name: str | None = None
   is_added: bool = False

from dataclasses import dataclass

from ...animals.logic.animals_matching_query import species_exhibit_key_from_values


@dataclass( frozen=True )
class ItineraryAnimalRecord:
   species: object
   exhibit: object
   old_likelihood: object
   new_likelihood: object


   def species_exhibit_key( self ):
      return species_exhibit_key_from_values( self.species, self.exhibit )

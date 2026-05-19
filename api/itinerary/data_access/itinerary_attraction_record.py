from dataclasses import dataclass

from .itinerary_name_key import itinerary_name_key


@dataclass( frozen=True )
class ItineraryAttractionRecord:
   attraction: object
   old_likelihood: object
   new_likelihood: object


   def name_key( self ):
      return itinerary_name_key( self.attraction )

from dataclasses import dataclass

from .itinerary_name_key import itinerary_name_key


@dataclass( frozen=True )
class ItineraryWildEncounterRecord:
   wild_encounter: object
   start_time: object
   end_time: object
   is_deleted: object


   def name_key( self ):
      return itinerary_name_key( self.wild_encounter )

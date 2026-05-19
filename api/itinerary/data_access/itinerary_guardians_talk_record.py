from dataclasses import dataclass

from .itinerary_name_key import itinerary_name_key


@dataclass( frozen=True )
class ItineraryGuardiansTalkRecord:
   talk_name: object
   start_time: object
   end_time: object
   is_deleted: object


   def name_key( self ):
      return itinerary_name_key( self.talk_name )

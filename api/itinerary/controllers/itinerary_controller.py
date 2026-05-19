from ...animals.controllers.animal_controller import AnimalController
from ...attractions.controllers.attraction_controller import AttractionController
from ...guardians.controllers.guardians_controller import GuardiansController
from ...wild_encounters.controllers.wild_encounter_controller import WildEncounterController
from ..data_access.itinerary import fetch_saved_itinerary
from ..data_access import itinerary_persistence
from ..logic import set_itinerary as set_itinerary_logic
from ..logic.itinerary import build_current_itinerary


class ItineraryController():
   def __init__( self, conn ):
      self._conn = conn


   def get_itinerary( self ):
      return build_current_itinerary(
         saved_itinerary=fetch_saved_itinerary( self._conn ),
         animal_controller=AnimalController( self._conn ),
         attraction_controller=AttractionController( self._conn ),
         guardians_controller=GuardiansController( self._conn ),
         wild_encounter_controller=WildEncounterController( self._conn ) )


   def set_itinerary(
         self,
         date,
         animals,
         attractions,
         guardians_talks,
         wild_encounters ):
      return set_itinerary_logic.set_itinerary(
         self._conn,
         date=date,
         animals=animals,
         attractions=attractions,
         guardians_talks=guardians_talks,
         wild_encounters=wild_encounters,
         animal_controller=AnimalController( self._conn ),
         attraction_controller=AttractionController( self._conn ),
         guardians_controller=GuardiansController( self._conn ),
         wild_encounter_controller=WildEncounterController( self._conn ) )


   def clear_itinerary( self ):
      return itinerary_persistence.clear_itinerary( self._conn )

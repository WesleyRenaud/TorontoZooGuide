from __future__ import annotations

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.data_access.itinerary_transportation_record import ItineraryTransportationRecord
from api.itinerary.scheduling.bulk.loop_schedule_stop_extractor import LoopScheduleStopExtractor


SPLASH_ISLAND = 'Splash Island'
CAROUSEL = 'Conservation Carousel'
ZOOMOBILE = 'Zoomobile'

LION = ItineraryAnimalRecord(
   species='African Lion',
   exhibit='Africa Savanna',
   old_likelihood=None,
   new_likelihood=100,
)
SPLASH = ItineraryAttractionRecord(
   attraction=SPLASH_ISLAND,
   old_likelihood=None,
   new_likelihood=100,
)
ZOOMOBILE_ATTRACTION = ItineraryTransportationRecord(
   transportation=ZOOMOBILE,
   old_likelihood=None,
   new_likelihood=100,
   added_as_attraction=True,
)


def Test_AttractionsFrom_TestMixedStops_ExpectAttractionRowsOnly() -> None:
   attractions = LoopScheduleStopExtractor.attractions_from(
      [ LION, SPLASH, ZOOMOBILE_ATTRACTION ] )

   assert len( attractions ) == 1
   assert attractions[ 0 ].attraction == SPLASH_ISLAND


def Test_AnimalsFrom_TestMixedStops_ExpectAnimalRowsOnly() -> None:
   animals = LoopScheduleStopExtractor.animals_from(
      [ LION, SPLASH, ZOOMOBILE_ATTRACTION ] )

   assert len( animals ) == 1
   assert animals[ 0 ].species == 'African Lion'


def Test_TransportationsFrom_TestMixedStops_ExpectTransportationRowsOnly() -> None:
   transportations = LoopScheduleStopExtractor.transportations_from(
      [ LION, SPLASH, ZOOMOBILE_ATTRACTION ] )

   assert len( transportations ) == 1
   assert transportations[ 0 ].transportation == ZOOMOBILE

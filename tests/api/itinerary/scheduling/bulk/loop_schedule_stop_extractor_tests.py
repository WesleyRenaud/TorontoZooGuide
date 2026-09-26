from __future__ import annotations

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.data_access.itinerary_transportation_record import ItineraryTransportationRecord
from api.itinerary.scheduling.bulk.loop_schedule_stop_extractor import LoopScheduleStopExtractor
from api.shared.enums.position import Position
from api.shared.enums.transportation_name import TransportationName


SPLASH_ISLAND = 'Splash Island'
CAROUSEL = 'Conservation Carousel'
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
   transportation=TransportationName.ZOOMOBILE,
   old_likelihood=None,
   new_likelihood=100,
   added_as_attraction=True,
)
MIXED_STOPS = [ LION, SPLASH, ZOOMOBILE_ATTRACTION ]


def Test_AttractionsFrom_TestMixedStops_ExpectAttractionRowsOnly() -> None:
   attractions = LoopScheduleStopExtractor.attractions_from( MIXED_STOPS )

   assert attractions == [ SPLASH ]
   assert attractions[ Position.FIRST ].attraction == SPLASH.attraction


def Test_AnimalsFrom_TestMixedStops_ExpectAnimalRowsOnly() -> None:
   animals = LoopScheduleStopExtractor.animals_from( MIXED_STOPS )

   assert animals == [ LION ]
   assert animals[ Position.FIRST ].species == LION.species


def Test_TransportationsFrom_TestMixedStops_ExpectTransportationRowsOnly() -> None:
   transportations = LoopScheduleStopExtractor.transportations_from( MIXED_STOPS )

   assert transportations == [ ZOOMOBILE_ATTRACTION ]
   assert transportations[ Position.FIRST ].transportation == ZOOMOBILE_ATTRACTION.transportation

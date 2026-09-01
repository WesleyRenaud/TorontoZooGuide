from __future__ import annotations

from api.itinerary.results.itinerary_time_set_result import ItineraryTimeSetResult
from api.itinerary.results.itinerary_time_set_result_response_builder import ItineraryTimeSetResultResponseBuilder
from api.models import Itinerary
from api.shared.enums import ItineraryErrorType
from api.shared.itinerary_config_builder import ItineraryConfigBuilder


VISIT_DATE = '2026-06-15'

EMPTY_ITINERARY_PATH = {
   'stops': [],
   'legs': [],
   'points': [],
}

EMPTY_ITINERARY = {
   'date': VISIT_DATE,
   'arrival_time': None,
   'departure_time': None,
   'selected_exhibits': [],
   'animals': [],
   'attractions': [],
   'transportations': [],
   'transportation_stations': [],
   'guardians_talks': [],
   'wild_encounters': [],
   'events': [],
}


def Test_ToDict_TestItinerary_ExpectPayload() -> None:
   result = ItineraryTimeSetResult(
      itinerary=Itinerary(
         date=VISIT_DATE,
         arrival_time='9:45 AM',
      ) )

   assert ItineraryTimeSetResultResponseBuilder.to_dict( result ) == {
      'status': 'success',
      'reasons': [],
      'suppressed_warnings': [],
      'itinerary_config': ItineraryConfigBuilder.to_dict(),
      'itinerary_path': EMPTY_ITINERARY_PATH,
      'itinerary': {
         **EMPTY_ITINERARY,
         'arrival_time': '9:45 AM',
      },
   }


def Test_ToDict_TestNoItinerary_ExpectOmittedItinerary() -> None:
   result = ItineraryTimeSetResult()

   payload = ItineraryTimeSetResultResponseBuilder.to_dict( result )

   assert 'itinerary' not in payload
   assert payload[ 'itinerary_path' ] == EMPTY_ITINERARY_PATH


def Test_ToDict_TestSuppressedWarnings_ExpectWarningValues() -> None:
   result = ItineraryTimeSetResult(
      suppressed_warnings=[
         ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP,
      ],
      itinerary=Itinerary( date=VISIT_DATE ),
   )

   payload = ItineraryTimeSetResultResponseBuilder.to_dict( result )

   assert payload[ 'suppressed_warnings' ] == [
      'earlyAdmissionRequiresMembership',
   ]

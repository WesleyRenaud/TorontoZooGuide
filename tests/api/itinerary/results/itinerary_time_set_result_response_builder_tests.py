from __future__ import annotations

from api.itinerary.results.itinerary_path_builder import ItineraryPathBuilder
from api.itinerary.results.itinerary_time_set_result import ItineraryTimeSetResult
from api.itinerary.results.itinerary_time_set_result_response_builder import ItineraryTimeSetResultResponseBuilder
from api.models import Itinerary
from api.shared.enums import ItineraryErrorType
from api.shared.itinerary_config_builder import ItineraryConfigBuilder


VISIT_DATE = '2026-06-15'


def Test_ToDict_TestItinerary_ExpectPayload() -> None:
   arrival_time = '9:45 AM'
   result = ItineraryTimeSetResult(
      itinerary=Itinerary(
         date=VISIT_DATE,
         arrival_time=arrival_time,
      ) )

   payload = ItineraryTimeSetResultResponseBuilder.to_dict( result )

   assert payload[ 'status' ] == result.status.value
   assert payload[ 'reasons' ] == []
   assert payload[ 'suppressed_warnings' ] == []
   assert payload[ 'itinerary_config' ] == ItineraryConfigBuilder.to_dict()
   assert payload[ 'itinerary_path' ] == ItineraryPathBuilder.build( None )
   assert payload[ 'itinerary' ] == result.itinerary.to_dict()


def Test_ToDict_TestNoItinerary_ExpectOmittedItinerary() -> None:
   result = ItineraryTimeSetResult()

   payload = ItineraryTimeSetResultResponseBuilder.to_dict( result )

   assert 'itinerary' not in payload
   assert payload[ 'itinerary_path' ] == ItineraryPathBuilder.build( None )


def Test_ToDict_TestSuppressedWarnings_ExpectWarningValues() -> None:
   result = ItineraryTimeSetResult(
      suppressed_warnings=[
         ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP,
      ],
      itinerary=Itinerary( date=VISIT_DATE ),
   )

   payload = ItineraryTimeSetResultResponseBuilder.to_dict( result )

   assert payload[ 'suppressed_warnings' ] == [
      warning.value for warning in result.suppressed_warnings
   ]


def Test_ToDict_TestExtraPayload_ExpectMerged() -> None:
   result = ItineraryTimeSetResult()
   extra = { 'custom_flag': True }

   payload = ItineraryTimeSetResultResponseBuilder.to_dict(
      result,
      extra=extra,
   )

   assert payload[ 'custom_flag' ] is extra[ 'custom_flag' ]
   assert 'itinerary' not in payload

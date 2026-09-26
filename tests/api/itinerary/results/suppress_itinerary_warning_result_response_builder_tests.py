from __future__ import annotations

from api.itinerary.operations.suppress_itinerary_warning_result import SuppressItineraryWarningResult
from api.itinerary.results.suppress_itinerary_warning_result_response_builder import SuppressItineraryWarningResultResponseBuilder
from api.shared.itinerary_config_builder import ItineraryConfigBuilder


def Test_ToDict_TestSuccess_ExpectPayload() -> None:
   result = SuppressItineraryWarningResult()

   payload = SuppressItineraryWarningResultResponseBuilder.to_dict( result )

   assert payload[ 'status' ] == result.status.value
   assert payload[ 'reasons' ] == []
   assert payload[ 'suppressed_warnings' ] == []
   assert payload[ 'itinerary_config' ] == ItineraryConfigBuilder.to_dict()

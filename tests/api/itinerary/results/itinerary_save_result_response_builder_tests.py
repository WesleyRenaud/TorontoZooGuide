from __future__ import annotations

from api.itinerary.domain.itinerary_adjustment import ItineraryAdjustment
from api.itinerary.domain.itinerary_adjustment_reason import ItineraryAdjustmentReason
from api.itinerary.results.itinerary_path_builder import ItineraryPathBuilder
from api.itinerary.results.itinerary_result_reason import ItineraryResultReason
from api.itinerary.results.itinerary_save_result import ItinerarySaveResult
from api.itinerary.results.itinerary_save_result_response_builder import ItinerarySaveResultResponseBuilder
from api.models import Itinerary
from api.shared.enums import ItineraryAdjustmentType
from api.shared.enums import ItineraryErrorType
from api.shared.itinerary_config_builder import ItineraryConfigBuilder


VISIT_DATE = '2026-06-15'

ARRIVAL_ADJUSTMENT = ItineraryAdjustment(
   type=ItineraryAdjustmentType.ARRIVAL_TIME_ADJUSTED,
   field='arrivalTime',
   previous_value='9:15 AM',
   value='09:30',
   reason=ItineraryAdjustmentReason.ARRIVAL_OUTSIDE_ADMISSION_HOURS,
)


def Test_ToDict_TestMinimalResult_ExpectStatusAndItinerary() -> None:
   result = ItinerarySaveResult(
      itinerary=Itinerary( date=VISIT_DATE ) )

   payload = ItinerarySaveResultResponseBuilder.to_dict( result )

   assert payload[ 'status' ] == result.status.value
   assert payload[ 'reasons' ] == []
   assert payload[ 'adjustments' ] == []
   assert payload[ 'suppressed_warnings' ] == []
   assert payload[ 'itinerary' ] == result.itinerary.to_dict()
   assert payload[ 'itinerary_path' ] == ItineraryPathBuilder.build( None )


def Test_ToDict_TestResultWithAdjustment_ExpectAdjustments() -> None:
   date = '2026-06-22'
   arrival_time = '9:30 AM'
   result = ItinerarySaveResult(
      itinerary=Itinerary(
         date=date,
         arrival_time=arrival_time ),
      adjustments=[ ARRIVAL_ADJUSTMENT ] )

   payload = ItinerarySaveResultResponseBuilder.to_dict( result )

   assert payload[ 'adjustments' ] == [
      adjustment.to_dict() for adjustment in result.adjustments
   ]


def Test_ToDict_TestResultWithReason_ExpectReasonCodes() -> None:
   reason = ItineraryResultReason(
      code=ItineraryErrorType.ITEM_NOT_ON_ITINERARY )
   result = ItinerarySaveResult(
      status=ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
      itinerary=Itinerary( date=VISIT_DATE ),
      reasons=[ reason ] )

   payload = ItinerarySaveResultResponseBuilder.to_dict( result )

   assert payload[ 'status' ] == result.status.value
   assert payload[ 'reasons' ] == [ item.to_dict() for item in result.reasons ]


def Test_ToDict_TestExcludeItinerary_ExpectNoItineraryKeys() -> None:
   result = ItinerarySaveResult(
      itinerary=Itinerary( date=VISIT_DATE ) )

   payload = ItinerarySaveResultResponseBuilder.to_dict(
      result,
      include_itinerary=False )

   assert 'itinerary' not in payload
   assert 'itinerary_path' not in payload


def Test_ToDict_TestIncludeConfig_ExpectConfig() -> None:
   result = ItinerarySaveResult(
      itinerary=Itinerary( date=VISIT_DATE ) )

   payload = ItinerarySaveResultResponseBuilder.to_dict(
      result,
      include_config=True )

   assert payload[ 'itinerary_config' ] == ItineraryConfigBuilder.to_dict()


def Test_ToDict_TestExtra_ExpectMergedPayload() -> None:
   result = ItinerarySaveResult(
      itinerary=Itinerary( date=VISIT_DATE ) )
   extra = { 'customField': 'value' }

   payload = ItinerarySaveResultResponseBuilder.to_dict(
      result,
      extra=extra )

   assert payload[ 'customField' ] == extra[ 'customField' ]

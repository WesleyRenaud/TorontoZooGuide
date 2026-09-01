from __future__ import annotations

from api.itinerary.domain.itinerary_adjustment import ItineraryAdjustment
from api.itinerary.domain.itinerary_adjustment_reason import ItineraryAdjustmentReason
from api.itinerary.domain.itinerary_adjustment_type import ItineraryAdjustmentType
from api.itinerary.results.itinerary_result_reason import ItineraryResultReason
from api.itinerary.results.itinerary_save_result import ItinerarySaveResult
from api.itinerary.results.itinerary_save_result_response_builder import ItinerarySaveResultResponseBuilder
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

   assert ItinerarySaveResultResponseBuilder.to_dict( result ) == {
      'status': 'success',
      'reasons': [],
      'adjustments': [],
      'suppressed_warnings': [],
      'itinerary': EMPTY_ITINERARY,
      'itinerary_path': EMPTY_ITINERARY_PATH,
   }


def Test_ToDict_TestResultWithAdjustment_ExpectAdjustments() -> None:
   result = ItinerarySaveResult(
      itinerary=Itinerary(
         date='2026-06-22',
         arrival_time='9:30 AM',
      ),
      adjustments=[ ARRIVAL_ADJUSTMENT ],
   )

   payload = ItinerarySaveResultResponseBuilder.to_dict( result )

   assert payload[ 'adjustments' ] == [
      {
         'type': 'arrivalTimeAdjusted',
         'field': 'arrivalTime',
         'previous_value': '9:15 AM',
         'value': '09:30',
         'reason': 'arrivalOutsideAdmissionHours',
      },
   ]


def Test_ToDict_TestResultWithReason_ExpectReasonCodes() -> None:
   result = ItinerarySaveResult(
      status=ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
      itinerary=Itinerary( date=VISIT_DATE ),
      reasons=[
         ItineraryResultReason(
            code=ItineraryErrorType.ITEM_NOT_ON_ITINERARY ),
      ],
   )

   payload = ItinerarySaveResultResponseBuilder.to_dict( result )

   assert payload[ 'status' ] == 'itemNotOnItinerary'
   assert payload[ 'reasons' ] == [
      {
         'code': 'itemNotOnItinerary',
         'items': [],
      },
   ]


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

   payload = ItinerarySaveResultResponseBuilder.to_dict(
      result,
      extra={ 'customField': 'value' } )

   assert payload[ 'customField' ] == 'value'

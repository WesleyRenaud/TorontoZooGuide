from __future__ import annotations

from api.shared.api_error_response_applier import ApiErrorResponseApplier
from api.shared.api_operation_failure import ApiOperationFailure
from api.shared.enums.api_error_type import ApiErrorType


def Test_ApplyError_TestParams_ExpectApiErrorTypeAndParams() -> None:
   response: dict[ str, object ] = { 'success': False }

   ApiErrorResponseApplier.apply_error(
      response,
      ApiErrorType.COULD_NOT_SET_GUARDIANS_TALK_SCHEDULE,
      talk='African Lion',
      location='Africa Savanna' )

   assert response == {
      'success': False,
      'apiErrorType': 'couldNotSetGuardiansTalkSchedule',
      'apiErrorParams': {
         'talk': 'African Lion',
         'location': 'Africa Savanna',
      },
   }


def Test_ApplyFailure_TestOperationFailure_ExpectAppliesFailureFields() -> None:
   response: dict[ str, object ] = { 'success': False }
   failure = ApiOperationFailure(
      error_type=ApiErrorType.GUARDIANS_TALK_OCCURRENCE_ALREADY_EXISTS,
      params={
         'talk': 'African Lion',
         'location': 'Africa Savanna',
         'date': '2026-06-20',
         'talkTime': '3:00 PM',
      } )

   ApiErrorResponseApplier.apply_failure( response, failure )

   assert response[ 'apiErrorType' ] == 'guardiansTalkOccurrenceAlreadyExists'
   assert response[ 'apiErrorParams' ] == failure.params

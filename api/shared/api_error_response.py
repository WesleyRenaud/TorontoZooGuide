from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .enums.api_error_type import ApiErrorType


@dataclass( frozen=True )
class ApiOperationFailure:
   error_type: ApiErrorType
   params: dict[ str, Any ]


class ApiErrorResponseApplier():
   @classmethod
   def apply_error(
         cls,
         response: dict[ str, Any ],
         error_type: ApiErrorType,
         **params: object ) -> None:
      response[ 'apiErrorType' ] = error_type.value

      if params:
         response[ 'apiErrorParams' ] = params


   @classmethod
   def apply_failure(
         cls,
         response: dict[ str, Any ],
         failure: ApiOperationFailure ) -> None:
      cls.apply_error( response, failure.error_type, **failure.params )

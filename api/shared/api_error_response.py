from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .enums.api_error_type import ApiErrorType


@dataclass( frozen=True )
class ApiOperationFailure:
   error_type: ApiErrorType
   params: dict[ str, Any ]


def apply_api_error(
      response: dict[ str, Any ],
      error_type: ApiErrorType,
      **params: object ) -> None:
   response[ 'apiErrorType' ] = error_type.value

   if params:
      response[ 'apiErrorParams' ] = params


def apply_api_failure(
      response: dict[ str, Any ],
      failure: ApiOperationFailure ) -> None:
   apply_api_error( response, failure.error_type, **failure.params )

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .enums.api_error_type import ApiErrorType


@dataclass( frozen=True )
class ApiOperationFailure:
   error_type: ApiErrorType
   params: dict[ str, Any ]

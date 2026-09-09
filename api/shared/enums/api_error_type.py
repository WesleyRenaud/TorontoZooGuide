from __future__ import annotations

from enum import Enum

from .shared_enum_values import SharedEnumValues


ApiErrorType = Enum(
   'ApiErrorType',
   SharedEnumValues.load( 'apiErrorType.json' ),
   type=str,
)

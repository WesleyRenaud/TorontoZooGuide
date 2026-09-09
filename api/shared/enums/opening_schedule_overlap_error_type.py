from __future__ import annotations

from enum import Enum

from .shared_enum_values import SharedEnumValues


OpeningScheduleOverlapErrorType = Enum(
   'OpeningScheduleOverlapErrorType',
   SharedEnumValues.load( 'openingScheduleOverlapErrorType.json' ),
   type=str,
)

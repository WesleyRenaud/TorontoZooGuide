from __future__ import annotations

from enum import Enum

from .shared_enum_values import SharedEnumValues


OpeningScheduleOverlapResolution = Enum(
   'OpeningScheduleOverlapResolution',
   SharedEnumValues.load( 'openingScheduleOverlapResolution.json' ),
   type=str,
)

from __future__ import annotations

from enum import Enum

from .shared_enum_values import SharedEnumValues


TransportationName = Enum(
   'TransportationName',
   SharedEnumValues.load( 'transportationName.json' ),
   type=str,
)

from __future__ import annotations

from enum import Enum

from .shared_enum_values import SharedEnumValues


ItemType = Enum(
   'ItemType',
   SharedEnumValues.load( 'itemType.json' ),
   type=str,
)

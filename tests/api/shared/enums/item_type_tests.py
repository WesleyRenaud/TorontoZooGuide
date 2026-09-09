from __future__ import annotations

import json
from pathlib import Path

from api.shared.enums.item_type import ItemType
from api.shared.enums.shared_enum_values import SharedEnumValues


def Test_ItemType_TestEquality_ExpectMatchesWireString() -> None:
   assert ItemType.ATTRACTION == ItemType.ATTRACTION.value
   assert ItemType.RESTAURANT == ItemType.RESTAURANT.value


def Test_ItemType_TestSharedJson_ExpectSingleSourceOfTruth() -> None:
   shared_members = SharedEnumValues.load( 'itemType.json' )
   actual = {
      name: member.value
      for name, member in ItemType.__members__.items()
   }

   assert actual == shared_members

   raw = json.loads(
      ( Path( SharedEnumValues.shared_enums_directory() ) / 'itemType.json' )
      .read_text( encoding='utf-8' )
   )
   assert dict( sorted( raw.items() ) ) == shared_members

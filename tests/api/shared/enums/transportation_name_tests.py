from __future__ import annotations

import json
from pathlib import Path

from api.shared.enums.shared_enum_values import SharedEnumValues
from api.shared.enums.transportation_name import TransportationName


def Test_TransportationName_TestSharedJson_ExpectSingleSourceOfTruth() -> None:
   shared_members = SharedEnumValues.load( 'transportationName.json' )
   actual = {
      name: member.value
      for name, member in TransportationName.__members__.items()
   }

   assert actual == shared_members

   raw = json.loads(
      ( Path( SharedEnumValues.shared_enums_directory() ) / 'transportationName.json' )
      .read_text( encoding='utf-8' )
   )
   assert dict( sorted( raw.items() ) ) == shared_members

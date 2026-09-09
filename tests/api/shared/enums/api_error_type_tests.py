from __future__ import annotations

import json
from pathlib import Path

from api.shared.enums.api_error_type import ApiErrorType
from api.shared.enums.shared_enum_values import SharedEnumValues


def Test_ApiErrorType_TestSharedJson_ExpectSingleSourceOfTruth() -> None:
   shared_members = SharedEnumValues.load( 'apiErrorType.json' )
   actual = {
      name: member.value
      for name, member in ApiErrorType.__members__.items()
   }

   assert actual == shared_members

   raw = json.loads(
      ( Path( SharedEnumValues.shared_enums_directory() ) / 'apiErrorType.json' )
      .read_text( encoding='utf-8' )
   )
   assert dict( sorted( raw.items() ) ) == shared_members

from __future__ import annotations

import json
from pathlib import Path

from api.shared.enums.opening_schedule_overlap_error_type import OpeningScheduleOverlapErrorType
from api.shared.enums.shared_enum_values import SharedEnumValues


def Test_OpeningScheduleOverlapErrorType_TestSharedJson_ExpectSingleSourceOfTruth() -> None:
   shared_members = SharedEnumValues.load( 'openingScheduleOverlapErrorType.json' )
   actual = {
      name: member.value
      for name, member in OpeningScheduleOverlapErrorType.__members__.items()
   }

   assert actual == shared_members

   raw = json.loads(
      ( Path( SharedEnumValues.shared_enums_directory() ) / 'openingScheduleOverlapErrorType.json' )
      .read_text( encoding='utf-8' )
   )
   assert dict( sorted( raw.items() ) ) == shared_members

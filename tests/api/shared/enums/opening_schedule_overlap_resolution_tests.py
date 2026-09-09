from __future__ import annotations

import json
from pathlib import Path

from api.shared.enums.opening_schedule_overlap_resolution import OpeningScheduleOverlapResolution
from api.shared.enums.shared_enum_values import SharedEnumValues


def Test_OpeningScheduleOverlapResolution_TestSharedJson_ExpectSingleSourceOfTruth() -> None:
   shared_members = SharedEnumValues.load( 'openingScheduleOverlapResolution.json' )
   actual = {
      name: member.value
      for name, member in OpeningScheduleOverlapResolution.__members__.items()
   }

   assert actual == shared_members

   raw = json.loads(
      ( Path( SharedEnumValues.shared_enums_directory() ) / 'openingScheduleOverlapResolution.json' )
      .read_text( encoding='utf-8' )
   )
   assert dict( sorted( raw.items() ) ) == shared_members

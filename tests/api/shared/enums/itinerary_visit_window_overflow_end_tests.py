from __future__ import annotations

import json
from pathlib import Path

from api.shared.enums.itinerary_visit_window_overflow_end import ItineraryVisitWindowOverflowEnd
from api.shared.enums.shared_enum_values import SharedEnumValues


def Test_ItineraryVisitWindowOverflowEnd_TestSharedJson_ExpectSingleSourceOfTruth() -> None:
   shared_members = SharedEnumValues.load( 'itineraryVisitWindowOverflowEnd.json' )

   actual = {
      name: member.value
      for name, member in ItineraryVisitWindowOverflowEnd.__members__.items()
   }

   assert actual == shared_members

   raw = json.loads(
      (
         Path( SharedEnumValues.shared_enums_directory() )
         / 'itineraryVisitWindowOverflowEnd.json'
      ).read_text( encoding='utf-8' ) )
   assert dict( sorted( raw.items() ) ) == shared_members

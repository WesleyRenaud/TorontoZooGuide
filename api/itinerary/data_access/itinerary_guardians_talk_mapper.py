from __future__ import annotations

from .itinerary_guardians_talk_record import ItineraryGuardiansTalkRecord
from ...shared.value_conversion import ValueConversion
from ...types import Row


class ItineraryGuardiansTalkMapper():
   @classmethod
   def map_record( cls, row: Row ) -> ItineraryGuardiansTalkRecord:
      return ItineraryGuardiansTalkRecord(
         talk_name=row[ 'TALK_NAME' ],
         start_time=row[ 'START_TIME' ],
         end_time=row[ 'END_TIME' ],
         is_deleted=ValueConversion.as_boolean( row[ 'IS_DELETED' ] ) )


   @classmethod
   def map_records( cls, rows: list[ Row ] ) -> list[ ItineraryGuardiansTalkRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]

from __future__ import annotations

from collections.abc import Iterable

from ...zoo_util import ZooUtil
from ...types import Row
from .itinerary_guardians_talk_record import ItineraryGuardiansTalkRecord


def map_itinerary_guardians_talk_record( row: Row ) -> ItineraryGuardiansTalkRecord:
   return ItineraryGuardiansTalkRecord(
      talk_name=row[ 'TALK_NAME' ],
      start_time=row[ 'START_TIME' ],
      end_time=row[ 'END_TIME' ],
      is_deleted=ZooUtil.as_boolean( row[ 'IS_DELETED' ] ) )


def map_itinerary_guardians_talk_records( rows: Iterable[ Row ] ) -> list[ ItineraryGuardiansTalkRecord ]:
   return [
      map_itinerary_guardians_talk_record( row )
      for row in rows
   ]

from __future__ import annotations

from .itinerary_event_default_mapper import ItineraryEventDefaultMapper
from .itinerary_event_default_record import ItineraryEventDefaultRecord
from ...types import Connection


def fetch_itinerary_event_default_records(
      conn: Connection ) -> list[ ItineraryEventDefaultRecord ]:
   cur = conn.cursor()

   rows = cur.execute(
      """   SELECT
               EVENT_TYPE,
               DEFAULT_ITINERARY_DURATION_MINUTES
            FROM ItineraryEventDefault
            ORDER BY EVENT_TYPE;
      """
   ).fetchall()

   cur.close()

   return ItineraryEventDefaultMapper.map_records( rows )

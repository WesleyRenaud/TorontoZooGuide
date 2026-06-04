from __future__ import annotations

from ...shared.duration_values import normalize_duration_seconds
from ...shared.enums import ItineraryEventType
from ...types import Connection


def fetch_enclosure_default_duration_seconds(
      conn: Connection,
      species: str,
      exhibit: str ) -> int | None:
   cur = conn.cursor()

   row = cur.execute(
      """   SELECT DEFAULT_ITINERARY_DURATION_MINUTES
            FROM Enclosure
            WHERE SPECIES = ?
              AND EXHIBIT = ?;
      """,
      ( species, exhibit ),
   ).fetchone()

   cur.close()

   if row is None:
      return None

   return normalize_duration_seconds( row[ 'DEFAULT_ITINERARY_DURATION_MINUTES' ] )


def fetch_attraction_default_duration_seconds(
      conn: Connection,
      attraction: str ) -> int | None:
   cur = conn.cursor()

   row = cur.execute(
      """   SELECT DEFAULT_ITINERARY_DURATION_MINUTES
            FROM Attraction
            WHERE NAME = ?;
      """,
      ( attraction, ),
   ).fetchone()

   cur.close()

   if row is None:
      return None

   return normalize_duration_seconds( row[ 'DEFAULT_ITINERARY_DURATION_MINUTES' ] )


def fetch_event_default_duration_seconds(
      conn: Connection,
      event_type: ItineraryEventType ) -> int | None:
   cur = conn.cursor()

   row = cur.execute(
      """   SELECT DEFAULT_ITINERARY_DURATION_MINUTES
            FROM ItineraryEventDefault
            WHERE EVENT_TYPE = ?;
      """,
      ( event_type.value, ),
   ).fetchone()

   cur.close()

   if row is None:
      return None

   return normalize_duration_seconds( row[ 'DEFAULT_ITINERARY_DURATION_MINUTES' ] )

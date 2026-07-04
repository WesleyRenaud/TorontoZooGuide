from __future__ import annotations

from ...shared.duration_values import normalize_duration_seconds
from ...shared.enums import ItineraryEventType
from ...types import Connection


def fetch_enclosure_viewing_default_duration_seconds(
      conn: Connection,
      species: str,
      exhibit: str,
      enclosure_name: str | None ) -> int | None:
   cur = conn.cursor()

   if enclosure_name is None:
      row = cur.execute(
         """   SELECT DEFAULT_ITINERARY_DURATION_MINUTES
               FROM EnclosureViewing
               WHERE SPECIES = ?
                 AND EXHIBIT = ?
                 AND NAME IS NULL;
         """,
         ( species, exhibit ),
      ).fetchone()
   else:
      row = cur.execute(
         """   SELECT DEFAULT_ITINERARY_DURATION_MINUTES
               FROM EnclosureViewing
               WHERE SPECIES = ?
                 AND EXHIBIT = ?
                 AND NAME = ?;
         """,
         ( species, exhibit, enclosure_name ),
      ).fetchone()

   cur.close()

   if row is None or row[ 'DEFAULT_ITINERARY_DURATION_MINUTES' ] is None:
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

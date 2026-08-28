from __future__ import annotations

from ...shared.duration_values import DurationValues
from ...shared.enums import ItineraryEventType
from ...types import Types


class ItineraryDefaultDurationProvider():
   @classmethod
   def fetch_enclosure_viewing_default_duration_seconds(
         cls,
         conn: Types.Connection,
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

      return DurationValues.normalize_seconds( row[ 'DEFAULT_ITINERARY_DURATION_MINUTES' ] )


   @classmethod
   def fetch_attraction_default_duration_seconds(
         cls,
         conn: Types.Connection,
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

      return DurationValues.normalize_seconds( row[ 'DEFAULT_ITINERARY_DURATION_MINUTES' ] )


   @classmethod
   def fetch_event_default_duration_seconds(
         cls,
         conn: Types.Connection,
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

      return DurationValues.normalize_seconds( row[ 'DEFAULT_ITINERARY_DURATION_MINUTES' ] )

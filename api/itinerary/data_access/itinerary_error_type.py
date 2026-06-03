from __future__ import annotations

from ...shared.enums import ItineraryErrorType
from ...types import Connection


def is_itinerary_error_suppressable(
      conn: Connection,
      error_type: ItineraryErrorType ) -> bool:
   cur = conn.cursor()

   row = cur.execute(
      """   SELECT IS_SUPPRESSABLE
            FROM ItineraryErrorType
            WHERE ERROR_TYPE = ?;
      """,
      ( error_type.value, ),
   ).fetchone()

   cur.close()

   return bool( row and row[ 0 ] )

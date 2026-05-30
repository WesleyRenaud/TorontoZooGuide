from __future__ import annotations

from ...shared.enums import ItineraryErrorType
from ...types import Connection, Cursor


def clear_itinerary_error_suppressions( cur: Cursor ) -> None:
   cur.execute( 'DELETE FROM ItineraryErrorSuppression;' )


def fetch_suppressed_error_type_values( conn: Connection ) -> list[ str ]:
   cur = conn.cursor()

   rows = cur.execute(
      """   SELECT ERROR_TYPE
            FROM ItineraryErrorSuppression
            WHERE SUPPRESS_WARNING = 1;
      """
   ).fetchall()

   cur.close()

   return [ str( row[ 0 ] ) for row in rows ]


def is_itinerary_error_suppressed(
      conn: Connection,
      error_type: ItineraryErrorType ) -> bool:
   cur = conn.cursor()

   row = cur.execute(
      """   SELECT SUPPRESS_WARNING
            FROM ItineraryErrorSuppression
            WHERE ERROR_TYPE = ?;
      """,
      ( error_type.value, )
   ).fetchone()

   cur.close()

   return bool( row and row[ 0 ] )


def suppress_itinerary_error(
      conn: Connection,
      error_type: ItineraryErrorType ) -> None:
   cur = conn.cursor()

   cur.execute(
      """   INSERT INTO ItineraryErrorSuppression (
               ERROR_TYPE,
               SUPPRESS_WARNING
            )
            VALUES ( ?, 1 )
            ON CONFLICT ( ERROR_TYPE ) DO UPDATE SET
               SUPPRESS_WARNING = 1;
      """,
      ( error_type.value, ) )

   conn.commit()
   cur.close()

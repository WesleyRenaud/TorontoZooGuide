from __future__ import annotations

from dataclasses import dataclass

from ...shared.enums import ItineraryErrorType
from ...types import Connection, Cursor


@dataclass( frozen=True )
class ItineraryStatusRecord:
   status: str
   is_suppressable: bool
   is_suppressed: bool


def fetch_itinerary_statuses( conn: Connection ) -> list[ ItineraryStatusRecord ]:
   cur = conn.cursor()

   rows = cur.execute(
      """   SELECT ItineraryStatus.STATUS,
                     ItineraryStatus.IS_SUPPRESSABLE,
                     COALESCE( ItineraryStatusSuppression.IS_SUPPRESSED, 0 )
            FROM ItineraryStatus
            LEFT JOIN ItineraryStatusSuppression
               ON ItineraryStatusSuppression.STATUS = ItineraryStatus.STATUS
            ORDER BY ItineraryStatus.STATUS;
      """
   ).fetchall()

   cur.close()

   return [
      ItineraryStatusRecord(
         status=str( row[ 0 ] ),
         is_suppressable=bool( row[ 1 ] ),
         is_suppressed=bool( row[ 2 ] ),
      )
      for row in rows
   ]


def fetch_suppressed_status_values( conn: Connection ) -> list[ str ]:
   cur = conn.cursor()

   rows = cur.execute(
      """   SELECT ItineraryStatus.STATUS
            FROM ItineraryStatus
            INNER JOIN ItineraryStatusSuppression
               ON ItineraryStatusSuppression.STATUS = ItineraryStatus.STATUS
            WHERE ItineraryStatus.IS_SUPPRESSABLE = 1
              AND ItineraryStatusSuppression.IS_SUPPRESSED = 1;
      """
   ).fetchall()

   cur.close()

   return [ str( row[ 0 ] ) for row in rows ]


def is_itinerary_status_suppressable(
      conn: Connection,
      error_type: ItineraryErrorType ) -> bool:
   cur = conn.cursor()

   row = cur.execute(
      """   SELECT IS_SUPPRESSABLE
            FROM ItineraryStatus
            WHERE STATUS = ?;
      """,
      ( error_type.value, ),
   ).fetchone()

   cur.close()

   return bool( row and row[ 0 ] )


def is_itinerary_error_suppressed(
      conn: Connection,
      error_type: ItineraryErrorType ) -> bool:
   if not is_itinerary_status_suppressable( conn, error_type ):
      return False

   cur = conn.cursor()

   row = cur.execute(
      """   SELECT ItineraryStatusSuppression.IS_SUPPRESSED
            FROM ItineraryStatusSuppression
            WHERE STATUS = ?;
      """,
      ( error_type.value, ),
   ).fetchone()

   cur.close()

   return bool( row and row[ 0 ] )


def suppress_itinerary_status(
      conn: Connection,
      error_type: ItineraryErrorType ) -> None:
   if not is_itinerary_status_suppressable( conn, error_type ):
      return

   cur = conn.cursor()

   cur.execute(
      """   INSERT INTO ItineraryStatusSuppression (
               STATUS,
               IS_SUPPRESSED
            )
            VALUES ( ?, 1 )
            ON CONFLICT ( STATUS ) DO UPDATE SET
               IS_SUPPRESSED = 1;
      """,
      ( error_type.value, ),
   )

   conn.commit()
   cur.close()


def clear_itinerary_status_suppressions( cur: Cursor ) -> None:
   cur.execute( 'DELETE FROM ItineraryStatusSuppression;' )

from __future__ import annotations

from .itinerary_status_record import ItineraryStatusRecord
from ...shared.enums import ItineraryErrorType
from ...shared.enums.position import Position
from ...types import Types


class ItineraryStatusProvider():
   @classmethod
   def fetch_itinerary_statuses( cls, conn: Types.Connection ) -> list[ ItineraryStatusRecord ]:
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
            status=str( row[ Position.FIRST ] ),
            is_suppressable=bool( row[ Position.SECOND ] ),
            is_suppressed=bool( row[ Position.THIRD ] ),
         )
         for row in rows
      ]


   @classmethod
   def fetch_suppressed_status_values( cls, conn: Types.Connection ) -> list[ str ]:
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

      return [ str( row[ Position.FIRST ] ) for row in rows ]


   @classmethod
   def is_itinerary_status_suppressable(
         cls,
         conn: Types.Connection,
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

      return bool( row and row[ Position.FIRST ] )


   @classmethod
   def is_itinerary_error_suppressed(
         cls,
         conn: Types.Connection,
         error_type: ItineraryErrorType ) -> bool:
      if not cls.is_itinerary_status_suppressable( conn, error_type ):
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

      return bool( row and row[ Position.FIRST ] )


   @classmethod
   def suppress_itinerary_status(
         cls,
         conn: Types.Connection,
         error_type: ItineraryErrorType ) -> None:
      if not cls.is_itinerary_status_suppressable( conn, error_type ):
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


   @classmethod
   def clear_itinerary_status_suppressions( cls, cur: Types.Cursor ) -> None:
      cur.execute( 'DELETE FROM ItineraryStatusSuppression;' )

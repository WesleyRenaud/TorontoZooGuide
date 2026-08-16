from __future__ import annotations

from ...models.itinerary_transportation_leg import ItineraryTransportationLeg
from ...shared.calendar_dates import DateValues
from ...types import Cursor
from ...types import ScheduleTimeKey


def insert_itinerary_transportation(
      cur: Cursor,
      *,
      transportation: str,
      old_likelihood: int | None,
      new_likelihood: int | None,
      start_time: ScheduleTimeKey = None,
      end_time: ScheduleTimeKey = None ) -> bool:
   cur.execute(
      """   INSERT OR IGNORE INTO ItineraryTransportation (
               TRANSPORTATION,
               OLD_LIKELIHOOD,
               NEW_LIKELIHOOD,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, ?, ?, ? );
      """,
      (
         transportation,
         old_likelihood,
         new_likelihood,
         DateValues.normalize_itinerary_schedule_time( start_time ),
         DateValues.normalize_itinerary_schedule_time( end_time ),
      ),
   )

   return cur.rowcount > 0


def insert_itinerary_transportation_legs(
      cur: Cursor,
      *,
      transportation: str,
      legs: list[ ItineraryTransportationLeg ] ) -> None:
   for leg in legs:
      cur.execute(
         """   INSERT INTO ItineraryTransportationLeg (
                  TRANSPORTATION,
                  FROM_STATION,
                  TO_STATION,
                  START_TIME,
                  END_TIME
               )
               VALUES ( ?, ?, ?, ?, ? );
         """,
         (
            transportation,
            leg.from_station,
            leg.to_station,
            DateValues.normalize_itinerary_schedule_time( leg.start_time ),
            DateValues.normalize_itinerary_schedule_time( leg.end_time ),
         ),
      )


def delete_itinerary_transportation_legs(
      cur: Cursor,
      *,
      transportation: str ) -> None:
   cur.execute(
      """   DELETE FROM ItineraryTransportationLeg
            WHERE TRANSPORTATION = ?;
      """,
      ( transportation, ),
   )

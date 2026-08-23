from __future__ import annotations

from .itinerary_transportation_route_markers import clear_itinerary_transportation_route_markers
from .itinerary_transportation_route_markers import delete_itinerary_transportation_route_markers
from ...models.itinerary_transportation_leg import ItineraryTransportationLeg
from ...shared.calendar_dates import DateValues
from ...types import Cursor
from ...types import ScheduleTimeKey


def insert_itinerary_transportation(
      cur: Cursor,
      transportation: str,
      old_likelihood: int | None,
      new_likelihood: int | None,
      added_as_attraction: bool,
      start_time: ScheduleTimeKey = None,
      end_time: ScheduleTimeKey = None,
      route: str | None = None,
) -> bool:
   cur.execute(
      """   INSERT OR IGNORE INTO ItineraryTransportation (
               TRANSPORTATION,
               OLD_LIKELIHOOD,
               NEW_LIKELIHOOD,
               ADDED_AS_ATTRACTION,
               START_TIME,
               END_TIME,
               ROUTE
            )
            VALUES ( ?, ?, ?, ?, ?, ?, ? );
      """,
      (
         transportation,
         old_likelihood,
         new_likelihood,
         added_as_attraction,
         DateValues.normalize_itinerary_schedule_time( start_time ),
         DateValues.normalize_itinerary_schedule_time( end_time ),
         route,
      ),
   )

   return cur.rowcount > 0


def insert_itinerary_transportation_legs(
      cur: Cursor,
      transportation: str,
      added_as_attraction: bool,
      legs: list[ ItineraryTransportationLeg ] ) -> None:
   for leg in legs:
      cur.execute(
         """   INSERT INTO ItineraryTransportationLeg (
                  TRANSPORTATION,
                  ADDED_AS_ATTRACTION,
                  FROM_STATION,
                  TO_STATION,
                  START_TIME,
                  END_TIME
               )
               VALUES ( ?, ?, ?, ?, ?, ? );
         """,
         (
            transportation,
            added_as_attraction,
            leg.from_station,
            leg.to_station,
            DateValues.normalize_itinerary_schedule_time( leg.start_time ),
            DateValues.normalize_itinerary_schedule_time( leg.end_time ),
         ),
      )


def delete_itinerary_transportation_legs(
      cur: Cursor,
      transportation: str,
      added_as_attraction: bool ) -> None:
   cur.execute(
      """   DELETE FROM ItineraryTransportationLeg
            WHERE TRANSPORTATION = ?
              AND ADDED_AS_ATTRACTION = ?;
      """,
      ( transportation, added_as_attraction ),
   )


def clear_itinerary_transportation_legs( cur: Cursor ) -> None:
   cur.execute( 'DELETE FROM ItineraryTransportationLeg;' )


def delete_itinerary_transportation_row(
      cur: Cursor,
      transportation: str,
      added_as_attraction: bool ) -> None:
   cur.execute(
      """   DELETE FROM ItineraryTransportation
            WHERE TRANSPORTATION = ?
              AND ADDED_AS_ATTRACTION = ?;
      """,
      ( transportation, added_as_attraction ),
   )


def clear_itinerary_transportation_rows( cur: Cursor ) -> None:
   cur.execute( 'DELETE FROM ItineraryTransportation;' )


def clear_itinerary_transportation_schedule_times(
      cur: Cursor,
      transportation: str,
      added_as_attraction: bool ) -> None:
   cur.execute(
      """   UPDATE ItineraryTransportation
            SET START_TIME = NULL,
                END_TIME = NULL,
                ROUTE = NULL
            WHERE TRANSPORTATION = ?
              AND ADDED_AS_ATTRACTION = ?;
      """,
      ( transportation, added_as_attraction ),
   )


def clear_all_itinerary_transportation_schedule_times( cur: Cursor ) -> None:
   cur.execute(
      """   UPDATE ItineraryTransportation
            SET START_TIME = NULL,
                END_TIME = NULL,
                ROUTE = NULL;
      """ )


def delete_itinerary_transportation(
      cur: Cursor,
      transportation: str,
      added_as_attraction: bool ) -> None:
   delete_itinerary_transportation_route_markers(
      cur,
      transportation=transportation,
      added_as_attraction=added_as_attraction )
   delete_itinerary_transportation_legs(
      cur,
      transportation=transportation,
      added_as_attraction=added_as_attraction )
   delete_itinerary_transportation_row(
      cur,
      transportation=transportation,
      added_as_attraction=added_as_attraction )


def clear_itinerary_transportations( cur: Cursor ) -> None:
   clear_itinerary_transportation_route_markers( cur )
   clear_itinerary_transportation_legs( cur )
   clear_itinerary_transportation_rows( cur )

from __future__ import annotations

from dataclasses import dataclass

from ...animal_item_key import AnimalScheduleItemKey
from .attraction_or_transportation_duration import default_duration_seconds_for_attraction_or_transportation
from ...data_access.attraction_also_transportation import attraction_is_also_transportation
from ...data_access.itinerary import fetch_itinerary_date
from ...data_access.itinerary_default_duration import fetch_enclosure_viewing_default_duration_seconds
from ...data_access.schedule_itinerary_item import insert_itinerary_animal_schedule
from ...data_access.schedule_itinerary_item import insert_itinerary_attraction_schedule
from ...data_access.schedule_itinerary_item import update_itinerary_animal_schedule
from ...data_access.schedule_itinerary_item import update_itinerary_attraction_schedule
from ...data_access.schedule_itinerary_transportation import apply_itinerary_transportation_schedule
from .schedule_item_key import ListedScheduleItemKey
from ....shared.calendar_dates import DateValues
from ...transportation.resolve_transportation_day_loop import fetch_transportation_day_loop
from ....types import Connection
from ....types import Cursor
from ....types import ScheduleTimeKey


@dataclass( frozen=True )
class ListedScheduleTarget:
   default_duration_seconds: int | None


def resolve_listed_schedule_target(
      conn: Connection,
      schedule_item_key: ListedScheduleItemKey ) -> ListedScheduleTarget:
   if isinstance( schedule_item_key, AnimalScheduleItemKey ):
      return ListedScheduleTarget(
         default_duration_seconds=fetch_enclosure_viewing_default_duration_seconds(
            conn,
            schedule_item_key.species,
            schedule_item_key.exhibit,
            schedule_item_key.enclosure_name ) )

   return ListedScheduleTarget(
      default_duration_seconds=(
         default_duration_seconds_for_attraction_or_transportation(
            conn,
            schedule_item_key.name ) ) )


def apply_listed_schedule(
      cur: Cursor,
      schedule_item_key: ListedScheduleItemKey,
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey,
      insert_if_missing: bool ) -> bool:
   if isinstance( schedule_item_key, AnimalScheduleItemKey ):
      if insert_if_missing:
         inserted = insert_itinerary_animal_schedule(
            cur,
            species=schedule_item_key.species,
            exhibit=schedule_item_key.exhibit,
            enclosure_name=schedule_item_key.enclosure_name,
            start_time=start_time,
            end_time=end_time )

         if inserted:
            return True

      return update_itinerary_animal_schedule(
         cur,
         species=schedule_item_key.species,
         exhibit=schedule_item_key.exhibit,
         enclosure_name=schedule_item_key.enclosure_name,
         start_time=start_time,
         end_time=end_time )

   if attraction_is_also_transportation( cur.connection, schedule_item_key.name ):
      visit_date = fetch_itinerary_date( cur.connection )
      parsed_visit_date = DateValues.parse_date_value( visit_date )

      if parsed_visit_date is None:
         return False

      day_loop = fetch_transportation_day_loop(
         cur.connection,
         transportation=schedule_item_key.name,
         target_date=parsed_visit_date )

      if day_loop is None:
         return False

      return apply_itinerary_transportation_schedule(
         cur,
         name=schedule_item_key.name,
         start_time=start_time,
         legs=day_loop.legs,
         insert_if_missing=insert_if_missing )

   if insert_if_missing:
      inserted = insert_itinerary_attraction_schedule(
         cur,
         name=schedule_item_key.name,
         start_time=start_time,
         end_time=end_time )

      if inserted:
         return True

   return update_itinerary_attraction_schedule(
      cur,
      name=schedule_item_key.name,
      start_time=start_time,
      end_time=end_time )

from __future__ import annotations

from dataclasses import dataclass

from ...animal_item_key import AnimalScheduleItemKey
from ...attraction_item_key import AttractionScheduleItemKey
from ...data_access.itinerary_default_duration import fetch_attraction_default_duration_seconds
from ...data_access.itinerary_default_duration import fetch_enclosure_default_duration_seconds
from ...data_access.schedule_itinerary_item import insert_itinerary_animal_schedule
from ...data_access.schedule_itinerary_item import insert_itinerary_attraction_schedule
from ...data_access.schedule_itinerary_item import update_itinerary_animal_schedule
from ...data_access.schedule_itinerary_item import update_itinerary_attraction_schedule
from .schedule_item_key import ListedScheduleItemKey
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
         default_duration_seconds=fetch_enclosure_default_duration_seconds(
            conn,
            schedule_item_key.species,
            schedule_item_key.exhibit ) )

   return ListedScheduleTarget(
      default_duration_seconds=fetch_attraction_default_duration_seconds(
         conn,
         schedule_item_key.name ) )


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
            start_time=start_time,
            end_time=end_time )

         if inserted:
            return True

      return update_itinerary_animal_schedule(
         cur,
         species=schedule_item_key.species,
         exhibit=schedule_item_key.exhibit,
         start_time=start_time,
         end_time=end_time )

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

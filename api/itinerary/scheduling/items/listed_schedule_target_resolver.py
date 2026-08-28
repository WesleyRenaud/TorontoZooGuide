from __future__ import annotations

from ...animal_schedule_item_key import AnimalScheduleItemKey
from .attraction_or_transportation_duration_resolver import AttractionOrTransportationDurationResolver
from ...attraction_schedule_item_key import AttractionScheduleItemKey
from ...data_access.itinerary_default_duration_provider import ItineraryDefaultDurationProvider
from ...data_access.itinerary_provider import ItineraryProvider
from ...data_access.itinerary_transportation_record import ItineraryTransportationRecord
from ...data_access.saved_itinerary_schedule_item_row_finder import SavedItineraryScheduleItemRowFinder
from ...data_access.schedule_itinerary_item_provider import ScheduleItineraryItemProvider
from ...data_access.schedule_itinerary_transportation_provider import ScheduleItineraryTransportationProvider
from .listed_schedule_item_key import ListedScheduleItemKey
from .listed_schedule_target import ListedScheduleTarget
from ....shared.calendar_dates import DateValues
from ...transportation.transportation_day_loop_fetcher import TransportationDayLoopFetcher
from ....types import Types


class ListedScheduleTargetResolver():
   @classmethod
   def resolve(
         cls,
         conn: Types.Connection,
         schedule_item_key: ListedScheduleItemKey.Key ) -> ListedScheduleTarget:
      if isinstance( schedule_item_key, AnimalScheduleItemKey ):
         return ListedScheduleTarget(
            default_duration_seconds=ItineraryDefaultDurationProvider.fetch_enclosure_viewing_default_duration_seconds(
               conn,
               schedule_item_key.species,
               schedule_item_key.exhibit,
               schedule_item_key.enclosure_name ) )

      return ListedScheduleTarget(
         default_duration_seconds=(
            AttractionOrTransportationDurationResolver.default_seconds(
               conn,
               schedule_item_key.name ) ) )


   @classmethod
   def apply(
         cls,
         cur: Types.Cursor,
         schedule_item_key: ListedScheduleItemKey.Key,
         start_time: Types.ScheduleTimeKey,
         end_time: Types.ScheduleTimeKey,
         insert_if_missing: bool ) -> bool:
      if isinstance( schedule_item_key, AnimalScheduleItemKey ):
         if insert_if_missing:
            inserted = ScheduleItineraryItemProvider.insert_itinerary_animal_schedule(
               cur,
               species=schedule_item_key.species,
               exhibit=schedule_item_key.exhibit,
               enclosure_name=schedule_item_key.enclosure_name,
               start_time=start_time,
               end_time=end_time )

            if inserted:
               return True

         return ScheduleItineraryItemProvider.update_itinerary_animal_schedule(
            cur,
            species=schedule_item_key.species,
            exhibit=schedule_item_key.exhibit,
            enclosure_name=schedule_item_key.enclosure_name,
            start_time=start_time,
            end_time=end_time )

      if isinstance( schedule_item_key, AttractionScheduleItemKey ):
         saved_row = SavedItineraryScheduleItemRowFinder.find_saved_itinerary_schedule_item_row(
            ItineraryProvider.fetch_saved_itinerary( cur.connection ),
            schedule_item_key )

         if isinstance( saved_row, ItineraryTransportationRecord ):
            visit_date = ItineraryProvider.fetch_itinerary_date( cur.connection )
            parsed_visit_date = DateValues.parse_date_value( visit_date )

            if parsed_visit_date is None:
               return False

            day_loop = TransportationDayLoopFetcher.fetch(
               cur.connection,
               transportation=schedule_item_key.name,
               target_date=parsed_visit_date )

            if day_loop is None:
               return False

            return ScheduleItineraryTransportationProvider.apply_itinerary_transportation_schedule(
               cur,
               name=schedule_item_key.name,
               added_as_attraction=saved_row.added_as_attraction,
               start_time=start_time,
               route=day_loop.route,
               legs=day_loop.legs )

      if insert_if_missing:
         inserted = ScheduleItineraryItemProvider.insert_itinerary_attraction_schedule(
            cur,
            name=schedule_item_key.name,
            start_time=start_time,
            end_time=end_time )

         if inserted:
            return True

      return ScheduleItineraryItemProvider.update_itinerary_attraction_schedule(
         cur,
         name=schedule_item_key.name,
         start_time=start_time,
         end_time=end_time )

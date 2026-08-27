from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from ..core.time_block import TimeBlock
from ..core.time_block_builder import TimeBlockBuilder
from ...data_access.itinerary_attraction_record import ItineraryAttractionRecord
from ...data_access.itinerary_provider import ItineraryProvider
from ...data_access.itinerary_transportation_record import ItineraryTransportationRecord
from ...data_access.schedule_itinerary_item_provider import ScheduleItineraryItemProvider
from ...data_access.schedule_itinerary_transportation_provider import ScheduleItineraryTransportationProvider
from .loop_schedule_slot import LoopScheduleSlot
from ....shared.calendar_dates import DateValues
from ...transportation.resolve_transportation_day_loop import fetch_transportation_day_loop
from ....types import Connection


@dataclass
class LoopScheduleSlotSink:
   persist: bool = True
   slots: list[ LoopScheduleSlot ] = field( default_factory=list )


   def save(
         self,
         conn: Connection,
         blockers: list[ TimeBlock ],
         stop_slots: list[ LoopScheduleSlot ] ) -> bool:
      self.slots.extend( stop_slots )

      if self.persist and not self._persist_loop_group_slots(
            conn,
            stop_slots ):
         return False

      self._append_slots_to_blockers( blockers, stop_slots )
      return True


   @staticmethod
   def _append_slots_to_blockers(
         blockers: list[ TimeBlock ],
         slots: list[ LoopScheduleSlot ] ) -> None:
      for _, start_time, end_time in slots:
         scheduled_block = TimeBlockBuilder.from_schedule_times(
            start_time,
            end_time )

         if scheduled_block is not None:
            blockers.append( scheduled_block )


   @staticmethod
   def _persist_loop_group_slots(
         conn: Connection,
         scheduled_slots: list[ LoopScheduleSlot ] ) -> bool:
      cur = conn.cursor()

      try:
         for stop, start_time, end_time in scheduled_slots:
            if isinstance( stop, ItineraryAttractionRecord ):
               persisted = ScheduleItineraryItemProvider.update_itinerary_attraction_schedule(
                  cur,
                  name=stop.attraction,
                  start_time=start_time,
                  end_time=end_time )
            elif isinstance( stop, ItineraryTransportationRecord ):
               visit_date = ItineraryProvider.fetch_itinerary_date( conn )
               parsed_visit_date = DateValues.parse_date_value( visit_date )
               day_loop = (
                  fetch_transportation_day_loop(
                     conn,
                     transportation=stop.transportation,
                     target_date=parsed_visit_date )
                  if parsed_visit_date is not None
                  else None
               )

               if day_loop is None:
                  persisted = False
               else:
                  persisted = ScheduleItineraryTransportationProvider.apply_itinerary_transportation_schedule(
                     cur,
                     name=stop.transportation,
                     added_as_attraction=stop.added_as_attraction,
                     start_time=start_time,
                     route=day_loop.route,
                     legs=day_loop.legs )
            else:
               persisted = ScheduleItineraryItemProvider.update_itinerary_animal_schedule(
                  cur,
                  species=stop.species,
                  exhibit=stop.exhibit,
                  enclosure_name=stop.enclosure_name,
                  start_time=start_time,
                  end_time=end_time )

            if not persisted:
               conn.rollback()
               return False

         conn.commit()
         return True

      finally:
         cur.close()

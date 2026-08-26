from __future__ import annotations

from datetime import date

from ...attractions.coordinators.attraction_coordinator import AttractionCoordinator
from ..data_access.itinerary_transportation_input import ItineraryTransportationInput
from ..data_access.itinerary_transportation_record import ItineraryTransportationRecord
from ..data_access.itinerary_transportation_save_carryover_mapper import ItineraryTransportationSaveCarryoverMapper
from ..domain.itinerary_visit_window_builder import ItineraryVisitWindowBuilder
from ..domain.transportation_route_marker_sequences_builder import TransportationRouteMarkerSequencesBuilder
from ...models import TransportationDiff
from ...models.itinerary_transportation_leg import ItineraryTransportationLeg
from ..transportation.expand_timed_transportation_legs import expand_timed_transportation_legs
from ..transportation.resolve_transportation_day_loop import fetch_transportation_day_loop
from ..transportation.resolve_transportation_day_loop import resolve_transportation_route_for_date
from ...types import Connection, DateKey, ScheduleTimeKey


class ItineraryTransportationValidator():
   @classmethod
   def validate(
         cls,
         attraction_coordinator: type[ AttractionCoordinator ],
         conn: Connection,
         transportations: list[ ItineraryTransportationInput ],
         new_visit_date: date,
         *,
         arrival_time: ScheduleTimeKey,
         departure_time: ScheduleTimeKey,
         old_visit_date: DateKey | None = None,
         saved_transportation_rows: list[ ItineraryTransportationRecord ] | None = None,
         visit_date_is_changing: bool = False ) -> list[ TransportationDiff ]:
      diffs: list[ TransportationDiff ] = []

      for transportation in transportations:
         carryover = ItineraryTransportationSaveCarryoverMapper.map_from_saved_transportation_rows(
            saved_transportation_rows,
            transportation,
            old_visit_date=old_visit_date )

         new_likelihood = attraction_coordinator.get_attraction_likelihood_for_visit_date(
            visit_date=new_visit_date,
            attraction_name=transportation.name )
         start_time, end_time = (
            ( carryover.start_time, carryover.end_time )
            if visit_date_is_changing
            else ItineraryVisitWindowBuilder.cleared_schedule_times(
               carryover.start_time,
               carryover.end_time,
               arrival_time=arrival_time,
               departure_time=departure_time ) )
         bulk_transit_evaluated = (
            False
            if visit_date_is_changing
            else carryover.bulk_transit_evaluated )
         end_time, legs = cls._timed_legs_for_transportation_save(
            conn,
            transportation_name=transportation.name,
            visit_date=new_visit_date,
            start_time=start_time,
            end_time=end_time,
            carryover_legs=carryover.legs,
            visit_date_is_changing=visit_date_is_changing,
            added_as_attraction=transportation.added_as_attraction )

         if not legs:
            diffs.append(
               TransportationDiff(
                  name=carryover.name,
                  old_likelihood=carryover.old_likelihood,
                  new_likelihood=new_likelihood,
                  start_time=start_time,
                  end_time=end_time,
                  legs=legs,
                  added_as_attraction=transportation.added_as_attraction,
                  bulk_transit_evaluated=bulk_transit_evaluated,
               )
            )
            continue

         route = resolve_transportation_route_for_date(
            conn,
            transportation=transportation.name,
            target_date=new_visit_date,
         )
         diffs.append(
            TransportationDiff(
               name=carryover.name,
               old_likelihood=carryover.old_likelihood,
               new_likelihood=new_likelihood,
               start_time=start_time,
               end_time=end_time,
               legs=legs,
               route=route,
               route_marker_sequences=TransportationRouteMarkerSequencesBuilder.build(
                  conn,
                  transportation=transportation.name,
                  route=route,
                  legs=legs,
               ),
               added_as_attraction=transportation.added_as_attraction,
               bulk_transit_evaluated=bulk_transit_evaluated,
            )
         )

      return diffs


   @classmethod
   def _timed_legs_for_transportation_save(
         cls,
         conn: Connection,
         transportation_name: str,
         visit_date: date,
         start_time: ScheduleTimeKey,
         end_time: ScheduleTimeKey,
         carryover_legs: list[ ItineraryTransportationLeg ],
         visit_date_is_changing: bool,
         added_as_attraction: bool,
   ) -> tuple[ ScheduleTimeKey, list[ ItineraryTransportationLeg ] ]:
      if start_time is None:
         return None, []

      if not visit_date_is_changing:
         return end_time, list( carryover_legs )

      day_loop = fetch_transportation_day_loop(
         conn,
         transportation=transportation_name,
         target_date=visit_date )

      if day_loop is None:
         return end_time, []

      timed_legs, expanded_end_time = expand_timed_transportation_legs(
         transportation=transportation_name,
         start_time=start_time,
         legs=day_loop.legs,
         added_as_attraction=added_as_attraction )

      return expanded_end_time, timed_legs

from __future__ import annotations

from ....attractions.scheduling.attraction_operating_hours import fetch_configured_attraction_operating_hours_seconds
from .bulk_schedule_walk_order import representative_walk_node_id
from ...data_access.find_saved_itinerary_schedule_item_row import find_saved_itinerary_transportation_row
from ...data_access.itinerary import fetch_saved_itinerary
from ...data_access.itinerary_animal_record import ItineraryAnimalRecord
from ...data_access.itinerary_transportation import set_itinerary_transportation_bulk_transit_evaluated
from ...data_access.itinerary_transportation_record import ItineraryTransportationRecord
from ...data_access.schedule_itinerary_item import update_itinerary_animal_schedule
from ...data_access.schedule_itinerary_transportation import apply_itinerary_transportation_ride_segments
from .planned_transit_ride import PlannedTransitRide
from ...routing.transit_ride_endpoint import TransitRideEndpoint
from ...routing.transportation_boarding_station import station_for_transportation_legs
from ...routing.walk_travel_time import travel_time_minutes_from_length_px
from ...routing.walk_travel_time import travel_time_seconds_between_nodes
from .scheduled_animal_anchor import ScheduledAnimalAnchor
from ....shared.calendar_dates import DateValues
from ....shared.constants import TRANSPORTATION_RIDE_MAX_WALK_DURATION_MULTIPLIER
from ....shared.constants import TRANSPORTATION_WALK_SAVINGS_MAX_REMAINING_FRACTION
from ....shared.duration_values import duration_minutes_to_seconds
from ....shared.operating_hours import OperatingHours
from ....transportation.data_access.transportation_station import fetch_transportation_station_records
from ...transportation.legs_along_day_loop import legs_along_day_loop
from ...transportation.resolve_transportation_day_loop import fetch_transportation_day_loop
from ...transportation.transportation_day_loop import TransportationDayLoop
from ...transportation.transportation_route_leg_segment import TransportationRouteLegSegment
from ...transportation_item_key import TransportationScheduleItemKey
from ....types import Connection
from ....types import DateKey
from ....types import ScheduleTimeKey
from ....walk_graph.data_access.load_walk_graph import load_walk_graph
from ....walk_graph.domain.walk_graph import WalkGraph
from ....walk_graph.shortest_path import build_walk_graph_adjacency
from ....walk_graph.shortest_path import shortest_path_distance
from ....walk_graph.shortest_path import WalkGraphAdjacency
from ....walk_graph.snap_point import snap_point_to_nearest_walk_node
from ....walk_graph.walk_node_id_for_viewing_spot import walk_node_id_for_viewing_spot


def apply_transportation_transit_rides(
      conn: Connection,
      *,
      transit_rows: list[ ItineraryTransportationRecord ],
      scheduled_animals: list[ ItineraryAnimalRecord ],
      visit_date: DateKey | None,
      schedule_anchor_seconds: int,
      zoo_operating_hours: OperatingHours | None = None ) -> None:
   if not transit_rows or not scheduled_animals or visit_date is None:
      return

   walk_graph = load_walk_graph()
   adjacency = build_walk_graph_adjacency( walk_graph )
   entrance_node_id = str( walk_graph[ 'entrance_node_id' ] )
   saved_itinerary = fetch_saved_itinerary( conn )

   for transit_row in transit_rows:
      parsed_visit_date = DateValues.parse_date_value( visit_date )

      if parsed_visit_date is None:
         continue

      day_loop = fetch_transportation_day_loop(
         conn,
         transportation=transit_row.transportation,
         target_date=parsed_visit_date )

      if day_loop is None:
         continue

      station_walk_nodes = _station_walk_node_ids(
         conn,
         transportation=transit_row.transportation,
         day_loop=day_loop,
         walk_graph=walk_graph )

      if not station_walk_nodes:
         continue

      animal_anchors = _animal_anchors(
         walk_graph,
         entrance_node_id,
         scheduled_animals )

      if not animal_anchors:
         continue

      timeline_start_seconds, start_node_id = _transit_timeline_start(
         find_saved_itinerary_transportation_row(
            saved_itinerary,
            TransportationScheduleItemKey(
               name=transit_row.transportation,
               added_as_attraction=True ) ),
         schedule_anchor_seconds=schedule_anchor_seconds,
         station_walk_nodes=station_walk_nodes,
         entrance_node_id=entrance_node_id )

      rides_before_animals, return_ride = _plan_rides_for_anchors(
         day_loop=day_loop,
         station_walk_nodes=station_walk_nodes,
         start_node_id=start_node_id,
         entrance_node_id=entrance_node_id,
         animal_anchors=animal_anchors,
         walk_graph=walk_graph,
         adjacency=adjacency )

      operating_hours = (
         None
         if zoo_operating_hours is None
         else fetch_configured_attraction_operating_hours_seconds(
            conn,
            transit_row.transportation,
            visit_date=parsed_visit_date,
            zoo_operating_hours=zoo_operating_hours )
      )

      _apply_timeline(
         conn,
         transit_row=transit_row,
         day_loop=day_loop,
         animal_anchors=animal_anchors,
         rides_before_animals=rides_before_animals,
         return_ride=return_ride,
         timeline_start_seconds=timeline_start_seconds,
         start_node_id=start_node_id,
         walk_graph=walk_graph,
         adjacency=adjacency,
         station_walk_nodes=station_walk_nodes,
         operating_hours=operating_hours )

      cur = conn.cursor()

      try:
         set_itinerary_transportation_bulk_transit_evaluated(
            cur,
            transportation=transit_row.transportation,
            added_as_attraction=transit_row.added_as_attraction,
            bulk_transit_evaluated=True )
         conn.commit()
      finally:
         cur.close()


def _transit_timeline_start(
      companion_attraction_row: ItineraryTransportationRecord | None,
      *,
      schedule_anchor_seconds: int,
      station_walk_nodes: dict[ str, str ],
      entrance_node_id: str,
) -> tuple[ int, str ]:
   if companion_attraction_row is None:
      return schedule_anchor_seconds, entrance_node_id

   end_seconds = DateValues.time_value_in_seconds( companion_attraction_row.end_time )
   timeline_start_seconds = (
      schedule_anchor_seconds
      if end_seconds is None
      else max( schedule_anchor_seconds, end_seconds ) )

   if not companion_attraction_row.legs:
      return timeline_start_seconds, entrance_node_id

   alight_node_id = station_walk_nodes.get(
      station_for_transportation_legs(
         companion_attraction_row.legs,
         TransitRideEndpoint.OFFBOARDING ) )

   return timeline_start_seconds, alight_node_id or entrance_node_id


def _station_walk_node_ids(
      conn: Connection,
      *,
      transportation: str,
      day_loop: TransportationDayLoop,
      walk_graph: WalkGraph ) -> dict[ str, str ]:
   route_stations = {
      day_loop.main_station,
      *( leg.from_station for leg in day_loop.legs ),
      *( leg.to_station for leg in day_loop.legs ),
   }
   station_nodes: dict[ str, str ] = {}

   for station in fetch_transportation_station_records( conn, transportation ):
      if station.name not in route_stations:
         continue

      walk_node_id, _ = snap_point_to_nearest_walk_node(
         station.x_coord,
         station.y_coord,
         walk_graph )
      station_nodes[ station.name ] = walk_node_id

   return station_nodes


def _animal_anchors(
      walk_graph: WalkGraph,
      entrance_node_id: str,
      scheduled_animals: list[ ItineraryAnimalRecord ],
) -> list[ ScheduledAnimalAnchor ]:
   timed_animals: list[ tuple[ int, int, ItineraryAnimalRecord ] ] = []

   for animal in scheduled_animals:
      start_seconds = DateValues.time_value_in_seconds( animal.start_time )
      end_seconds = DateValues.time_value_in_seconds( animal.end_time )

      if start_seconds is None or end_seconds is None:
         continue

      timed_animals.append( ( start_seconds, end_seconds, animal ) )

   timed_animals.sort( key=lambda item: item[ 0 ] )
   anchors: list[ ScheduledAnimalAnchor ] = []

   for start_seconds, end_seconds, animal in timed_animals:
      walk_node_id = representative_walk_node_id(
         walk_graph,
         entrance_node_id,
         animal.species,
         animal.exhibit,
         animal.enclosure_name )

      if walk_node_id is None:
         walk_node_id = walk_node_id_for_viewing_spot(
            animal.species,
            animal.exhibit,
            animal.enclosure_name )

      if walk_node_id is None:
         continue

      anchors.append(
         ScheduledAnimalAnchor(
            animal=animal,
            walk_node_id=str( walk_node_id ),
            duration_seconds=max( 0, end_seconds - start_seconds ) ) )

   return anchors


def _plan_rides_for_anchors(
      *,
      day_loop: TransportationDayLoop,
      station_walk_nodes: dict[ str, str ],
      start_node_id: str,
      entrance_node_id: str,
      animal_anchors: list[ ScheduledAnimalAnchor ],
      walk_graph: WalkGraph,
      adjacency: WalkGraphAdjacency,
) -> tuple[ list[ PlannedTransitRide | None ], PlannedTransitRide | None ]:
   rides_before_animals: list[ PlannedTransitRide | None ] = []
   current_node_id = start_node_id

   for anchor in animal_anchors:
      rides_before_animals.append(
         _best_saving_ride(
            day_loop=day_loop,
            station_walk_nodes=station_walk_nodes,
            from_node_id=current_node_id,
            to_node_id=anchor.walk_node_id,
            walk_graph=walk_graph,
            adjacency=adjacency ) )
      current_node_id = anchor.walk_node_id

   return_ride = _best_saving_ride(
      day_loop=day_loop,
      station_walk_nodes=station_walk_nodes,
      from_node_id=current_node_id,
      to_node_id=entrance_node_id,
      walk_graph=walk_graph,
      adjacency=adjacency )

   return rides_before_animals, return_ride


def _best_saving_ride(
      *,
      day_loop: TransportationDayLoop,
      station_walk_nodes: dict[ str, str ],
      from_node_id: str,
      to_node_id: str,
      walk_graph: WalkGraph,
      adjacency: WalkGraphAdjacency,
) -> PlannedTransitRide | None:
   direct_walk_px = shortest_path_distance(
      walk_graph,
      from_node_id,
      to_node_id,
      adjacency=adjacency )

   if direct_walk_px is None or direct_walk_px <= 0:
      return None

   max_remaining_px = (
      TRANSPORTATION_WALK_SAVINGS_MAX_REMAINING_FRACTION * direct_walk_px )
   max_ride_minutes = (
      TRANSPORTATION_RIDE_MAX_WALK_DURATION_MULTIPLIER
      * travel_time_minutes_from_length_px( direct_walk_px ) )
   best_ride: PlannedTransitRide | None = None

   for board_station, board_node_id in station_walk_nodes.items():
      walk_to_board = shortest_path_distance(
         walk_graph,
         from_node_id,
         board_node_id,
         adjacency=adjacency )

      if walk_to_board is None:
         continue

      for alight_station, alight_node_id in station_walk_nodes.items():
         if board_station == alight_station:
            continue

         legs = legs_along_day_loop(
            day_loop,
            board_station,
            alight_station )

         if not legs:
            continue

         ride_duration_minutes = sum( leg.duration_minutes for leg in legs )

         if ride_duration_minutes > max_ride_minutes:
            continue

         walk_from_alight = shortest_path_distance(
            walk_graph,
            alight_node_id,
            to_node_id,
            adjacency=adjacency )

         if walk_from_alight is None:
            continue

         remaining_walk_px = walk_to_board + walk_from_alight

         if remaining_walk_px > max_remaining_px:
            continue

         if (
               best_ride is None
               or remaining_walk_px < best_ride.remaining_walk_px ):
            best_ride = PlannedTransitRide(
               from_station=board_station,
               to_station=alight_station,
               legs=list( legs ),
               remaining_walk_px=remaining_walk_px )

   return best_ride


def _walk_seconds_to_station(
      *,
      walk_graph: WalkGraph,
      adjacency: WalkGraphAdjacency,
      station_walk_nodes: dict[ str, str ],
      from_node_id: str,
      station_name: str ) -> int:
   board_node_id = station_walk_nodes.get( station_name )

   if board_node_id is None:
      return 0

   return travel_time_seconds_between_nodes(
      walk_graph,
      from_node_id,
      board_node_id,
      adjacency=adjacency )


def _ride_window_within_operating_hours(
      ride_start: int,
      ride_duration: int,
      operating_hours: OperatingHours | None,
) -> tuple[ int, int ] | None:
   if operating_hours is None:
      return ride_start, ride_start + ride_duration

   adjusted_start = max( ride_start, operating_hours.open_seconds )
   adjusted_end = adjusted_start + ride_duration

   if adjusted_end > operating_hours.close_seconds:
      return None

   return adjusted_start, adjusted_end


def _apply_timeline(
      conn: Connection,
      *,
      transit_row: ItineraryTransportationRecord,
      day_loop: TransportationDayLoop,
      animal_anchors: list[ ScheduledAnimalAnchor ],
      rides_before_animals: list[ PlannedTransitRide | None ],
      return_ride: PlannedTransitRide | None,
      timeline_start_seconds: int,
      start_node_id: str,
      walk_graph: WalkGraph,
      adjacency: WalkGraphAdjacency,
      station_walk_nodes: dict[ str, str ],
      operating_hours: OperatingHours | None ) -> None:
   segments: list[ tuple[ ScheduleTimeKey, list[ TransportationRouteLegSegment ] ] ] = []
   animal_updates: list[ tuple[ ItineraryAnimalRecord, ScheduleTimeKey, ScheduleTimeKey ] ] = []
   shift_seconds = 0
   cursor_seconds = timeline_start_seconds
   current_node_id = start_node_id

   for ride, anchor in zip( rides_before_animals, animal_anchors ):
      original_start = DateValues.time_value_in_seconds( anchor.animal.start_time )
      original_end = DateValues.time_value_in_seconds( anchor.animal.end_time )

      if original_start is None or original_end is None:
         continue

      animal_start = original_start + shift_seconds
      animal_end = original_end + shift_seconds

      if ride is not None:
         ride_duration = duration_minutes_to_seconds(
            sum( leg.duration_minutes for leg in ride.legs ) )
         proposed_ride_start = (
            cursor_seconds
            + _walk_seconds_to_station(
               walk_graph=walk_graph,
               adjacency=adjacency,
               station_walk_nodes=station_walk_nodes,
               from_node_id=current_node_id,
               station_name=ride.from_station ) )
         ride_window = _ride_window_within_operating_hours(
            proposed_ride_start,
            ride_duration,
            operating_hours )

         if ride_window is not None:
            ride_start, ride_end = ride_window

            if ride_end > animal_start:
               extra = ride_end - animal_start
               shift_seconds += extra
               animal_start += extra
               animal_end += extra

            segments.append(
               (
                  DateValues.schedule_time_key_from_seconds( ride_start ),
                  list( ride.legs ),
               ) )
            cursor_seconds = max( cursor_seconds, ride_end )
            current_node_id = (
               station_walk_nodes.get( ride.to_station )
               or current_node_id )

      animal_updates.append(
         (
            anchor.animal,
            DateValues.schedule_time_key_from_seconds( animal_start ),
            DateValues.schedule_time_key_from_seconds( animal_end ),
         ) )
      cursor_seconds = max( cursor_seconds, animal_end )
      current_node_id = anchor.walk_node_id

   if return_ride is not None:
      return_ride_duration = duration_minutes_to_seconds(
         sum( leg.duration_minutes for leg in return_ride.legs ) )
      proposed_return_start = (
         cursor_seconds
         + _walk_seconds_to_station(
            walk_graph=walk_graph,
            adjacency=adjacency,
            station_walk_nodes=station_walk_nodes,
            from_node_id=current_node_id,
            station_name=return_ride.from_station ) )
      return_window = _ride_window_within_operating_hours(
         proposed_return_start,
         return_ride_duration,
         operating_hours )

      if return_window is not None:
         return_start, _return_end = return_window
         segments.append(
            (
               DateValues.schedule_time_key_from_seconds( return_start ),
               list( return_ride.legs ),
            ) )

   if not segments:
      return

   cur = conn.cursor()

   try:
      for animal, start_time, end_time in animal_updates:
         update_itinerary_animal_schedule(
            cur,
            species=animal.species,
            exhibit=animal.exhibit,
            enclosure_name=animal.enclosure_name,
            start_time=start_time,
            end_time=end_time )

      apply_itinerary_transportation_ride_segments(
         cur,
         name=transit_row.transportation,
         added_as_attraction=transit_row.added_as_attraction,
         route=day_loop.route,
         segments=segments )
      conn.commit()
   finally:
      cur.close()

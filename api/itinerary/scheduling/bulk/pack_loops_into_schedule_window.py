from __future__ import annotations

from dataclasses import dataclass

from .loop_schedule_slot_assigner import LoopScheduleSlotAssigner
from .loop_schedule_unit import LoopScheduleUnit
from .loop_schedule_unit_builder import LoopScheduleUnitBuilder
from .loop_unit_travel_time_calculator import LoopUnitTravelTimeCalculator
from ...routing.partition_itinerary_schedule_windows import ItineraryScheduleWindow
from ....types import Connection
from ....walk_graph.domain.loop_side_cluster_id import LoopSideClusterId
from ....walk_graph.domain.master_route_loop import is_two_way_loop_traversal
from ....walk_graph.domain.walk_graph import WalkGraph
from ....walk_graph.shortest_path import build_walk_graph_adjacency
from ....walk_graph.shortest_path import shortest_path_distance
from ....walk_graph.shortest_path import shortest_path_distances
from ....walk_graph.shortest_path import WalkGraphAdjacency


@dataclass( frozen=True )
class PreparedLoopScheduleUnit:
   unit: LoopScheduleUnit
   occupied_seconds: int


def prepare_loop_schedule_units(
      conn: Connection,
      units: list[ LoopScheduleUnit ],
      *,
      walk_graph: WalkGraph ) -> list[ PreparedLoopScheduleUnit ] | None:
   prepared_units: list[ PreparedLoopScheduleUnit ] = []
   adjacency = build_walk_graph_adjacency( walk_graph )

   for unit in units:
      prepared_stops = LoopScheduleSlotAssigner.prepare_stops(
         conn,
         walk_graph,
         unit.stops,
         adjacency=adjacency )

      if prepared_stops is None:
         return None

      prepared_units.append(
         PreparedLoopScheduleUnit(
            unit=unit,
            occupied_seconds=LoopScheduleSlotAssigner.total_occupied_seconds( prepared_stops ) ) )

   return prepared_units


def pack_loops_into_schedule_window(
      walk_graph: WalkGraph,
      schedule_window: ItineraryScheduleWindow,
      *,
      prepared_units: list[ PreparedLoopScheduleUnit ],
      cursor_seconds: int,
      current_node_id: str,
      departure_side_cluster_id: str | None = None ) -> list[ PreparedLoopScheduleUnit ]:
   if not prepared_units:
      return []

   window_start_seconds = max(
      cursor_seconds,
      schedule_window.start_seconds )

   if window_start_seconds >= schedule_window.end_seconds:
      return []

   return _pack_loops_for_anchored_window(
      walk_graph,
      schedule_window,
      prepared_units=prepared_units,
      window_start_seconds=window_start_seconds,
      current_node_id=current_node_id,
      departure_side_cluster_id=departure_side_cluster_id )


def _pack_loops_for_anchored_window(
      walk_graph: WalkGraph,
      schedule_window: ItineraryScheduleWindow,
      *,
      prepared_units: list[ PreparedLoopScheduleUnit ],
      window_start_seconds: int,
      current_node_id: str,
      departure_side_cluster_id: str | None = None ) -> list[ PreparedLoopScheduleUnit ]:
   anchor_node_id = _anchor_walk_node_id( schedule_window )

   if anchor_node_id is None:
      return _pack_loops_for_open_window(
         walk_graph,
         schedule_window,
         prepared_units=prepared_units,
         window_start_seconds=window_start_seconds,
         current_node_id=current_node_id,
         departure_side_cluster_id=departure_side_cluster_id )

   best_sequence: list[ PreparedLoopScheduleUnit ] = []
   best_score: tuple[ float, float, str ] | None = None

   for terminal_unit in prepared_units:
      for oriented_terminal_unit in _prepared_unit_orientations( terminal_unit ):
         sequence = _pack_loops_with_terminal_unit(
            walk_graph,
            prepared_units,
            terminal_unit=oriented_terminal_unit,
            window_start_seconds=window_start_seconds,
            window_end_seconds=schedule_window.end_seconds,
            current_node_id=current_node_id,
            anchor_node_id=anchor_node_id,
            departure_side_cluster_id=departure_side_cluster_id )

      if not sequence:
         continue

      score = _anchored_sequence_score(
         walk_graph,
         sequence,
         window_end_seconds=schedule_window.end_seconds,
         window_start_seconds=window_start_seconds,
         current_node_id=current_node_id,
         anchor_node_id=anchor_node_id )

      if best_score is None or score < best_score:
         best_score = score
         best_sequence = sequence

   if best_sequence:
      return best_sequence

   return _pack_loops_for_open_window(
      walk_graph,
      schedule_window,
      prepared_units=prepared_units,
      window_start_seconds=window_start_seconds,
      current_node_id=current_node_id,
      departure_side_cluster_id=departure_side_cluster_id )


def pack_all_loops_before_deadline(
      walk_graph: WalkGraph,
      *,
      prepared_units: list[ PreparedLoopScheduleUnit ],
      window_start_seconds: int,
      deadline_seconds: int,
      current_node_id: str,
      departure_side_cluster_id: str | None = None ) -> list[ PreparedLoopScheduleUnit ] | None:
   if not prepared_units or window_start_seconds >= deadline_seconds:
      return None

   occupied_seconds = LoopUnitTravelTimeCalculator.packed_units_occupied_seconds(
      walk_graph,
      prepared_units,
      from_node_id=current_node_id )

   if window_start_seconds + occupied_seconds > deadline_seconds:
      return None

   packed_units = _pack_loops_for_open_window(
      walk_graph,
      ItineraryScheduleWindow(
         start_seconds=window_start_seconds,
         end_seconds=deadline_seconds ),
      prepared_units=prepared_units,
      window_start_seconds=window_start_seconds,
      current_node_id=current_node_id,
      departure_side_cluster_id=departure_side_cluster_id )

   if len( packed_units ) != len( prepared_units ):
      return None

   return packed_units


def _pack_loops_with_terminal_unit(
      walk_graph: WalkGraph,
      prepared_units: list[ PreparedLoopScheduleUnit ],
      *,
      terminal_unit: PreparedLoopScheduleUnit,
      window_start_seconds: int,
      window_end_seconds: int,
      current_node_id: str,
      anchor_node_id: str,
      departure_side_cluster_id: str | None = None ) -> list[ PreparedLoopScheduleUnit ]:
   terminal_start_seconds = window_end_seconds - terminal_unit.occupied_seconds

   if terminal_start_seconds < window_start_seconds:
      return []

   prefix_units = _greedy_prefix_units_before_terminal(
      walk_graph,
      [
         unit
         for unit in prepared_units
         if not _prepared_units_share_loop( unit, terminal_unit )
      ],
      window_start_seconds=window_start_seconds,
      terminal_start_seconds=terminal_start_seconds,
      current_node_id=current_node_id,
      terminal_side_cluster_id=terminal_unit.unit.side_cluster_id,
      departure_side_cluster_id=departure_side_cluster_id )

   occupied_seconds = LoopUnitTravelTimeCalculator.packed_units_occupied_seconds(
      walk_graph,
      [ *prefix_units, terminal_unit ],
      from_node_id=current_node_id )

   if window_start_seconds + occupied_seconds > window_end_seconds:
      return []

   return [ *prefix_units, terminal_unit ]


def _greedy_prefix_units_before_terminal(
      walk_graph: WalkGraph,
      candidate_units: list[ PreparedLoopScheduleUnit ],
      *,
      window_start_seconds: int,
      terminal_start_seconds: int,
      current_node_id: str,
      terminal_side_cluster_id: str | None,
      departure_side_cluster_id: str | None = None ) -> list[ PreparedLoopScheduleUnit ]:
   remaining_units = list( candidate_units )
   packed_units: list[ PreparedLoopScheduleUnit ] = []
   cursor_seconds = window_start_seconds
   walk_node_id = current_node_id
   previous_side_cluster_id = departure_side_cluster_id
   adjacency = build_walk_graph_adjacency( walk_graph )

   while remaining_units:
      available_seconds = terminal_start_seconds - cursor_seconds

      if available_seconds <= 0:
         break

      fitting_units = [
         unit
         for unit in remaining_units
         if (
               LoopUnitTravelTimeCalculator.approach_seconds_to_unit(
                  walk_graph,
                  walk_node_id,
                  unit.unit,
                  adjacency=adjacency )
               + unit.occupied_seconds ) <= available_seconds
      ]

      if not fitting_units:
         break

      prefer_side_cluster_loop_order = _should_prefer_side_cluster_loop_order(
         fitting_units,
         previous_side_cluster_id=previous_side_cluster_id )

      next_unit = min(
         fitting_units,
         key=lambda unit: _prefix_unit_sort_key(
            walk_graph,
            unit,
            from_node_id=walk_node_id,
            terminal_side_cluster_id=terminal_side_cluster_id,
            adjacency=adjacency,
            prefer_side_cluster_loop_order=prefer_side_cluster_loop_order ) )
      remaining_units.remove( next_unit )
      next_unit = _prepared_unit_with_best_approach_orientation(
         walk_graph,
         from_node_id=walk_node_id,
         prepared_unit=next_unit,
         adjacency=adjacency )
      packed_units.append( next_unit )
      cursor_seconds += (
         LoopUnitTravelTimeCalculator.approach_seconds_to_unit(
            walk_graph,
            walk_node_id,
            next_unit.unit,
            adjacency=adjacency )
         + next_unit.occupied_seconds )
      previous_side_cluster_id = next_unit.unit.side_cluster_id

      if next_unit.unit.exit_walk_node_id is not None:
         walk_node_id = next_unit.unit.exit_walk_node_id

   return packed_units


def _pack_loops_for_open_window(
      walk_graph: WalkGraph,
      schedule_window: ItineraryScheduleWindow,
      *,
      prepared_units: list[ PreparedLoopScheduleUnit ],
      window_start_seconds: int,
      current_node_id: str,
      departure_side_cluster_id: str | None = None ) -> list[ PreparedLoopScheduleUnit ]:
   remaining_units = list( prepared_units )
   packed_units: list[ PreparedLoopScheduleUnit ] = []
   cursor_seconds = window_start_seconds
   walk_node_id = current_node_id
   previous_side_cluster_id = departure_side_cluster_id
   adjacency = build_walk_graph_adjacency( walk_graph )
   preferred_side_cluster_sequence, prefer_soft_pin_loop_ids = (
      _choose_side_cluster_packing_order(
         schedule_window,
         prepared_units=prepared_units,
         walk_graph=walk_graph,
         current_node_id=current_node_id,
         cursor_seconds=window_start_seconds ) )

   while remaining_units:
      available_seconds = schedule_window.end_seconds - cursor_seconds

      if available_seconds <= 0:
         break

      fitting_units = [
         unit
         for unit in remaining_units
         if (
               LoopUnitTravelTimeCalculator.approach_seconds_to_unit(
                  walk_graph,
                  walk_node_id,
                  unit.unit,
                  adjacency=adjacency )
               + unit.occupied_seconds ) <= available_seconds
      ]

      if not fitting_units:
         break

      prefer_side_cluster_loop_order = _should_prefer_side_cluster_loop_order(
         fitting_units,
         previous_side_cluster_id=previous_side_cluster_id )

      next_unit = min(
         fitting_units,
         key=lambda unit: _open_window_unit_sort_key(
            walk_graph,
            unit,
            from_node_id=walk_node_id,
            previous_side_cluster_id=previous_side_cluster_id,
            adjacency=adjacency,
            prefer_side_cluster_loop_order=prefer_side_cluster_loop_order,
            remaining_units=remaining_units,
            preferred_side_cluster_sequence=preferred_side_cluster_sequence,
            prefer_soft_pin_loop_ids=prefer_soft_pin_loop_ids ) )
      remaining_units.remove( next_unit )
      next_unit = _prepared_unit_with_best_approach_orientation(
         walk_graph,
         from_node_id=walk_node_id,
         prepared_unit=next_unit,
         adjacency=adjacency )
      packed_units.append( next_unit )
      cursor_seconds += (
         LoopUnitTravelTimeCalculator.approach_seconds_to_unit(
            walk_graph,
            walk_node_id,
            next_unit.unit,
            adjacency=adjacency )
         + next_unit.occupied_seconds )
      previous_side_cluster_id = next_unit.unit.side_cluster_id

      if next_unit.unit.exit_walk_node_id is not None:
         walk_node_id = next_unit.unit.exit_walk_node_id

   return packed_units


def _anchored_sequence_score(
      walk_graph: WalkGraph,
      sequence: list[ PreparedLoopScheduleUnit ],
      *,
      window_end_seconds: int,
      window_start_seconds: int,
      current_node_id: str,
      anchor_node_id: str ) -> tuple[ float, float, str ]:
   terminal_unit = sequence[ -1 ]
   occupied_seconds = LoopUnitTravelTimeCalculator.packed_units_occupied_seconds(
      walk_graph,
      sequence,
      from_node_id=current_node_id )
   dead_time_seconds = float(
      window_end_seconds - window_start_seconds - occupied_seconds )
   terminal_exit_node_id = terminal_unit.unit.exit_walk_node_id or ''
   event_travel_distance = _walk_distance_px(
      walk_graph,
      terminal_exit_node_id,
      anchor_node_id )

   return (
      event_travel_distance,
      dead_time_seconds,
      terminal_unit.unit.loop_id or '',
   )


def _prefix_unit_sort_key(
      walk_graph: WalkGraph,
      prepared_unit: PreparedLoopScheduleUnit,
      *,
      from_node_id: str,
      terminal_side_cluster_id: str | None,
      adjacency: WalkGraphAdjacency,
      prefer_side_cluster_loop_order: bool ) -> tuple[ float, float, str ]:
   return _prepared_unit_sort_key(
      walk_graph,
      prepared_unit,
      from_node_id=from_node_id,
      adjacency=adjacency,
      prefer_side_cluster_loop_order=prefer_side_cluster_loop_order,
      reference_side_cluster_id=terminal_side_cluster_id )


def _open_window_unit_sort_key(
      walk_graph: WalkGraph,
      prepared_unit: PreparedLoopScheduleUnit,
      *,
      from_node_id: str,
      previous_side_cluster_id: str | None,
      adjacency: WalkGraphAdjacency,
      prefer_side_cluster_loop_order: bool,
      remaining_units: list[ PreparedLoopScheduleUnit ],
      preferred_side_cluster_sequence: list[ LoopSideClusterId ] | None = None,
      prefer_soft_pin_loop_ids: list[ str ] | None = None,
   ) -> tuple[ float, float, float, float, str ]:
   remaining_cluster_ids = [
      unit.unit.side_cluster_id
      for unit in remaining_units
      if unit.unit.side_cluster_id is not None
   ]
   next_cluster_id = next(
      (
         cluster_id
         for cluster_id in ( preferred_side_cluster_sequence or [] )
         if cluster_id in remaining_cluster_ids
      ),
      None )
   corridor_rank = int(
      next_cluster_id is not None
      and prepared_unit.unit.side_cluster_id != next_cluster_id )
   pin_rank = int(
      bool( prefer_soft_pin_loop_ids )
      and prepared_unit.unit.loop_id not in prefer_soft_pin_loop_ids )
   distance_rank, cluster_rank, loop_id = _prepared_unit_sort_key(
      walk_graph,
      prepared_unit,
      from_node_id=from_node_id,
      adjacency=adjacency,
      prefer_side_cluster_loop_order=prefer_side_cluster_loop_order,
      reference_side_cluster_id=previous_side_cluster_id )

   return (
      float( corridor_rank ),
      float( pin_rank ),
      distance_rank,
      cluster_rank,
      loop_id )


def _prepared_unit_sort_key(
      walk_graph: WalkGraph,
      prepared_unit: PreparedLoopScheduleUnit,
      *,
      from_node_id: str,
      adjacency: WalkGraphAdjacency,
      prefer_side_cluster_loop_order: bool,
      reference_side_cluster_id: str | None ) -> tuple[ float, float, str ]:
   travel_distance = _travel_distance_to_unit_entry(
      walk_graph,
      from_node_id=from_node_id,
      prepared_unit=prepared_unit,
      adjacency=adjacency )
   loop_index_in_side_cluster = prepared_unit.unit.loop_index_in_side_cluster

   if prefer_side_cluster_loop_order and loop_index_in_side_cluster is not None:
      return (
         float( -loop_index_in_side_cluster ),
         travel_distance,
         prepared_unit.unit.loop_id or '',
      )

   same_side_cluster = int(
      _shares_side_cluster(
         prepared_unit.unit.side_cluster_id,
         reference_side_cluster_id ) )

   return (
      travel_distance,
      float( -same_side_cluster ),
      prepared_unit.unit.loop_id or '',
   )


def _soft_pin_loop_ids_in_units(
      schedule_window: ItineraryScheduleWindow,
      prepared_units: list[ PreparedLoopScheduleUnit ],
   ) -> list[ str ]:
   unit_loop_ids = [
      prepared_unit.unit.loop_id
      for prepared_unit in prepared_units
      if prepared_unit.unit.loop_id is not None
   ]
   loop_ids: list[ str ] = []

   for soft_pin in schedule_window.attraction_hours_soft_pins:
      if (
            soft_pin.loop_id in unit_loop_ids
            and soft_pin.loop_id not in loop_ids ):
         loop_ids.append( soft_pin.loop_id )

   return loop_ids


def _choose_side_cluster_packing_order(
      schedule_window: ItineraryScheduleWindow,
      *,
      prepared_units: list[ PreparedLoopScheduleUnit ],
      walk_graph: WalkGraph,
      current_node_id: str,
      cursor_seconds: int,
   ) -> tuple[ list[ LoopSideClusterId ] | None, list[ str ] | None ]:
   """Prefer the soft-pin corridor later when hours allow; otherwise front-load it."""
   soft_pin_loop_ids = _soft_pin_loop_ids_in_units(
      schedule_window,
      prepared_units )

   if not soft_pin_loop_ids:
      return None, None

   soft_cluster_id = next(
      (
         LoopSideClusterId( prepared_unit.unit.side_cluster_id )
         for prepared_unit in prepared_units
         if (
               prepared_unit.unit.loop_id in soft_pin_loop_ids
               and prepared_unit.unit.side_cluster_id is not None )
      ),
      None )

   if soft_cluster_id is None:
      return None, None

   present_cluster_ids = [
      cluster_id
      for cluster_id in LoopSideClusterId
      if any(
         prepared_unit.unit.side_cluster_id == cluster_id
         for prepared_unit in prepared_units )
   ]
   other_cluster_ids = [
      cluster_id
      for cluster_id in present_cluster_ids
      if cluster_id != soft_cluster_id
   ]
   pin_later_order = [ *other_cluster_ids, soft_cluster_id ]
   pin_first_order = [ soft_cluster_id, *other_cluster_ids ]

   if _soft_pins_fit_before_close(
         schedule_window,
         prepared_units=prepared_units,
         cluster_order=pin_later_order,
         soft_pin_loop_ids=soft_pin_loop_ids,
         soft_pin_late_in_own_cluster=True,
         walk_graph=walk_graph,
         current_node_id=current_node_id,
         cursor_seconds=cursor_seconds ):
      return pin_later_order, None

   return pin_first_order, soft_pin_loop_ids


def _soft_pins_fit_before_close(
      schedule_window: ItineraryScheduleWindow,
      *,
      prepared_units: list[ PreparedLoopScheduleUnit ],
      cluster_order: list[ LoopSideClusterId ],
      soft_pin_loop_ids: list[ str ],
      soft_pin_late_in_own_cluster: bool,
      walk_graph: WalkGraph,
      current_node_id: str,
      cursor_seconds: int,
   ) -> bool:
   for prepared_unit in prepared_units:
      if prepared_unit.unit.loop_id not in soft_pin_loop_ids:
         continue

      matching_pins = [
         soft_pin
         for soft_pin in schedule_window.attraction_hours_soft_pins
         if soft_pin.loop_id == prepared_unit.unit.loop_id
      ]
      soft_cluster_id = prepared_unit.unit.side_cluster_id

      if not matching_pins or soft_cluster_id not in cluster_order:
         continue

      preceding_cluster_ids = cluster_order[ : cluster_order.index( soft_cluster_id ) ]
      units_before_soft_end = [
         candidate
         for candidate in prepared_units
         if candidate.unit.side_cluster_id in preceding_cluster_ids
         or (
               soft_pin_late_in_own_cluster
               and candidate.unit.side_cluster_id == soft_cluster_id
               and candidate.unit.loop_id not in soft_pin_loop_ids )
      ] + [ prepared_unit ]

      if (
            cursor_seconds
            + LoopUnitTravelTimeCalculator.packed_units_occupied_seconds(
               walk_graph,
               units_before_soft_end,
               from_node_id=current_node_id )
            > min( matching_pins[ 0 ].close_seconds, schedule_window.end_seconds ) ):
         return False

   return True


def _should_prefer_side_cluster_loop_order(
      fitting_units: list[ PreparedLoopScheduleUnit ],
      *,
      previous_side_cluster_id: str | None ) -> bool:
   if previous_side_cluster_id is None:
      return False

   side_cluster_ids = {
      prepared_unit.unit.side_cluster_id
      for prepared_unit in fitting_units
      if prepared_unit.unit.side_cluster_id is not None
   }

   if len( side_cluster_ids ) != 1:
      return False

   side_cluster_id = next( iter( side_cluster_ids ) )

   if (
         previous_side_cluster_id is not None
         and previous_side_cluster_id != side_cluster_id ):
      return False

   return True


def _travel_distance_to_unit_entry(
      walk_graph: WalkGraph,
      *,
      from_node_id: str,
      prepared_unit: PreparedLoopScheduleUnit,
      adjacency: WalkGraphAdjacency ) -> float:
   unit = prepared_unit.unit
   entry_walk_node_id = unit.entry_walk_node_id

   if entry_walk_node_id is None:
      return float( 'inf' )

   forward_distance = _walk_distance_px(
      walk_graph,
      from_node_id,
      entry_walk_node_id,
      adjacency=adjacency )

   if not is_two_way_loop_traversal( unit.traversal ):
      return forward_distance

   exit_walk_node_id = unit.exit_walk_node_id

   if exit_walk_node_id is None:
      return forward_distance

   reverse_distance = _walk_distance_px(
      walk_graph,
      from_node_id,
      exit_walk_node_id,
      adjacency=adjacency )

   return min( forward_distance, reverse_distance )


def remove_matching_prepared_loop_unit(
      prepared_units: list[ PreparedLoopScheduleUnit ],
      prepared_unit: PreparedLoopScheduleUnit ) -> None:
   for index, candidate in enumerate( prepared_units ):
      if _prepared_units_share_loop( candidate, prepared_unit ):
         prepared_units.pop( index )
         return

   prepared_units.remove( prepared_unit )


def _prepared_units_share_loop(
      left_unit: PreparedLoopScheduleUnit,
      right_unit: PreparedLoopScheduleUnit ) -> bool:
   left_loop_id = left_unit.unit.loop_id
   right_loop_id = right_unit.unit.loop_id

   if left_loop_id is None or right_loop_id is None:
      return left_unit is right_unit

   return left_loop_id == right_loop_id


def _prepared_unit_orientations(
      prepared_unit: PreparedLoopScheduleUnit ) -> list[ PreparedLoopScheduleUnit ]:
   return [
      _prepared_unit_with_loop_schedule_unit(
         prepared_unit,
         loop_unit )
      for loop_unit in LoopScheduleUnitBuilder.orientations( prepared_unit.unit )
   ]


def _prepared_unit_with_best_approach_orientation(
      walk_graph: WalkGraph,
      *,
      from_node_id: str,
      prepared_unit: PreparedLoopScheduleUnit,
      adjacency: WalkGraphAdjacency ) -> PreparedLoopScheduleUnit:
   unit = prepared_unit.unit

   if not is_two_way_loop_traversal( unit.traversal ):
      return prepared_unit

   forward_distance = _walk_distance_px(
      walk_graph,
      from_node_id,
      unit.entry_walk_node_id or '',
      adjacency=adjacency )
   reverse_distance = _walk_distance_px(
      walk_graph,
      from_node_id,
      unit.exit_walk_node_id or '',
      adjacency=adjacency )

   if reverse_distance < forward_distance:
      return _prepared_unit_with_loop_schedule_unit(
         prepared_unit,
         LoopScheduleUnitBuilder.reversed( unit ) )

   return prepared_unit


def _prepared_unit_with_loop_schedule_unit(
      prepared_unit: PreparedLoopScheduleUnit,
      loop_unit: LoopScheduleUnit ) -> PreparedLoopScheduleUnit:
   return PreparedLoopScheduleUnit(
      unit=loop_unit,
      occupied_seconds=prepared_unit.occupied_seconds )


def _walk_distance_px(
      walk_graph: WalkGraph,
      from_node_id: str,
      to_node_id: str,
      *,
      adjacency: WalkGraphAdjacency | None = None ) -> float:
   if not from_node_id or not to_node_id:
      return float( 'inf' )

   if from_node_id == to_node_id:
      return 0.0

   if adjacency is None:
      distance_px = shortest_path_distance(
         walk_graph,
         from_node_id,
         to_node_id )
   else:
      distance_px = shortest_path_distances(
         walk_graph,
         from_node_id,
         adjacency=adjacency ).get( to_node_id )

   if distance_px is None:
      return float( 'inf' )

   return distance_px


def _shares_side_cluster(
      left_side_cluster_id: str | None,
      right_side_cluster_id: str | None ) -> bool:
   if left_side_cluster_id is None or right_side_cluster_id is None:
      return False

   return left_side_cluster_id == right_side_cluster_id


def _anchor_walk_node_id(
      schedule_window: ItineraryScheduleWindow ) -> str | None:
   anchor_stop = schedule_window.anchor_stop

   if anchor_stop is None or not anchor_stop.walk_node_ids:
      return None

   return anchor_stop.walk_node_ids[ 0 ]

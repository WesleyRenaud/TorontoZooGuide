from __future__ import annotations

from dataclasses import dataclass

from ...data_access.itinerary_animal_record import ItineraryAnimalRecord
from ...data_access.itinerary_default_duration import fetch_enclosure_viewing_default_duration_seconds
from .loop_schedule_unit import LoopScheduleUnit
from ...routing.partition_itinerary_schedule_windows import ItineraryScheduleWindow
from ....types import Connection
from ....walk_graph.domain.walk_graph import WalkGraph
from ....walk_graph.shortest_path import build_walk_graph_adjacency
from ....walk_graph.shortest_path import shortest_path_distance
from ....walk_graph.shortest_path import shortest_path_distances
from ....walk_graph.shortest_path import WalkGraphAdjacency


@dataclass( frozen=True )
class PreparedLoopScheduleUnit:
   unit: LoopScheduleUnit
   duration_seconds: int


def prepare_loop_schedule_units(
      conn: Connection,
      units: list[ LoopScheduleUnit ] ) -> list[ PreparedLoopScheduleUnit ] | None:
   prepared_units: list[ PreparedLoopScheduleUnit ] = []

   for unit in units:
      duration_seconds = _total_viewing_duration_seconds( conn, unit.animals )

      if duration_seconds is None:
         return None

      prepared_units.append(
         PreparedLoopScheduleUnit(
            unit=unit,
            duration_seconds=duration_seconds ) )

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
      sequence = _pack_loops_with_terminal_unit(
         walk_graph,
         prepared_units,
         terminal_unit=terminal_unit,
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
   terminal_start_seconds = window_end_seconds - terminal_unit.duration_seconds

   if terminal_start_seconds < window_start_seconds:
      return []

   prefix_units = _greedy_prefix_units_before_terminal(
      walk_graph,
      [
         unit
         for unit in prepared_units
         if unit is not terminal_unit
      ],
      window_start_seconds=window_start_seconds,
      terminal_start_seconds=terminal_start_seconds,
      current_node_id=current_node_id,
      terminal_side_cluster_id=terminal_unit.unit.side_cluster_id,
      departure_side_cluster_id=departure_side_cluster_id )

   total_duration_seconds = sum(
      unit.duration_seconds
      for unit in prefix_units ) + terminal_unit.duration_seconds

   if window_start_seconds + total_duration_seconds > window_end_seconds:
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
         if unit.duration_seconds <= available_seconds
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
      packed_units.append( next_unit )
      cursor_seconds += next_unit.duration_seconds
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

   while remaining_units:
      available_seconds = schedule_window.end_seconds - cursor_seconds

      if available_seconds <= 0:
         break

      fitting_units = [
         unit
         for unit in remaining_units
         if unit.duration_seconds <= available_seconds
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
            prefer_side_cluster_loop_order=prefer_side_cluster_loop_order ) )
      remaining_units.remove( next_unit )
      packed_units.append( next_unit )
      cursor_seconds += next_unit.duration_seconds
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
      anchor_node_id: str ) -> tuple[ float, float, str ]:
   terminal_unit = sequence[ -1 ]
   total_duration_seconds = sum(
      unit.duration_seconds
      for unit in sequence )
   dead_time_seconds = float(
      window_end_seconds - window_start_seconds - total_duration_seconds )
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
      prefer_side_cluster_loop_order: bool ) -> tuple[ float, ... ]:
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
      prefer_side_cluster_loop_order: bool ) -> tuple[ float, ... ]:
   return _prepared_unit_sort_key(
      walk_graph,
      prepared_unit,
      from_node_id=from_node_id,
      adjacency=adjacency,
      prefer_side_cluster_loop_order=prefer_side_cluster_loop_order,
      reference_side_cluster_id=previous_side_cluster_id )


def _prepared_unit_sort_key(
      walk_graph: WalkGraph,
      prepared_unit: PreparedLoopScheduleUnit,
      *,
      from_node_id: str,
      adjacency: WalkGraphAdjacency,
      prefer_side_cluster_loop_order: bool,
      reference_side_cluster_id: str | None ) -> tuple[ float, ... ]:
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
   entry_walk_node_id = prepared_unit.unit.entry_walk_node_id

   if entry_walk_node_id is None:
      return float( 'inf' )

   return _walk_distance_px(
      walk_graph,
      from_node_id,
      entry_walk_node_id,
      adjacency=adjacency )


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


def _total_viewing_duration_seconds(
      conn: Connection,
      animals: tuple[ ItineraryAnimalRecord, ... ] ) -> int | None:
   total_duration_seconds = 0

   for animal_row in animals:
      duration_seconds = fetch_enclosure_viewing_default_duration_seconds(
         conn,
         animal_row.species,
         animal_row.exhibit,
         animal_row.enclosure_name )

      if duration_seconds is None:
         return None

      total_duration_seconds += duration_seconds

   return total_duration_seconds

from __future__ import annotations

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.routing.attraction_hours_soft_pin import AttractionHoursSoftPin
from api.itinerary.routing.partition_itinerary_schedule_windows import ItineraryScheduleWindow
from api.itinerary.scheduling.bulk import attraction_hours_soft_pin as soft_pin_module
from api.itinerary.scheduling.bulk import schedule_animals_by_master_route_loop as schedule_module
from api.itinerary.scheduling.bulk import schedule_loop_unit_with_attraction_hours as hours_module
from api.itinerary.scheduling.bulk.loop_schedule_unit import LoopScheduleUnit
from api.itinerary.scheduling.bulk.pack_loops_into_schedule_window import PreparedLoopScheduleUnit
from api.shared.operating_hours import OperatingHours


def _loop_unit(
      loop_id: str | None,
      stops: list,
   ) -> LoopScheduleUnit:
   return LoopScheduleUnit(
      loop_id=loop_id,
      stops=stops,
      entry_walk_node_id=None,
      exit_walk_node_id=None,
      side_cluster_id=None,
      loop_index_in_side_cluster=None,
      traversal=None )


def test_resolve_attraction_hours_soft_pins_rejects_invalid_visit_date() -> None:
   assert soft_pin_module.resolve_attraction_hours_soft_pins(
      object(),
      attractions=[],
      loop_units=[],
      visit_date=None,
      zoo_operating_hours=OperatingHours(
         open_seconds=9 * 3600,
         close_seconds=19 * 3600 ) ) == []


def test_attach_attraction_hours_soft_pins_noop_without_pins() -> None:
   windows = [
      ItineraryScheduleWindow(
         start_seconds=9 * 3600,
         end_seconds=12 * 3600 ),
   ]

   assert soft_pin_module.attach_attraction_hours_soft_pins_to_schedule_windows(
      windows,
      [] ) is windows


def test_attach_attraction_hours_soft_pins_filters_by_window_overlap() -> None:
   soft_pin = AttractionHoursSoftPin(
      loop_id='zoomobile',
      viewing_spot_index=0,
      attraction_name='Zoomobile',
      open_seconds=10 * 3600,
      close_seconds=18 * 3600 )
   morning = ItineraryScheduleWindow(
      start_seconds=9 * 3600,
      end_seconds=10 * 3600 )
   afternoon = ItineraryScheduleWindow(
      start_seconds=11 * 3600,
      end_seconds=15 * 3600 )

   attached = soft_pin_module.attach_attraction_hours_soft_pins_to_schedule_windows(
      [ morning, afternoon ],
      [ soft_pin ] )

   assert attached[ 0 ].attraction_hours_soft_pins == []
   assert attached[ 1 ].attraction_hours_soft_pins == [ soft_pin ]


def test_loop_id_by_attraction_name_skips_null_loop_and_animal_stops() -> None:
   animal = ItineraryAnimalRecord(
      species='Capybara',
      exhibit='Americas Outdoor Mayan Temple Ruins' )
   attraction = ItineraryAttractionRecord(
      attraction='Zoomobile',
      old_likelihood=None,
      new_likelihood=100 )

   loop_ids = soft_pin_module._loop_id_by_attraction_name(
      [
         _loop_unit( None, [ attraction ] ),
         _loop_unit( 'zoomobile', [ animal, attraction ] ),
      ] )

   assert loop_ids == { 'Zoomobile': 'zoomobile' }


def test_stops_before_attraction_hours_soft_pin_skips_unknown_indexes() -> None:
   soft_pin = AttractionHoursSoftPin(
      loop_id='unknown-loop',
      viewing_spot_index=2,
      attraction_name='Zoomobile',
      open_seconds=10 * 3600,
      close_seconds=18 * 3600 )
   attraction = ItineraryAttractionRecord(
      attraction='Zoomobile',
      old_likelihood=None,
      new_likelihood=100 )

   assert soft_pin_module.stops_before_attraction_hours_soft_pin(
      [ attraction ],
      loop_id='unknown-loop',
      soft_pin=soft_pin ) == []


def test_wait_filler_pack_end_reserves_inactive_soft_pins_without_hard_pin() -> None:
   active = AttractionHoursSoftPin(
      loop_id='face-painting',
      viewing_spot_index=0,
      attraction_name='Face Painting',
      open_seconds=11 * 3600,
      close_seconds=16 * 3600 )
   zoomobile = AttractionHoursSoftPin(
      loop_id='zoomobile',
      viewing_spot_index=0,
      attraction_name='Zoomobile',
      open_seconds=10 * 3600,
      close_seconds=18 * 3600 )
   schedule_window = ItineraryScheduleWindow(
      start_seconds=9 * 3600,
      end_seconds=17 * 3600,
      attraction_hours_soft_pins=[ active, zoomobile ] )
   remaining_units = [
      PreparedLoopScheduleUnit(
         unit=_loop_unit( 'face-painting', [] ),
         occupied_seconds=20 * 60 ),
      PreparedLoopScheduleUnit(
         unit=_loop_unit( 'zoomobile', [] ),
         occupied_seconds=30 * 60 ),
   ]

   wait_pack_end, planned_active_start = schedule_module._wait_filler_pack_end_seconds(
      schedule_window,
      remaining_units=remaining_units,
      active_soft_pin_loop_ids={ 'face-painting' },
      hard_pinned_loop_ids=set(),
      active_open_seconds=11 * 3600,
      hard_pin_deadline_seconds=None,
      cursor_seconds=9 * 3600 + 15 * 60 )

   assert planned_active_start == 11 * 3600
   assert wait_pack_end == 11 * 3600 - 30 * 60


def test_wait_filler_pack_end_cascades_against_hard_pin_deadline() -> None:
   active = AttractionHoursSoftPin(
      loop_id='face-painting',
      viewing_spot_index=0,
      attraction_name='Face Painting',
      open_seconds=11 * 3600,
      close_seconds=16 * 3600 )
   carousel = AttractionHoursSoftPin(
      loop_id='carousel',
      viewing_spot_index=0,
      attraction_name='Conservation Carousel',
      open_seconds=9 * 3600 + 30 * 60,
      close_seconds=18 * 3600 )
   schedule_window = ItineraryScheduleWindow(
      start_seconds=9 * 3600,
      end_seconds=17 * 3600,
      attraction_hours_soft_pins=[ active, carousel ] )
   remaining_units = [
      PreparedLoopScheduleUnit(
         unit=_loop_unit( 'face-painting', [] ),
         occupied_seconds=20 * 60 ),
      PreparedLoopScheduleUnit(
         unit=_loop_unit( 'carousel', [] ),
         occupied_seconds=15 * 60 ),
   ]

   wait_pack_end, planned_active_start = schedule_module._wait_filler_pack_end_seconds(
      schedule_window,
      remaining_units=remaining_units,
      active_soft_pin_loop_ids={ 'face-painting' },
      hard_pinned_loop_ids=set(),
      active_open_seconds=11 * 3600,
      hard_pin_deadline_seconds=12 * 3600,
      cursor_seconds=9 * 3600 + 15 * 60 )

   assert planned_active_start == 12 * 3600 - 20 * 60
   assert wait_pack_end == planned_active_start - 15 * 60


def test_drain_cascaded_inactive_soft_pins_noop_without_active_open() -> None:
   schedule_window = ItineraryScheduleWindow(
      start_seconds=9 * 3600,
      end_seconds=17 * 3600,
      attraction_hours_soft_pins=[] )

   assert schedule_module._drain_cascaded_inactive_soft_pin_loop_units(
      object(),
      [],
      schedule_window,
      active_soft_pin_loop_ids=set(),
      hard_pinned_loop_ids=set(),
      pinned_earliest_start_cache={},
      blockers=[],
      cursor_seconds=9 * 3600,
      current_node_id='entrance',
      walk_graph=object(),
      cascade_end_seconds=11 * 3600 ) == ( 9 * 3600, 'entrance' )


def test_drain_cascaded_inactive_soft_pins_skips_missing_and_unready_units() -> None:
   active = AttractionHoursSoftPin(
      loop_id='face-painting',
      viewing_spot_index=0,
      attraction_name='Face Painting',
      open_seconds=11 * 3600,
      close_seconds=16 * 3600 )
   carousel = AttractionHoursSoftPin(
      loop_id='carousel',
      viewing_spot_index=0,
      attraction_name='Conservation Carousel',
      open_seconds=9 * 3600 + 30 * 60,
      close_seconds=18 * 3600 )
   zoomobile = AttractionHoursSoftPin(
      loop_id='zoomobile',
      viewing_spot_index=0,
      attraction_name='Zoomobile',
      open_seconds=10 * 3600,
      close_seconds=18 * 3600 )
   schedule_window = ItineraryScheduleWindow(
      start_seconds=9 * 3600,
      end_seconds=17 * 3600,
      attraction_hours_soft_pins=[ active, carousel, zoomobile ] )
   unready = PreparedLoopScheduleUnit(
      unit=_loop_unit( 'carousel', [] ),
      occupied_seconds=15 * 60 )

   assert schedule_module._drain_cascaded_inactive_soft_pin_loop_units(
      object(),
      [ unready ],
      schedule_window,
      active_soft_pin_loop_ids={ 'face-painting' },
      hard_pinned_loop_ids=set(),
      pinned_earliest_start_cache={ id( unready ): 10 * 3600 },
      blockers=[],
      cursor_seconds=9 * 3600,
      current_node_id='entrance',
      walk_graph=object(),
      cascade_end_seconds=11 * 3600 ) == ( 9 * 3600, 'entrance' )


def test_schedule_prepared_loop_unit_with_attraction_hours_early_exits() -> None:
   attraction = ItineraryAttractionRecord(
      attraction='Zoomobile',
      old_likelihood=None,
      new_likelihood=100 )
   prepared = PreparedLoopScheduleUnit(
      unit=_loop_unit( None, [ attraction ] ),
      occupied_seconds=30 * 60 )
   soft_pin = AttractionHoursSoftPin(
      loop_id='zoomobile',
      viewing_spot_index=0,
      attraction_name='Zoomobile',
      open_seconds=10 * 3600,
      close_seconds=18 * 3600 )

   stops, cursor = hours_module.schedule_prepared_loop_unit_with_attraction_hours(
      object(),
      prepared,
      [ soft_pin ],
      blockers=[],
      window_start_seconds=9 * 3600,
      window_end_seconds=17 * 3600,
      cursor_seconds=9 * 3600 )
   assert stops == [ attraction ]
   assert cursor == 9 * 3600

   prepared_with_loop = PreparedLoopScheduleUnit(
      unit=_loop_unit( 'other-loop', [ attraction ] ),
      occupied_seconds=30 * 60 )
   stops, cursor = hours_module.schedule_prepared_loop_unit_with_attraction_hours(
      object(),
      prepared_with_loop,
      [ soft_pin ],
      blockers=[],
      window_start_seconds=9 * 3600,
      window_end_seconds=17 * 3600,
      cursor_seconds=9 * 3600 )
   assert stops == [ attraction ]
   assert cursor == 9 * 3600

   stops, cursor = hours_module.schedule_prepared_loop_unit_with_attraction_hours(
      object(),
      prepared_with_loop,
      [],
      blockers=[],
      window_start_seconds=9 * 3600,
      window_end_seconds=17 * 3600,
      cursor_seconds=9 * 3600 )
   assert stops == [ attraction ]
   assert cursor == 9 * 3600


def test_attraction_hours_loop_earliest_start_seconds_early_exits() -> None:
   attraction = ItineraryAttractionRecord(
      attraction='Zoomobile',
      old_likelihood=None,
      new_likelihood=100 )
   soft_pin = AttractionHoursSoftPin(
      loop_id='zoomobile',
      viewing_spot_index=0,
      attraction_name='Zoomobile',
      open_seconds=10 * 3600,
      close_seconds=18 * 3600 )

   assert hours_module.attraction_hours_loop_earliest_start_seconds(
      object(),
      PreparedLoopScheduleUnit(
         unit=_loop_unit( None, [ attraction ] ),
         occupied_seconds=30 * 60 ),
      [ soft_pin ] ) is None

   assert hours_module.attraction_hours_loop_earliest_start_seconds(
      object(),
      PreparedLoopScheduleUnit(
         unit=_loop_unit( 'other-loop', [ attraction ] ),
         occupied_seconds=30 * 60 ),
      [ soft_pin ] ) is None

   assert hours_module.attraction_hours_loop_earliest_start_seconds(
      object(),
      PreparedLoopScheduleUnit(
         unit=_loop_unit( 'zoomobile', [ attraction ] ),
         occupied_seconds=30 * 60 ),
      [ soft_pin ] ) == 10 * 3600


def test_resolve_skips_attraction_not_on_any_loop() -> None:
   soft_pins = soft_pin_module.resolve_attraction_hours_soft_pins(
      object(),
      attractions=[
         ItineraryAttractionRecord(
            attraction='Zoomobile',
            old_likelihood=None,
            new_likelihood=100 ),
      ],
      loop_units=[],
      visit_date='2026-06-20',
      zoo_operating_hours=OperatingHours(
         open_seconds=9 * 3600,
         close_seconds=19 * 3600 ) )

   assert soft_pins == []


def test_attraction_stop_for_soft_pin_and_duration_helpers() -> None:
   attraction = ItineraryAttractionRecord(
      attraction='Zoomobile',
      old_likelihood=None,
      new_likelihood=100 )
   soft_pin = AttractionHoursSoftPin(
      loop_id='zoomobile',
      viewing_spot_index=0,
      attraction_name='Zoomobile',
      open_seconds=10 * 3600,
      close_seconds=18 * 3600 )
   other = AttractionHoursSoftPin(
      loop_id='carousel',
      viewing_spot_index=0,
      attraction_name='Conservation Carousel',
      open_seconds=9 * 3600 + 30 * 60,
      close_seconds=18 * 3600 )

   assert hours_module._attraction_stop_for_soft_pin( [ attraction ], soft_pin ) is attraction
   assert hours_module._attraction_stop_for_soft_pin( [ attraction ], other ) is None
   assert hours_module._stop_is_soft_pinned_attraction(
      attraction,
      { 'Zoomobile' } ) is True
   assert hours_module._still_unscheduled_stops(
      [ attraction ],
      scheduled_stop_ids={ id( attraction ) } ) == []

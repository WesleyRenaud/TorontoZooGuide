from __future__ import annotations

from datetime import date

from support import ANIMAL_KEY

from api.itinerary.logic.parse_schedule_item_request import parse_schedule_item_request
from api.itinerary.scheduling.find_next_available_slot import find_next_available_slot
from api.itinerary.scheduling.scheduling_anchor import scheduling_anchor_seconds
from api.itinerary.scheduling.time_block import time_blocks_overlap
from api.itinerary.scheduling.time_block import TimeBlock
from api.shared.enums import ItineraryEventType
from api.shared.enums import ScheduleItemKind
from api.zoo_hours.data_access.zoo_hours import fetch_zoo_hours_record
from conftest import DbControllers


def test_schedule_item_kind_from_item_type_accepts_module_types() -> None:
   assert ScheduleItemKind.from_item_type( 'animals' ) == ScheduleItemKind.ANIMAL
   assert ScheduleItemKind.from_item_type( 'attractions' ) == ScheduleItemKind.ATTRACTION
   assert ScheduleItemKind.ANIMAL.item_type == 'animals'
   assert ScheduleItemKind.ATTRACTION.item_type == 'attractions'


def test_parse_schedule_item_request_animal_key() -> None:
   parsed = parse_schedule_item_request( 'animals', ANIMAL_KEY )

   assert parsed is not None
   assert parsed.kind == ScheduleItemKind.ANIMAL
   assert parsed.species == 'African Lion'
   assert parsed.exhibit == 'Africa Savanna'


def test_parse_schedule_item_request_event_type_as_item_type() -> None:
   parsed = parse_schedule_item_request( 'lunch', '' )

   assert parsed is not None
   assert parsed.kind == ScheduleItemKind.EVENT
   assert parsed.event_type == ItineraryEventType.LUNCH


def test_parse_schedule_item_request_attraction_key() -> None:
   parsed = parse_schedule_item_request( 'attractions', 'Conservation Carousel' )

   assert parsed is not None
   assert parsed.kind == ScheduleItemKind.ATTRACTION
   assert parsed.attraction_name == 'Conservation Carousel'


def test_scheduling_anchor_uses_arrival_when_set( db: DbControllers ) -> None:
   zoo_hours = fetch_zoo_hours_record( db.conn, date( 2026, 6, 20 ) )

   assert scheduling_anchor_seconds( zoo_hours, '09:00' ) == 9 * 3600
   assert scheduling_anchor_seconds( zoo_hours, None ) == 9 * 3600 + 30 * 60


def test_scheduling_anchor_ignores_early_admission_without_arrival(
      db: DbControllers ) -> None:
   zoo_hours = fetch_zoo_hours_record( db.conn, date( 2026, 6, 20 ) )

   assert zoo_hours.early_admission_time == '09:00'
   assert zoo_hours.open_time == '09:30'
   assert scheduling_anchor_seconds( zoo_hours, None ) == 9 * 3600 + 30 * 60


def test_find_next_available_slot_skips_overlapping_blockers() -> None:
   blockers = [
      TimeBlock(
         start_seconds=9 * 3600 + 30 * 60,
         end_seconds=9 * 3600 + 38 * 60 ),
   ]

   slot = find_next_available_slot(
      blockers,
      anchor_seconds=9 * 3600 + 30 * 60,
      duration_seconds=8 * 60,
      day_end_seconds=17 * 3600 )

   assert slot == ( '09:38', '09:46' )


def test_find_next_available_slot_returns_none_when_window_is_too_short() -> None:
   assert find_next_available_slot(
      [],
      anchor_seconds=9 * 3600 + 30 * 60,
      duration_seconds=8 * 60,
      day_end_seconds=9 * 3600 + 35 * 60,
   ) is None


def test_time_blocks_overlap_allows_adjacent_slots() -> None:
   first = TimeBlock( start_seconds=9 * 60 * 60, end_seconds=( 9 * 60 + 30 ) * 60 )
   second = TimeBlock( start_seconds=( 9 * 60 + 30 ) * 60, end_seconds=10 * 60 * 60 )

   assert not time_blocks_overlap( first, second )

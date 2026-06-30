from __future__ import annotations

from datetime import date

from itinerary.support import ANIMAL_KEY, PENGUIN_KEY

from api.itinerary.animal_item_key import AnimalScheduleItemKey
from api.itinerary.attraction_item_key import AttractionScheduleItemKey
from api.itinerary.scheduling.core.find_next_available_slot import find_next_available_slot
from api.itinerary.scheduling.core.scheduling_anchor import scheduling_anchor_seconds
from api.itinerary.scheduling.core.time_block import time_blocks_overlap
from api.itinerary.scheduling.core.time_block import TimeBlock
from api.itinerary.scheduling.items.map_schedule_item_key_from_wire import map_schedule_item_key_from_wire
from api.shared.enums import ItineraryEventType
from api.shared.enums import ScheduleItemKind
from api.zoo_hours.data_access.zoo_hours import fetch_zoo_hours_record
from conftest import DbControllers


def test_schedule_item_kind_normalizes_entrance() -> None:
   assert ScheduleItemKind.normalize( 'entrance' ) == ScheduleItemKind.ENTRANCE


def test_schedule_item_kind_from_item_type_accepts_module_types() -> None:
   assert ScheduleItemKind.from_item_type( 'animals' ) == ScheduleItemKind.ANIMAL
   assert ScheduleItemKind.from_item_type( 'attractions' ) == ScheduleItemKind.ATTRACTION
   assert ScheduleItemKind.ANIMAL.item_type == 'animals'
   assert ScheduleItemKind.ATTRACTION.item_type == 'attractions'


def test_map_schedule_item_key_from_wire_animal_key() -> None:
   schedule_item_key = map_schedule_item_key_from_wire( 'animals', ANIMAL_KEY )

   assert schedule_item_key == AnimalScheduleItemKey(
      species='African Lion',
      exhibit='Africa Savanna' )


def test_map_schedule_item_key_from_wire_animal_key_with_enclosure_name() -> None:
   schedule_item_key = map_schedule_item_key_from_wire( 'animals', PENGUIN_KEY )

   assert schedule_item_key == AnimalScheduleItemKey(
      species='African Penguin',
      exhibit='Africa Savanna',
      enclosure_name='Outdoor' )


def test_map_schedule_item_key_from_wire_event_type_as_item_type() -> None:
   schedule_item_key = map_schedule_item_key_from_wire( 'lunch', '' )

   assert schedule_item_key == ItineraryEventType.LUNCH


def test_map_schedule_item_key_from_wire_attraction_key() -> None:
   schedule_item_key = map_schedule_item_key_from_wire(
      'attractions',
      'Conservation Carousel' )

   assert schedule_item_key == AttractionScheduleItemKey(
      name='Conservation Carousel' )


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

   assert slot == ( '9:38 AM', '9:46 AM' )


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

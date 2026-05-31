from api.itinerary.logic.parse_schedule_time_options import parse_schedule_time_options
from api.itinerary.scheduling.resolve_schedule_slot import resolve_schedule_slot
from api.itinerary.scheduling.time_block import TimeBlock
from api.shared.enums import ItineraryErrorType


def test_resolve_schedule_slot_uses_anchor_when_start_time_is_unset() -> None:
   slot = resolve_schedule_slot(
      [],
      anchor_minutes=9 * 60 + 30,
      duration_minutes=8,
      day_end_minutes=17 * 60 )

   assert slot == ( '09:30', '09:38' )


def test_resolve_schedule_slot_honors_requested_start_time() -> None:
   blockers = [
      TimeBlock( start_minutes=9 * 60 + 30, end_minutes=9 * 60 + 38 ),
   ]

   slot = resolve_schedule_slot(
      blockers,
      anchor_minutes=9 * 60 + 30,
      duration_minutes=8,
      day_end_minutes=17 * 60,
      start_time='10:00' )

   assert slot == ( '10:00', '10:08' )


def test_resolve_schedule_slot_returns_none_when_requested_slot_overlaps() -> None:
   blockers = [
      TimeBlock( start_minutes=10 * 60, end_minutes=10 * 60 + 8 ),
   ]

   assert resolve_schedule_slot(
      blockers,
      anchor_minutes=9 * 60 + 30,
      duration_minutes=8,
      day_end_minutes=17 * 60,
      start_time='10:00',
   ) is None


def test_parse_schedule_time_options_rejects_duration_without_time() -> None:
   assert parse_schedule_time_options( None, 30 ) == ItineraryErrorType.SAVE_FAILED

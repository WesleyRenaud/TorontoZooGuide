from api.itinerary.scheduling.core.resolve_schedule_slot import resolve_schedule_slot
from api.itinerary.scheduling.core.time_block import TimeBlock
from api.itinerary.scheduling.items.parse_schedule_time_options import parse_schedule_time_options
from api.shared.enums import ItineraryErrorType

ANCHOR_SECONDS = 9 * 3600 + 30 * 60
DAY_END_SECONDS = 17 * 3600
DURATION_SECONDS = 8 * 60


def test_resolve_schedule_slot_uses_anchor_when_start_time_is_unset() -> None:
   slot = resolve_schedule_slot(
      [],
      anchor_seconds=ANCHOR_SECONDS,
      duration_seconds=DURATION_SECONDS,
      day_end_seconds=DAY_END_SECONDS )

   assert slot == ( '9:30 AM', '9:38 AM' )


def test_resolve_schedule_slot_honors_requested_start_time() -> None:
   blockers = [
      TimeBlock(
         start_seconds=9 * 3600 + 30 * 60,
         end_seconds=9 * 3600 + 38 * 60 ),
   ]

   slot = resolve_schedule_slot(
      blockers,
      anchor_seconds=ANCHOR_SECONDS,
      duration_seconds=DURATION_SECONDS,
      day_end_seconds=DAY_END_SECONDS,
      start_time='10:00' )

   assert slot == ( '10:00 AM', '10:08 AM' )


def test_resolve_schedule_slot_returns_none_when_requested_slot_overlaps() -> None:
   blockers = [
      TimeBlock(
         start_seconds=10 * 3600,
         end_seconds=10 * 3600 + 8 * 60 ),
   ]

   assert resolve_schedule_slot(
      blockers,
      anchor_seconds=ANCHOR_SECONDS,
      duration_seconds=DURATION_SECONDS,
      day_end_seconds=DAY_END_SECONDS,
      start_time='10:00',
   ) is None


def test_parse_schedule_time_options_rejects_duration_without_time() -> None:
   assert parse_schedule_time_options( None, 30 ) == ItineraryErrorType.SAVE_FAILED


def test_parse_schedule_time_options_rejects_invalid_provided_start_time() -> None:
   assert parse_schedule_time_options( 'not-a-time', None ) == ItineraryErrorType.SAVE_FAILED
   assert parse_schedule_time_options( '   ', 30 ) == ItineraryErrorType.SAVE_FAILED

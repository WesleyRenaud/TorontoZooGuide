from api.itinerary.scheduling.core.schedule_slot_resolver import ScheduleSlotResolver
from api.itinerary.scheduling.core.time_block import TimeBlock
from api.itinerary.scheduling.items.parsed_schedule_time_options import ParsedScheduleTimeOptions
from api.itinerary.scheduling.items.schedule_time_options_parser import ScheduleTimeOptionsParser
from api.shared.enums import ItineraryErrorType

ANCHOR_SECONDS = 9 * 3600 + 30 * 60
DAY_END_SECONDS = 17 * 3600
DURATION_SECONDS = 8 * 60


def test_resolve_schedule_slot_uses_anchor_when_start_time_is_unset() -> None:
   slot = ScheduleSlotResolver.resolve(
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

   slot = ScheduleSlotResolver.resolve(
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

   assert ScheduleSlotResolver.resolve(
      blockers,
      anchor_seconds=ANCHOR_SECONDS,
      duration_seconds=DURATION_SECONDS,
      day_end_seconds=DAY_END_SECONDS,
      start_time='10:00',
   ) is None


def test_parse_schedule_time_options_allows_duration_without_time() -> None:
   assert ScheduleTimeOptionsParser.parse( None, 30 ) == ParsedScheduleTimeOptions(
      start_time=None,
      duration_minutes=30,
   )
   assert ScheduleTimeOptionsParser.parse( '   ', 30 ) == ParsedScheduleTimeOptions(
      start_time=None,
      duration_minutes=30,
   )


def test_parse_schedule_time_options_rejects_invalid_provided_start_time() -> None:
   assert ScheduleTimeOptionsParser.parse( 'not-a-time', None ) == ItineraryErrorType.SAVE_FAILED

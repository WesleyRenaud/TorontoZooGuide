from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import guardians_talk_save_entry

from api.exhibits.coordinators.exhibit_coordinator import ExhibitCoordinator
from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.results.itinerary_save_result import ItinerarySaveResult
from api.itinerary.routing.itinerary_stop import ItineraryStop
from api.itinerary.routing.loop_schedule_pin import LoopSchedulePin
from api.itinerary.routing.partition_itinerary_schedule_windows import ItineraryScheduleWindow
from api.itinerary.scheduling.bulk.bulk_schedule_loop_pins import keep_completable_loop_pins
from api.models import Animal
from api.shared.calendar_dates import DateValues
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ScheduleItemKind
from conftest import DbControllers

ZEBRA_TALK = "Grevy's Zebra"
CAMEL_TALK = 'Bactrian Camel'
AFRICA_SAVANNA = 'Africa Savanna'
EURASIA_WILDS = 'Eurasia Wilds'

# From animals.db GuardiansTalkSchedule (2026-06-27 .. 2026-09-07):
# Grevy's Zebra: Mon/Wed 12:00 PM
# Bactrian Camel: every day 12:30 PM
VISIT_DATE = '2026-07-01'  # Wednesday (zebra day + early admission)
ZEBRA_TIME = '12:00'
CAMEL_TIME = '12:30'


def _selected_exhibits_for_africa_savanna() -> list[ str ]:
   for region in ExhibitCoordinator.get_regions_with_exhibits():
      if AFRICA_SAVANNA in region.exhibits:
         return [ AFRICA_SAVANNA ]

   raise AssertionError( f'{ AFRICA_SAVANNA } exhibit not found in seed data' )


def _set_summer_zebra_and_camel_schedules_from_database() -> None:
   assert GuardiansCoordinator.set_guardians_talk_schedule(
      talk=ZEBRA_TALK,
      location=AFRICA_SAVANNA,
      start_date='2026-06-27',
      end_date='2026-09-07',
      monday_time=ZEBRA_TIME,
      tuesday_time=None,
      wednesday_time=ZEBRA_TIME,
      thursday_time=None,
      friday_time=None,
      saturday_time=None,
      sunday_time=None,
      message="The Grevy's Zebra at Africa Savanna is not scheduled today.",
   )
   assert GuardiansCoordinator.set_guardians_talk_schedule(
      talk=CAMEL_TALK,
      location=EURASIA_WILDS,
      start_date='2026-06-27',
      end_date='2026-09-07',
      monday_time=CAMEL_TIME,
      tuesday_time=CAMEL_TIME,
      wednesday_time=CAMEL_TIME,
      thursday_time=CAMEL_TIME,
      friday_time=CAMEL_TIME,
      saturday_time=CAMEL_TIME,
      sunday_time=CAMEL_TIME,
      message='The Bactrian Camel at Eurasia Wilds is not scheduled today.',
   )


def _seconds( value: str | None ) -> int | None:
   if not value:
      return None

   return DateValues.time_value_in_seconds( value )


def _last_animal_before(
      result: ItinerarySaveResult,
      *,
      before_seconds: int ) -> Animal | None:
   candidates = [
      animal
      for animal in result.itinerary.animals
      if ( end := _seconds( animal.end_time ) ) is not None
      and end <= before_seconds
   ]
   if not candidates:
      return None

   return max(
      candidates,
      key=lambda animal: _seconds( animal.end_time ) or 0 )


def _talk_loop_pin(
      *,
      loop_id: str,
      viewing_spot_index: int,
      item_key: str,
      start_seconds: int,
      end_seconds: int ) -> LoopSchedulePin:
   return LoopSchedulePin(
      loop_id=loop_id,
      viewing_spot_index=viewing_spot_index,
      stop=ItineraryStop(
         schedule_item_kind=ScheduleItemKind.GUARDIANS_TALK,
         item_key=item_key,
         walk_node_ids=( 'v-0000', ),
         is_fixed_time=True ),
      start_seconds=start_seconds,
      end_seconds=end_seconds,
   )


def test_keep_completable_loop_pins_drops_pin_without_post_talk_window() -> None:
   zebra_pin = _talk_loop_pin(
      loop_id='africa_savanna_canadian_domain',
      viewing_spot_index=18,
      item_key=ZEBRA_TALK,
      start_seconds=12 * 3600,
      end_seconds=12 * 3600 + 30 * 60 )
   camel_pin = _talk_loop_pin(
      loop_id='eurasia',
      viewing_spot_index=1,
      item_key=CAMEL_TALK,
      start_seconds=12 * 3600 + 30 * 60,
      end_seconds=13 * 3600 )
   schedule_windows = [
      ItineraryScheduleWindow(
         start_seconds=9 * 3600,
         end_seconds=12 * 3600 ),
      ItineraryScheduleWindow(
         start_seconds=13 * 3600,
         end_seconds=17 * 3600 ),
   ]

   kept_pins = keep_completable_loop_pins(
      schedule_windows,
      [ zebra_pin, camel_pin ] )

   assert kept_pins == [ camel_pin ]


def test_keep_completable_loop_pins_keeps_pin_with_post_talk_window() -> None:
   zebra_pin = _talk_loop_pin(
      loop_id='africa_savanna_canadian_domain',
      viewing_spot_index=18,
      item_key=ZEBRA_TALK,
      start_seconds=12 * 3600,
      end_seconds=12 * 3600 + 30 * 60 )
   schedule_windows = [
      ItineraryScheduleWindow(
         start_seconds=9 * 3600,
         end_seconds=12 * 3600 ),
      ItineraryScheduleWindow(
         start_seconds=12 * 3600 + 30 * 60,
         end_seconds=17 * 3600 ),
   ]

   kept_pins = keep_completable_loop_pins( schedule_windows, [ zebra_pin ] )

   assert kept_pins == [ zebra_pin ]


def test_adjacent_zebra_then_camel_anchors_savanna_loop_before_zebra(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   """Africa + zebra (12:00) + camel (12:30) using animals.db talk schedules.

   Camel immediately after zebra means the zebra talk cannot weave the savanna
   loop. Demote zebra to an anchor so the whole savanna loop packs before it
   instead of splitting across the camel talk.
   """
   freeze_database_today( date( 2026, 7, 1 ) )
   _set_summer_zebra_and_camel_schedules_from_database()

   assert ItineraryCoordinator.set_itinerary(
      date=VISIT_DATE,
      arrival_time='09:00',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[
         guardians_talk_save_entry( ZEBRA_TALK ),
         guardians_talk_save_entry( CAMEL_TALK ),
      ],
      wild_encounters=[],
      selected_exhibits=_selected_exhibits_for_africa_savanna(),
      confirming_early_admission=True,
   ).success

   result = ItineraryCoordinator.bulk_schedule_animals()

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS

   zebra_talk = next(
      talk for talk in result.itinerary.guardians_talks
      if talk.name == ZEBRA_TALK )
   camel_talk = next(
      talk for talk in result.itinerary.guardians_talks
      if talk.name == CAMEL_TALK )
   zebra_start = _seconds( zebra_talk.start_time )
   camel_start = _seconds( camel_talk.start_time )
   camel_end = _seconds( camel_talk.end_time )
   assert zebra_start == _seconds( '12:00 PM' )
   assert camel_start == _seconds( '12:30 PM' )
   assert camel_end is not None

   last_before_zebra = _last_animal_before(
      result,
      before_seconds=zebra_start )
   assert last_before_zebra is not None, 'Expected animals before zebra'

   last_end = _seconds( last_before_zebra.end_time )
   assert last_end is not None
   gap_minutes = ( zebra_start - last_end ) / 60

   assert gap_minutes < 15, (
      f'Dead space of { gap_minutes :.1f } min between '
      f'{ last_before_zebra.species } ({ last_before_zebra.end_time }) '
      f'and zebra talk ({ zebra_talk.start_time })'
   )

   savanna_after_camel = [
      animal
      for animal in result.itinerary.animals
      if animal.exhibit == AFRICA_SAVANNA
      and ( start := _seconds( animal.start_time ) ) is not None
      and start >= camel_end
   ]
   assert savanna_after_camel == [], (
      'Savanna loop must not continue after the camel talk when zebra was '
      'demoted to an anchor'
   )

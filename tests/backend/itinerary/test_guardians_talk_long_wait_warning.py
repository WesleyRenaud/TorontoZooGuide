from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import entrance_travel_seconds_to_animal, guardians_talk_save_entry, LION_ITINERARY_ENTRY, LION_KEY, parsed_schedule_item, schedule_itinerary_item, schedule_time_after_seconds
from wild_encounter_schedule_support import wire_schedule_row, wire_schedule_rows

from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.scheduling.core.guest_item_schedule_status_checker import GuestItemScheduleStatusChecker
from api.itinerary.scheduling.core.time_block import TimeBlock
from api.itinerary.scheduling.core.time_block_builder import TimeBlockBuilder
from api.itinerary.warnings.guardians_talk_long_wait_warning_builder import GuardiansTalkLongWaitWarningBuilder
from api.models import Animal
from api.models import GuardiansTalk
from api.shared.constants import MAX_FIXED_TIME_ITEM_WAIT_MINUTES
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ScheduleItemKind
from conftest import DbControllers

ZEBRA_TALK = "Grevy's Zebra"
MEERKAT_TALK = 'Slender-Tailed Meerkat'
NEW_WORLD_PRIMATES_TALK = 'New World Primates'
TAMARIN_ITINERARY_ENTRY = {
   'species': 'Golden Lion Tamarin',
   'exhibit': 'Americas Pavilion',
   'enclosure_name': 'Outdoor',
}
TAMARIN_KEY = 'Golden Lion Tamarin||Americas Pavilion||Outdoor'


def _set_talk_schedule(
      talk: str,
      *,
      location: str,
      talk_time: str ) -> None:
   assert GuardiansCoordinator.set_guardians_talk_schedule(
      talk=talk,
      location=location,
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows( talk_time, monday=True, tuesday=True, wednesday=True, thursday=True, friday=True, saturday=True, sunday=True ),
      message=None,
   )


def _set_zebra_and_meerkat_schedules() -> None:
   _set_talk_schedule(
      ZEBRA_TALK,
      location='Africa Savanna',
      talk_time='10:00' )
   _set_talk_schedule(
      MEERKAT_TALK,
      location='African Rainforest Pavilion',
      talk_time='13:00' )


def test_time_block_gap_seconds_between_non_overlapping_blocks() -> None:
   morning = TimeBlock( start_seconds=9 * 3600, end_seconds=9 * 3600 + 30 * 60 )
   afternoon = TimeBlock(
      start_seconds=11 * 3600,
      end_seconds=11 * 3600 + 30 * 60 )

   assert TimeBlockBuilder.gap_seconds( morning, afternoon ) == 90 * 60
   assert TimeBlockBuilder.gap_seconds( afternoon, morning ) == 90 * 60


def test_isolated_guardians_talks_detects_talk_far_from_other_items() -> None:
   itinerary = ItineraryBuilder.empty()
   itinerary.animals = [
      Animal(
         species='African Lion',
         exhibit='Africa Savanna',
         start_time='10:00 AM',
         end_time='10:08 AM' ),
   ]
   itinerary.guardians_talks = [
      GuardiansTalk(
         name=ZEBRA_TALK,
         location='Africa Savanna',
         x_coord=0.0,
         y_coord=0.0,
         start_time='10:15 AM',
         end_time='10:45 AM' ),
      GuardiansTalk(
         name=MEERKAT_TALK,
         location='African Rainforest Pavilion',
         x_coord=0.0,
         y_coord=0.0,
         start_time='1:00 PM',
         end_time='1:30 PM' ),
   ]

   isolated = GuardiansTalkLongWaitWarningBuilder.isolated_from_itinerary( itinerary )

   assert [ talk.name for talk in isolated ] == [ MEERKAT_TALK ]
   assert MAX_FIXED_TIME_ITEM_WAIT_MINUTES == 30


def test_isolated_guardians_talks_ignores_talk_near_other_items() -> None:
   itinerary = ItineraryBuilder.empty()
   itinerary.animals = [
      Animal(
         species='African Lion',
         exhibit='Africa Savanna',
         start_time='10:00 AM',
         end_time='10:08 AM' ),
   ]
   itinerary.guardians_talks = [
      GuardiansTalk(
         name=ZEBRA_TALK,
         location='Africa Savanna',
         x_coord=0.0,
         y_coord=0.0,
         start_time='10:15 AM',
         end_time='10:45 AM' ),
   ]

   assert GuardiansTalkLongWaitWarningBuilder.isolated_from_itinerary( itinerary ) == []


def test_set_itinerary_warns_when_talk_is_far_from_other_scheduled_talk(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   _set_zebra_and_meerkat_schedules()

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[
         guardians_talk_save_entry( ZEBRA_TALK, start_time='10:00' ),
         guardians_talk_save_entry( MEERKAT_TALK, start_time='13:00' ),
      ],
      wild_encounters=[],
      confirming_guardians_talk_without_animal=True,
   )

   assert not result.success
   assert result.status == ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT
   assert result.reasons[ 0 ].code == ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT
   assert { item.name for item in result.reasons[ 0 ].items } == {
      ZEBRA_TALK,
      MEERKAT_TALK,
   }

   confirmed = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[
         guardians_talk_save_entry( ZEBRA_TALK, start_time='10:00' ),
         guardians_talk_save_entry( MEERKAT_TALK, start_time='13:00' ),
      ],
      wild_encounters=[],
      confirming_fixed_time_item_long_wait=True,
      confirming_guardians_talk_without_animal=True,
   )

   assert confirmed.success


def test_schedule_talk_warns_when_far_from_existing_scheduled_items(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   _set_zebra_and_meerkat_schedules()

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[ guardians_talk_save_entry( ZEBRA_TALK, start_time='10:00' ) ],
      wild_encounters=[],
      confirming_guardians_talk_without_animal=True,
   ).success
   assert schedule_itinerary_item(
      ScheduleItemKind.ANIMAL.item_type,
      LION_KEY,
      start_time='10:30',
   ).success

   result = schedule_itinerary_item(
      ScheduleItemKind.GUARDIANS_TALK.item_type,
      f'{ MEERKAT_TALK }||13:00',
      confirming_guardians_talk_without_animal=True,
   )

   assert not result.success
   assert result.status == ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT
   assert [ item.name for item in result.reasons[ 0 ].items ] == [ MEERKAT_TALK ]

   confirmed = ItineraryCoordinator.schedule_itinerary_item(
      parsed_schedule_item(
         ScheduleItemKind.GUARDIANS_TALK.item_type,
         f'{ MEERKAT_TALK }||13:00' ),
      confirming_fixed_time_item_long_wait=True,
      confirming_guardians_talk_without_animal=True,
   )

   assert confirmed.success


def test_schedule_talk_skips_long_wait_when_bulk_pack_would_close_gap(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   _set_talk_schedule(
      NEW_WORLD_PRIMATES_TALK,
      location='Americas Pavilion',
      talk_time='12:00' )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[ TAMARIN_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success
   animal_scheduled = schedule_itinerary_item(
      ScheduleItemKind.ANIMAL.item_type,
      TAMARIN_KEY,
   )

   assert animal_scheduled.success

   animal_times_before = [
      ( animal.species, animal.start_time, animal.end_time )
      for animal in animal_scheduled.itinerary.animals
   ]

   assert animal_times_before
   assert all(
      GuestItemScheduleStatusChecker.has_schedule_times( start_time, end_time )
      for _, start_time, end_time in animal_times_before
   )

   result = schedule_itinerary_item(
      ScheduleItemKind.GUARDIANS_TALK.item_type,
      f'{ NEW_WORLD_PRIMATES_TALK }||12:00',
   )

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS
   assert [
      ( animal.species, animal.start_time, animal.end_time )
      for animal in result.itinerary.animals
   ] == animal_times_before
   assert [ talk.name for talk in result.itinerary.guardians_talks ] == [
      NEW_WORLD_PRIMATES_TALK,
   ]


def test_schedule_talk_warns_when_no_previously_scheduled_animals_to_pack(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   _set_zebra_and_meerkat_schedules()

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[
         guardians_talk_save_entry( ZEBRA_TALK, start_time='10:00' ),
      ],
      wild_encounters=[],
      confirming_guardians_talk_without_animal=True,
   ).success

   result = schedule_itinerary_item(
      ScheduleItemKind.GUARDIANS_TALK.item_type,
      f'{ MEERKAT_TALK }||13:00',
      confirming_guardians_talk_without_animal=True,
   )

   assert not result.success
   assert result.status == ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT
   assert [ item.name for item in result.reasons[ 0 ].items ] == [ MEERKAT_TALK ]


def test_set_itinerary_skips_long_wait_warning_for_already_saved_talks(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   _set_zebra_and_meerkat_schedules()

   confirmed = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[
         guardians_talk_save_entry( ZEBRA_TALK, start_time='10:00' ),
         guardians_talk_save_entry( MEERKAT_TALK, start_time='13:00' ),
      ],
      wild_encounters=[],
      confirming_fixed_time_item_long_wait=True,
      confirming_guardians_talk_without_animal=True,
   )

   assert confirmed.success

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[
         guardians_talk_save_entry( ZEBRA_TALK, start_time='10:00' ),
         guardians_talk_save_entry( MEERKAT_TALK, start_time='13:00' ),
      ],
      wild_encounters=[],
      confirming_guardians_talk_without_animal=True,
   )

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS
   assert { talk.name for talk in result.itinerary.guardians_talks } == {
      ZEBRA_TALK,
      MEERKAT_TALK,
   }


def test_bulk_schedule_skips_long_wait_warning_for_already_saved_talks(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   _set_talk_schedule(
      ZEBRA_TALK,
      location='Africa Savanna',
      talk_time='12:00' )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[
         guardians_talk_save_entry( ZEBRA_TALK, start_time='12:00' ),
      ],
      wild_encounters=[],
      confirming_fixed_time_item_long_wait=True,
      confirming_guardians_talk_without_animal=True,
   ).success

   assert schedule_itinerary_item(
      ScheduleItemKind.ANIMAL.item_type,
      LION_KEY,
   ).success

   result = ItineraryCoordinator.bulk_schedule_itinerary()

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS
   assert [ talk.name for talk in result.itinerary.guardians_talks ] == [ ZEBRA_TALK ]
   assert all(
      GuestItemScheduleStatusChecker.has_schedule_times( animal.start_time, animal.end_time )
      for animal in result.itinerary.animals
   )


def test_set_itinerary_warns_only_for_newly_added_talk_with_long_wait(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   _set_zebra_and_meerkat_schedules()

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[ guardians_talk_save_entry( ZEBRA_TALK, start_time='10:00' ) ],
      wild_encounters=[],
      confirming_guardians_talk_without_animal=True,
   ).success

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[
         guardians_talk_save_entry( ZEBRA_TALK, start_time='10:00' ),
         guardians_talk_save_entry( MEERKAT_TALK, start_time='13:00' ),
      ],
      wild_encounters=[],
      confirming_guardians_talk_without_animal=True,
   )

   assert not result.success
   assert result.status == ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT
   assert [ item.name for item in result.reasons[ 0 ].items ] == [ MEERKAT_TALK ]

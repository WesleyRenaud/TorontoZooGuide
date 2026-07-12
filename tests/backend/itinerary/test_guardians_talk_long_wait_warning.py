from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import guardians_talk_save_entry, LION_ITINERARY_ENTRY, LION_KEY, parsed_schedule_item, schedule_itinerary_item

from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.domain.itinerary import empty_itinerary
from api.itinerary.scheduling.bulk.bulk_schedule_animals import has_itinerary_schedule_times
from api.itinerary.scheduling.core.time_block import time_block_gap_seconds
from api.itinerary.scheduling.core.time_block import TimeBlock
from api.itinerary.warnings.guardians_talk_long_wait_warning import isolated_guardians_talks_from_itinerary
from api.models import Animal
from api.models import GuardiansTalk
from api.shared.constants import MAX_GUARDIANS_TALK_WAIT_MINUTES
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ScheduleItemKind
from conftest import DbControllers

ZEBRA_TALK = "Grevy's Zebra"
MEERKAT_TALK = 'Slender-Tailed Meerkat'


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
      monday_time=talk_time,
      tuesday_time=talk_time,
      wednesday_time=talk_time,
      thursday_time=talk_time,
      friday_time=talk_time,
      saturday_time=talk_time,
      sunday_time=talk_time,
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

   assert time_block_gap_seconds( morning, afternoon ) == 90 * 60
   assert time_block_gap_seconds( afternoon, morning ) == 90 * 60


def test_isolated_guardians_talks_detects_talk_far_from_other_items() -> None:
   itinerary = empty_itinerary()
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

   isolated = isolated_guardians_talks_from_itinerary( itinerary )

   assert [ talk.name for talk in isolated ] == [ MEERKAT_TALK ]
   assert MAX_GUARDIANS_TALK_WAIT_MINUTES == 30


def test_isolated_guardians_talks_ignores_talk_near_other_items() -> None:
   itinerary = empty_itinerary()
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

   assert isolated_guardians_talks_from_itinerary( itinerary ) == []


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
         guardians_talk_save_entry( ZEBRA_TALK ),
         guardians_talk_save_entry( MEERKAT_TALK ),
      ],
      wild_encounters=[],
      confirming_guardians_talk_without_animal=True,
   )

   assert not result.success
   assert result.status == ItineraryErrorType.GUARDIANS_TALK_LONG_WAIT
   assert result.reasons[ 0 ].code == ItineraryErrorType.GUARDIANS_TALK_LONG_WAIT
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
         guardians_talk_save_entry( ZEBRA_TALK ),
         guardians_talk_save_entry( MEERKAT_TALK ),
      ],
      wild_encounters=[],
      confirming_guardians_talk_long_wait=True,
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
      guardians_talks=[ guardians_talk_save_entry( ZEBRA_TALK ) ],
      wild_encounters=[],
      confirming_guardians_talk_without_animal=True,
   ).success
   assert schedule_itinerary_item(
      ScheduleItemKind.ANIMAL.item_type,
      LION_KEY,
      start_time='10:30',
   ).success
   assert schedule_itinerary_item(
      ScheduleItemKind.GUARDIANS_TALK.item_type,
      ZEBRA_TALK,
      confirming_guardians_talk_without_animal=True,
   ).success

   result = schedule_itinerary_item(
      ScheduleItemKind.GUARDIANS_TALK.item_type,
      MEERKAT_TALK,
      confirming_guardians_talk_without_animal=True,
   )

   assert not result.success
   assert result.status == ItineraryErrorType.GUARDIANS_TALK_LONG_WAIT
   assert [ item.name for item in result.reasons[ 0 ].items ] == [ MEERKAT_TALK ]

   confirmed = ItineraryCoordinator.schedule_itinerary_item(
      parsed_schedule_item(
         ScheduleItemKind.GUARDIANS_TALK.item_type,
         MEERKAT_TALK ),
      confirming_guardians_talk_long_wait=True,
      confirming_guardians_talk_without_animal=True,
   )

   assert confirmed.success


def test_bulk_schedule_warns_and_leaves_schedule_unchanged_until_confirmed(
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
         guardians_talk_save_entry( ZEBRA_TALK ),
         guardians_talk_save_entry( MEERKAT_TALK ),
      ],
      wild_encounters=[],
      confirming_guardians_talk_long_wait=True,
      confirming_guardians_talk_without_animal=True,
   ).success

   warning = ItineraryCoordinator.bulk_schedule_animals()

   assert not warning.success
   assert warning.status == ItineraryErrorType.GUARDIANS_TALK_LONG_WAIT
   assert not any(
      has_itinerary_schedule_times( animal.start_time, animal.end_time )
      for animal in warning.itinerary.animals
   )

   confirmed = ItineraryCoordinator.bulk_schedule_animals(
      confirming_guardians_talk_long_wait=True,
   )

   assert confirmed.success
   assert any(
      has_itinerary_schedule_times( animal.start_time, animal.end_time )
      for animal in confirmed.itinerary.animals
   )

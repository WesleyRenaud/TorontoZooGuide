from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import LION_ITINERARY_ENTRY, LION_KEY, parsed_schedule_item, RHINO_ENCOUNTER, schedule_itinerary_item, WILD_ENCOUNTER, wild_encounter_key, wild_encounter_wire
from wild_encounter_schedule_support import wire_schedule_rows

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.scheduling.core.guest_item_schedule_status import has_itinerary_schedule_times
from api.itinerary.warnings.wild_encounter_long_wait_warning_builder import WildEncounterLongWaitWarningBuilder
from api.models import Animal
from api.models import WildEncounter
from api.shared.constants import MAX_FIXED_TIME_ITEM_WAIT_MINUTES
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ScheduleItemKind
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from conftest import DbControllers


def _set_encounter_schedule( encounter_name: str, *, encounter_time: str ) -> None:
   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name=encounter_name,
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows(
         encounter_time,
         monday=True,
         tuesday=True,
         wednesday=True,
         thursday=True,
         friday=True,
         saturday=True,
         sunday=True ),
      message=None,
   )


def _set_rainforest_and_rhino_schedules() -> None:
   _set_encounter_schedule( WILD_ENCOUNTER, encounter_time='10:00' )
   _set_encounter_schedule( RHINO_ENCOUNTER, encounter_time='13:00' )


def test_isolated_wild_encounters_detects_encounter_far_from_other_items() -> None:
   itinerary = ItineraryBuilder.empty()
   itinerary.animals = [
      Animal(
         species='African Lion',
         exhibit='Africa Savanna',
         start_time='10:00 AM',
         end_time='10:08 AM' ),
   ]
   itinerary.wild_encounters = [
      WildEncounter(
         name=WILD_ENCOUNTER,
         meeting_spot='Wild Encounter - Africa Meeting Spot',
         link='',
         start_time='10:15 AM',
         end_time='11:00 AM' ),
      WildEncounter(
         name=RHINO_ENCOUNTER,
         meeting_spot='Wild Encounter - Penguin Meeting Spot',
         link='',
         start_time='1:00 PM',
         end_time='1:45 PM' ),
   ]

   isolated = WildEncounterLongWaitWarningBuilder.isolated_from_itinerary( itinerary )

   assert [ encounter.name for encounter in isolated ] == [ RHINO_ENCOUNTER ]
   assert MAX_FIXED_TIME_ITEM_WAIT_MINUTES == 30


def test_isolated_wild_encounters_ignores_encounter_near_other_items() -> None:
   itinerary = ItineraryBuilder.empty()
   itinerary.animals = [
      Animal(
         species='African Lion',
         exhibit='Africa Savanna',
         start_time='10:00 AM',
         end_time='10:08 AM' ),
   ]
   itinerary.wild_encounters = [
      WildEncounter(
         name=WILD_ENCOUNTER,
         meeting_spot='Wild Encounter - Africa Meeting Spot',
         link='',
         start_time='10:15 AM',
         end_time='11:00 AM' ),
   ]

   assert WildEncounterLongWaitWarningBuilder.isolated_from_itinerary( itinerary ) == []


def test_set_itinerary_warns_when_encounter_is_far_from_other_scheduled_encounter(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   _set_rainforest_and_rhino_schedules()

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[
         wild_encounter_key( WILD_ENCOUNTER, start_time='10:00' ),
         wild_encounter_key( RHINO_ENCOUNTER, start_time='13:00' ),
      ],
   )

   assert not result.success
   assert result.status == ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT
   assert result.reasons[ 0 ].code == ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT
   assert { item.name for item in result.reasons[ 0 ].items } == {
      WILD_ENCOUNTER,
      RHINO_ENCOUNTER,
   }

   confirmed = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[
         wild_encounter_key( WILD_ENCOUNTER, start_time='10:00' ),
         wild_encounter_key( RHINO_ENCOUNTER, start_time='13:00' ),
      ],
      confirming_fixed_time_item_long_wait=True,
   )

   assert confirmed.success


def test_schedule_encounter_warns_when_far_from_existing_scheduled_items(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   _set_rainforest_and_rhino_schedules()

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[
         wild_encounter_key( WILD_ENCOUNTER, start_time='10:00' ),
      ],
   ).success
   assert schedule_itinerary_item(
      ScheduleItemKind.ANIMAL.item_type,
      LION_KEY,
      start_time='11:00',
   ).success

   result = schedule_itinerary_item(
      ScheduleItemKind.WILD_ENCOUNTER.item_type,
      wild_encounter_wire( RHINO_ENCOUNTER, start_time='13:00' ),
   )

   assert not result.success
   assert result.status == ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT
   assert [ item.name for item in result.reasons[ 0 ].items ] == [ RHINO_ENCOUNTER ]

   confirmed = ItineraryCoordinator.schedule_itinerary_item(
      parsed_schedule_item(
         ScheduleItemKind.WILD_ENCOUNTER.item_type,
         wild_encounter_wire( RHINO_ENCOUNTER, start_time='13:00' ) ),
      confirming_fixed_time_item_long_wait=True,
   )

   assert confirmed.success


def test_set_itinerary_skips_long_wait_warning_for_already_saved_encounters(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   _set_rainforest_and_rhino_schedules()

   confirmed = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[
         wild_encounter_key( WILD_ENCOUNTER, start_time='10:00' ),
         wild_encounter_key( RHINO_ENCOUNTER, start_time='13:00' ),
      ],
      confirming_fixed_time_item_long_wait=True,
   )

   assert confirmed.success

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[
         wild_encounter_key( WILD_ENCOUNTER, start_time='10:00' ),
         wild_encounter_key( RHINO_ENCOUNTER, start_time='13:00' ),
      ],
   )

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS
   assert { encounter.name for encounter in result.itinerary.wild_encounters } == {
      WILD_ENCOUNTER,
      RHINO_ENCOUNTER,
   }


def test_set_itinerary_warns_only_for_newly_added_encounter_with_long_wait(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   _set_rainforest_and_rhino_schedules()

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[
         wild_encounter_key( WILD_ENCOUNTER, start_time='10:00' ),
      ],
   ).success

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[
         wild_encounter_key( WILD_ENCOUNTER, start_time='10:00' ),
         wild_encounter_key( RHINO_ENCOUNTER, start_time='13:00' ),
      ],
   )

   assert not result.success
   assert result.status == ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT
   assert [ item.name for item in result.reasons[ 0 ].items ] == [ RHINO_ENCOUNTER ]


def test_bulk_schedule_skips_long_wait_warning_for_already_saved_encounters(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   _set_encounter_schedule( RHINO_ENCOUNTER, encounter_time='12:00' )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[
         wild_encounter_key( RHINO_ENCOUNTER, start_time='12:00' ),
      ],
      confirming_fixed_time_item_long_wait=True,
   ).success

   assert schedule_itinerary_item(
      ScheduleItemKind.ANIMAL.item_type,
      LION_KEY,
   ).success

   result = ItineraryCoordinator.bulk_schedule_itinerary()

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS
   assert [ encounter.name for encounter in result.itinerary.wild_encounters ] == [
      RHINO_ENCOUNTER,
   ]
   assert all(
      has_itinerary_schedule_times( animal.start_time, animal.end_time )
      for animal in result.itinerary.animals
   )

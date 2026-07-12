from __future__ import annotations

from collections.abc import Callable
from datetime import date

from wild_encounter_schedule_support import wire_schedule_row, wire_schedule_rows

from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.guardians.itinerary.guardians_talk_itinerary_validation import validate_guardians_talks_for_itinerary
from api.itinerary.data_access.itinerary_guardians_talk_input import ItineraryGuardiansTalkInput
from api.itinerary.wild_encounter_item_key import WildEncounterScheduleItemKey
from api.models import GuardiansTalk
from api.models import WildEncounter
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from api.wild_encounters.itinerary.wild_encounter_itinerary_validation import validate_wild_encounters_for_itinerary
from conftest import DbControllers


def test_validate_guardians_talks_splits_available_and_unavailable_entries() -> None:
   day_schedule = [
      GuardiansTalk(
         name='African Lion',
         location='Africa Savanna',
         x_coord=51.138,
         y_coord=41.279,
         start_time='10:00 AM',
         maximum_duration=30,
         is_available=True ),
   ]

   result = validate_guardians_talks_for_itinerary(
      guardians_talks_to_include=[
         ItineraryGuardiansTalkInput( name='African Lion', start_time='10:00' ),
         ItineraryGuardiansTalkInput( name='Amur Tiger', start_time='10:00' ),
      ],
      day_schedule=day_schedule )

   assert [
      ( d.name, d.is_deleted, d.start_time, d.end_time )
      for d in result
   ] == [
      ( 'African Lion', False, '10:00', '10:30 AM' ),
      ( 'Amur Tiger', True, '10:00', None ),
   ]


def test_validate_wild_encounters_splits_available_and_unavailable_entries() -> None:
   day_schedule = [
      WildEncounter(
         name='Kangaroo',
         meeting_spot='Wild Encounter - Eurasia Meeting Spot',
         link='https://www.torontozoo.com/tickets/wekangaroo',
         start_time='1:00 PM',
         maximum_duration=45,
         is_available=True ),
      WildEncounter(
         name='African Rainforest',
         meeting_spot='Wild Encounter - Africa Meeting Spot',
         link='https://www.torontozoo.com/tickets/weafricarainforest',
         start_time='2:00 PM',
         maximum_duration=45,
         is_available=False,
         unavailable_message='Unavailable.' ),
   ]

   result = validate_wild_encounters_for_itinerary(
      wild_encounters_to_include=[
         WildEncounterScheduleItemKey( name='African Rainforest', start_time='14:00' ),
         WildEncounterScheduleItemKey( name='Kangaroo', start_time='13:00' ),
      ],
      day_schedule=day_schedule )

   assert [
      ( d.name, d.is_deleted, d.start_time, d.end_time )
      for d in result
   ] == [
      ( 'African Rainforest', True, '2:00 PM', '2:45 PM' ),
      ( 'Kangaroo', False, '1:00 PM', '1:45 PM' ),
   ]


def test_scheduled_itinerary_filter_helpers_filter_case_insensitively_and_sort(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   assert GuardiansCoordinator.set_guardians_talk_schedule(
      talk='African Lion',
      location='Africa Savanna',
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows( '10:00', monday=True, tuesday=False, wednesday=False, thursday=False, friday=False, saturday=False, sunday=False ),
      message=None
   )
   assert GuardiansCoordinator.set_guardians_talk_schedule(
      talk='Amur Tiger',
      location='Eurasia Wilds',
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows( '09:00', monday=True, tuesday=False, wednesday=False, thursday=False, friday=False, saturday=False, sunday=False ),
      message=None
   )
   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name='African Rainforest',
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows( '14:00' ),
      message=None
   )
   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name='Kangaroo',
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows( '09:00' ),
      message=None
   )

   talk_result = validate_guardians_talks_for_itinerary(
      [
         ItineraryGuardiansTalkInput( name=' african lion ', start_time='10:00' ),
         ItineraryGuardiansTalkInput( name='AMUR TIGER', start_time='09:00' ),
      ],
      GuardiansCoordinator.get_guardians_talk_schedule(
         month='June',
         day=15,
         year=2026 )
   )
   encounter_result = validate_wild_encounters_for_itinerary(
      [
         WildEncounterScheduleItemKey( name=' kangaroo ', start_time='09:00' ),
         WildEncounterScheduleItemKey( name='AFRICAN RAINFOREST', start_time='14:00' ),
      ],
      WildEncounterCoordinator.get_wild_encounter_schedule(
         month='June',
         day=15,
         year=2026 )
   )

   assert [
      d.name for d in talk_result if not d.is_deleted
   ] == [
      'African Lion',
      'Amur Tiger',
   ]
   assert [
      ( d.name, d.is_deleted )
      for d in encounter_result
   ] == [
      ( 'Kangaroo', False ),
      ( 'African Rainforest', False ),
   ]

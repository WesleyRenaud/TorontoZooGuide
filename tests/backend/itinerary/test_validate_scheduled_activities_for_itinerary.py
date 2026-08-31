from __future__ import annotations

from collections.abc import Callable
from datetime import date

from wild_encounter_schedule_support import wire_schedule_rows

from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.guardians.itinerary.guardians_talk_itinerary_validator import GuardiansTalkItineraryValidator
from api.itinerary.data_access.itinerary_guardians_talk_input import ItineraryGuardiansTalkInput
from api.itinerary.wild_encounter_schedule_item_key import WildEncounterScheduleItemKey
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from api.wild_encounters.itinerary.wild_encounter_itinerary_validator import WildEncounterItineraryValidator
from conftest import DbControllers


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

   talk_result = GuardiansTalkItineraryValidator.validate_for_itinerary(
      [
         ItineraryGuardiansTalkInput( name=' african lion ', start_time='10:00' ),
         ItineraryGuardiansTalkInput( name='AMUR TIGER', start_time='09:00' ),
      ],
      GuardiansCoordinator.get_guardians_talk_schedule(
         month='June',
         day=15,
         year=2026 )
   )
   encounter_result = WildEncounterItineraryValidator.validate_for_itinerary(
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

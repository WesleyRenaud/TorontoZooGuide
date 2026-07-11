from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import LION_ITINERARY_ENTRY, schedule_itinerary_item, wild_encounter_wire
from wild_encounter_schedule_support import wire_schedule_row

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.shared.calendar_dates import DateValues
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ScheduleItemKind
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from conftest import DbControllers

BACTRIAN_CAMELS = 'Bactrian Camels'
CHEETAH_ITINERARY_ENTRY = {
   'species': 'Cheetah',
   'exhibit': 'Africa Savanna',
}


def _set_bactrian_camels_schedule( *, encounter_time: str = '15:30' ) -> None:
   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name=BACTRIAN_CAMELS,
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=[
         wire_schedule_row(
            encounter_time,
            monday=False,
            tuesday=False,
            wednesday=False,
            thursday=False,
            friday=False,
            saturday=True,
            sunday=False,
         ),
      ],
      message=None,
   )


def test_bulk_schedule_packs_animals_against_unpinned_afternoon_encounter(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )
   _set_bactrian_camels_schedule()

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      departure_time='12:00',
      animals=[
         LION_ITINERARY_ENTRY,
         CHEETAH_ITINERARY_ENTRY,
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   assert ItineraryCoordinator.bulk_schedule_animals().success

   result = schedule_itinerary_item(
      ScheduleItemKind.WILD_ENCOUNTER.item_type,
      wild_encounter_wire( BACTRIAN_CAMELS, start_time='15:30' ),
   )

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS
   assert result.itinerary is not None

   encounter = next(
      saved_encounter
      for saved_encounter in result.itinerary.wild_encounters
      if saved_encounter.name == BACTRIAN_CAMELS )
   scheduled_animals = [
      animal
      for animal in result.itinerary.animals
      if animal.start_time is not None and animal.end_time is not None
   ]

   assert scheduled_animals
   assert encounter.start_time == '3:30 PM'

   encounter_start_seconds = DateValues.time_value_in_seconds(
      encounter.start_time )
   latest_animal_end_seconds = max(
      DateValues.time_value_in_seconds( animal.end_time )
      for animal in scheduled_animals )
   earliest_animal_start_seconds = min(
      DateValues.time_value_in_seconds( animal.start_time )
      for animal in scheduled_animals )
   arrival_seconds = DateValues.time_value_in_seconds(
      result.itinerary.arrival_time )

   assert encounter_start_seconds is not None
   assert latest_animal_end_seconds is not None
   assert earliest_animal_start_seconds is not None
   assert arrival_seconds is not None

   assert latest_animal_end_seconds == encounter_start_seconds
   assert earliest_animal_start_seconds == arrival_seconds
   assert earliest_animal_start_seconds > DateValues.time_value_in_seconds(
      '12:00 PM' )

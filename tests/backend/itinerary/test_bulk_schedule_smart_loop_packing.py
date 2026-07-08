from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import CHEETAH_INDO_MALAYA_ITINERARY_ENTRY, wild_encounter_key
from wild_encounter_schedule_support import wire_schedule_row

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.shared.calendar_dates import DateValues
from api.shared.enums import ItineraryErrorType
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from conftest import DbControllers

DEMOISELLE_CRANE_ITINERARY_ENTRY = {
   'species': 'Demoiselle Crane',
   'exhibit': 'Australasia Pavilion',
}


def _set_giraffe_encounter_schedule( *, start_time: str = '11:00' ) -> None:
   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name='Masai Giraffe',
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=[
         wire_schedule_row(
            start_time,
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


def test_bulk_schedule_animals_places_south_loop_last_before_giraffe_encounter(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )
   _set_giraffe_encounter_schedule()

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      departure_time='17:00',
      animals=[
         DEMOISELLE_CRANE_ITINERARY_ENTRY,
         CHEETAH_INDO_MALAYA_ITINERARY_ENTRY,
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[
         wild_encounter_key( 'Masai Giraffe', start_time='11:00' ),
      ],
      confirming_early_admission=True,
   ).success

   result = ItineraryCoordinator.bulk_schedule_animals()

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS
   assert result.reasons == ()

   demoiselle_crane = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'Demoiselle Crane' )
   cheetah = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'Cheetah'
      and animal.exhibit == 'Indo-Malaya Outdoor' )

   encounter_start_seconds = DateValues.time_value_in_seconds( '11:00 AM' )
   demoiselle_end_seconds = DateValues.time_value_in_seconds(
      demoiselle_crane.end_time )
   cheetah_start_seconds = DateValues.time_value_in_seconds(
      cheetah.start_time )
   cheetah_end_seconds = DateValues.time_value_in_seconds( cheetah.end_time )

   assert encounter_start_seconds is not None
   assert demoiselle_end_seconds is not None
   assert cheetah_start_seconds is not None
   assert cheetah_end_seconds is not None

   assert demoiselle_end_seconds <= cheetah_start_seconds
   assert cheetah_end_seconds <= encounter_start_seconds
   assert cheetah_end_seconds == encounter_start_seconds


def test_bulk_schedule_animals_schedules_only_fitting_south_loop_in_short_pre_encounter_window(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )
   _set_giraffe_encounter_schedule( start_time='09:06' )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      departure_time='17:00',
      animals=[
         DEMOISELLE_CRANE_ITINERARY_ENTRY,
         CHEETAH_INDO_MALAYA_ITINERARY_ENTRY,
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[
         wild_encounter_key( 'Masai Giraffe', start_time='09:06' ),
      ],
      confirming_early_admission=True,
   ).success

   result = ItineraryCoordinator.bulk_schedule_animals()

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS
   assert result.reasons == ()

   demoiselle_crane = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'Demoiselle Crane' )
   cheetah = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'Cheetah'
      and animal.exhibit == 'Indo-Malaya Outdoor' )

   encounter_start_seconds = DateValues.time_value_in_seconds( '09:06 AM' )
   encounter_end_seconds = DateValues.time_value_in_seconds( '09:51 AM' )
   cheetah_end_seconds = DateValues.time_value_in_seconds( cheetah.end_time )
   demoiselle_start_seconds = DateValues.time_value_in_seconds(
      demoiselle_crane.start_time )

   assert encounter_start_seconds is not None
   assert encounter_end_seconds is not None
   assert cheetah_end_seconds is not None
   assert demoiselle_start_seconds is not None

   assert cheetah_end_seconds == encounter_start_seconds
   assert demoiselle_start_seconds >= encounter_end_seconds


def test_bulk_schedule_animals_packs_prefix_and_terminal_loops_before_giraffe_encounter(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )
   _set_giraffe_encounter_schedule( start_time='09:08' )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      departure_time='17:00',
      animals=[
         DEMOISELLE_CRANE_ITINERARY_ENTRY,
         CHEETAH_INDO_MALAYA_ITINERARY_ENTRY,
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[
         wild_encounter_key( 'Masai Giraffe', start_time='09:08' ),
      ],
      confirming_early_admission=True,
   ).success

   result = ItineraryCoordinator.bulk_schedule_animals()

   assert result.success
   assert result.reasons == ()

   demoiselle_crane = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'Demoiselle Crane' )
   cheetah = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'Cheetah'
      and animal.exhibit == 'Indo-Malaya Outdoor' )

   encounter_start_seconds = DateValues.time_value_in_seconds( '09:08 AM' )
   demoiselle_end_seconds = DateValues.time_value_in_seconds(
      demoiselle_crane.end_time )
   cheetah_end_seconds = DateValues.time_value_in_seconds( cheetah.end_time )

   assert encounter_start_seconds is not None
   assert demoiselle_end_seconds is not None
   assert cheetah_end_seconds is not None

   assert demoiselle_end_seconds <= DateValues.time_value_in_seconds(
      cheetah.start_time )
   assert cheetah_end_seconds == encounter_start_seconds

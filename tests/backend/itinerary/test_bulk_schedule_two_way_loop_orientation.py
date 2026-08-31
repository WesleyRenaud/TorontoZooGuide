from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.shared.calendar_dates import DateValues
from api.shared.enums import ItineraryErrorType
from conftest import DbControllers

GOLDEN_LION_TAMARIN_ITINERARY_ENTRY = {
   'species': 'Golden Lion Tamarin',
   'exhibit': 'Americas Pavilion',
   'enclosure_name': 'Outdoor',
}

CAPYBARA_TEMPLE_ITINERARY_ENTRY = {
   'species': 'Capybara',
   'exhibit': 'Americas Outdoor Mayan Temple Ruins',
}

HIGHLAND_CATTLE_ITINERARY_ENTRY = {
   'species': 'Highland Cattle',
   'exhibit': 'Eurasia Wilds',
}

WEST_CAUCASIAN_TUR_ITINERARY_ENTRY = {
   'species': 'West Caucasian Tur',
   'exhibit': 'Eurasia Wilds',
}

AMERICAS_PAVILION_TO_EURASIA_ITINERARY = [
   GOLDEN_LION_TAMARIN_ITINERARY_ENTRY,
   CAPYBARA_TEMPLE_ITINERARY_ENTRY,
   HIGHLAND_CATTLE_ITINERARY_ENTRY,
   WEST_CAUCASIAN_TUR_ITINERARY_ENTRY,
]


def test_bulk_schedule_itinerary_reverses_eurasia_loop_after_temple_for_shorter_walk(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      departure_time='17:00',
      animals=AMERICAS_PAVILION_TO_EURASIA_ITINERARY,
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   result = ItineraryCoordinator.bulk_schedule_itinerary()

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS
   assert result.reasons == []

   tamarin = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'Golden Lion Tamarin' )
   capybara = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'Capybara' )
   cattle = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'Highland Cattle' )
   tur = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'West Caucasian Tur' )

   tamarin_end_seconds = DateValues.time_value_in_seconds( tamarin.end_time )
   capybara_start_seconds = DateValues.time_value_in_seconds( capybara.start_time )
   capybara_end_seconds = DateValues.time_value_in_seconds( capybara.end_time )
   tur_start_seconds = DateValues.time_value_in_seconds( tur.start_time )
   tur_end_seconds = DateValues.time_value_in_seconds( tur.end_time )
   cattle_start_seconds = DateValues.time_value_in_seconds( cattle.start_time )

   assert tamarin_end_seconds is not None
   assert capybara_start_seconds is not None
   assert capybara_end_seconds is not None
   assert tur_start_seconds is not None
   assert tur_end_seconds is not None
   assert cattle_start_seconds is not None

   assert tamarin_end_seconds <= capybara_start_seconds
   assert capybara_end_seconds <= tur_start_seconds
   assert tur_end_seconds <= cattle_start_seconds
   assert tur_start_seconds < cattle_start_seconds

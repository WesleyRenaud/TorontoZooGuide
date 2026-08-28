from __future__ import annotations

from test_animal_viewability_logic import make_animal_viewability_record

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.animals.domain.itinerary_animal_records_filter_builder import ItineraryAnimalRecordsFilterBuilder
from api.shared.constants import Constants
from conftest import DbControllers


def test_filter_animal_records_for_itinerary_excludes_zoomobile_only() -> None:
   records = [
      make_animal_viewability_record(
         species='Asian Wild Horse',
         exhibit='Eurasia Wilds',
         enclosure_name='Shady Acres',
         enclosure_type='Outdoor',
         x_coord=1.0,
         y_coord=1.0,
         animal_day_seasonal_multiplier=1.0,
         exhibit_day_seasonal_availability_multiplier=1.0,
         is_zoomobile_only=False ),
      make_animal_viewability_record(
         species='Asian Wild Horse',
         exhibit='Eurasia Wilds',
         enclosure_name='Eurasia Drive Thru',
         enclosure_type='Outdoor',
         x_coord=2.0,
         y_coord=2.0,
         animal_day_seasonal_multiplier=1.0,
         exhibit_day_seasonal_availability_multiplier=1.0,
         is_zoomobile_only=True ),
   ]

   filtered = ItineraryAnimalRecordsFilterBuilder.filter( records )

   assert [
      ( record.species, record.enclosure_name )
      for record in filtered
   ] == [
      ( 'Asian Wild Horse', 'Shady Acres' ),
   ]


def test_get_animals_viewable_on_day_excludes_seeded_zoomobile_only_viewings(
      db: DbControllers ) -> None:
   map_animals = AnimalCoordinator.get_animals_viewable_on_day(
      day=15,
      month='June',
      year=2026,
      temp=22,
      for_itinerary=False )
   itinerary_animals = AnimalCoordinator.get_animals_viewable_on_day(
      day=15,
      month='June',
      year=2026,
      temp=22,
      for_itinerary=True,
      threshold=Constants.ITINERARY_ANIMAL_MIN_LIKELIHOOD )

   map_keys = {
      ( animal.species, animal.enclosure_name )
      for animal in map_animals
   }
   itinerary_keys = {
      ( animal.species, animal.enclosure_name )
      for animal in itinerary_animals
   }

   assert ( 'Domestic Yak', 'Eurasia Drive Thru' ) in map_keys
   assert ( 'Asian Wild Horse', 'Eurasia Drive Thru' ) in map_keys
   assert ( 'West Caucasian Tur', 'Zoomobile Habitat' ) in map_keys

   assert ( 'Domestic Yak', 'Eurasia Drive Thru' ) not in itinerary_keys
   assert ( 'Asian Wild Horse', 'Eurasia Drive Thru' ) not in itinerary_keys
   assert ( 'West Caucasian Tur', 'Zoomobile Habitat' ) not in itinerary_keys
   assert ( 'Asian Wild Horse', 'Shady Acres' ) in itinerary_keys


def test_include_off_display_animals_includes_below_min_likelihood(
      db: DbControllers ) -> None:
   without_off_display = AnimalCoordinator.get_animals_viewable_on_day(
      day=31,
      month='October',
      year=2026,
      temp=12,
      for_itinerary=True,
      threshold=Constants.ITINERARY_ANIMAL_MIN_LIKELIHOOD,
      exhibits_to_include=[ 'Africa Savanna' ] )
   with_off_display = AnimalCoordinator.get_animals_viewable_on_day(
      day=31,
      month='October',
      year=2026,
      temp=12,
      for_itinerary=True,
      threshold=Constants.ITINERARY_ANIMAL_MIN_LIKELIHOOD,
      include_off_display_animals=True,
      exhibits_to_include=[ 'Africa Savanna' ] )

   without_species = { animal.species for animal in without_off_display }
   with_species = { animal.species for animal in with_off_display }
   below_min = {
      animal.species
      for animal in with_off_display
      if animal.likelihood < Constants.ITINERARY_ANIMAL_MIN_LIKELIHOOD
   }

   assert 'Warthog' not in without_species
   assert 'Warthog' in with_species
   assert below_min
   assert all(
      animal.likelihood >= Constants.ITINERARY_ANIMAL_MIN_LIKELIHOOD
      for animal in without_off_display
   )

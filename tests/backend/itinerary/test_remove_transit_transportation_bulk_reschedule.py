from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import itinerary_animals_for_exhibits
from itinerary.support import remove_itinerary_item

from api.exhibits.coordinators.exhibit_coordinator import ExhibitCoordinator
from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.data_access.itinerary_transportation_input import ItineraryTransportationInput
from api.shared.calendar_dates import DateValues
from conftest import DbControllers

VISIT_DATE = '2026-07-11'
VISIT_DAY = date( 2026, 7, 11 )
ZOOMOBILE = 'Zoomobile'


def _selected_exhibits_for_regions( region_names: list[ str ] ) -> list[ str ]:
   selected_exhibits: list[ str ] = []

   for region in ExhibitCoordinator.get_regions_with_exhibits():
      if region.name in region_names:
         selected_exhibits.extend( region.exhibits )

   assert selected_exhibits
   return selected_exhibits


def _seconds( time_key: str | None ) -> int:
   value = DateValues.time_value_in_seconds( time_key )
   assert value is not None
   return value


def test_remove_transit_zoomobile_bulk_reschedules_without_rides(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( VISIT_DAY )
   selected_exhibits = _selected_exhibits_for_regions( [ 'Canadian Domain' ] )

   assert ItineraryCoordinator.set_itinerary(
      date=VISIT_DATE,
      arrival_time='09:00',
      departure_time='18:00',
      animals=itinerary_animals_for_exhibits(
         selected_exhibits,
         visit_date=VISIT_DATE ),
      attractions=[],
      transportations=[
         ItineraryTransportationInput(
            name=ZOOMOBILE,
            added_as_attraction=False ),
      ],
      guardians_talks=[],
      wild_encounters=[],
      selected_exhibits=selected_exhibits,
      confirming_early_admission=True,
   ).success

   assert ItineraryCoordinator.bulk_schedule_animals().success

   itinerary_before = ItineraryCoordinator.get_itinerary()
   transit_before = next(
      transportation
      for transportation in itinerary_before.transportations
      if not transportation.added_as_attraction )
   scheduled_animals_before = [
      animal
      for animal in itinerary_before.animals
      if animal.start_time and animal.end_time
   ]

   assert transit_before.legs
   assert scheduled_animals_before
   animal_start_before = {
      ( animal.species, animal.exhibit ): _seconds( animal.start_time )
      for animal in scheduled_animals_before
   }

   assert remove_itinerary_item(
      'transportations',
      f'{ ZOOMOBILE }||0' ).success

   itinerary_after = ItineraryCoordinator.get_itinerary()

   assert all(
      transportation.name != ZOOMOBILE
      or transportation.added_as_attraction
      for transportation in itinerary_after.transportations
   )

   scheduled_animals_after = [
      animal
      for animal in itinerary_after.animals
      if animal.start_time and animal.end_time
   ]

   assert {
      ( animal.species, animal.exhibit )
      for animal in scheduled_animals_after
   } == {
      ( animal.species, animal.exhibit )
      for animal in scheduled_animals_before
   }
   assert any(
      _seconds( animal.start_time )
      != animal_start_before[ ( animal.species, animal.exhibit ) ]
      for animal in scheduled_animals_after
   )


def test_remove_attraction_zoomobile_keeps_transit_rides(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( VISIT_DAY )
   selected_exhibits = _selected_exhibits_for_regions( [ 'Canadian Domain' ] )

   assert ItineraryCoordinator.set_itinerary(
      date=VISIT_DATE,
      arrival_time='09:00',
      departure_time='18:00',
      animals=itinerary_animals_for_exhibits(
         selected_exhibits,
         visit_date=VISIT_DATE ),
      attractions=[],
      transportations=[
         ItineraryTransportationInput(
            name=ZOOMOBILE,
            added_as_attraction=True ),
         ItineraryTransportationInput(
            name=ZOOMOBILE,
            added_as_attraction=False ),
      ],
      guardians_talks=[],
      wild_encounters=[],
      selected_exhibits=selected_exhibits,
      confirming_early_admission=True,
   ).success

   assert ItineraryCoordinator.bulk_schedule_animals().success

   transit_before = next(
      transportation
      for transportation in ItineraryCoordinator.get_itinerary().transportations
      if not transportation.added_as_attraction )
   transit_board_alight_before = [
      ( leg.from_station, leg.to_station )
      for leg in transit_before.legs
   ]

   assert remove_itinerary_item( 'attractions', ZOOMOBILE ).success

   transit_after = next(
      transportation
      for transportation in ItineraryCoordinator.get_itinerary().transportations
      if not transportation.added_as_attraction )

   assert [
      ( leg.from_station, leg.to_station )
      for leg in transit_after.legs
   ] == transit_board_alight_before

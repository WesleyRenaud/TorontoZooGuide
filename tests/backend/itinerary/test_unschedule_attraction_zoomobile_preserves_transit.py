from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import itinerary_animals_for_exhibits
from itinerary.support import unschedule_itinerary_item

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


def test_unschedule_attraction_zoomobile_preserves_transit_ride_legs(
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

   itinerary_before = ItineraryCoordinator.get_itinerary()
   attraction_before = next(
      transportation
      for transportation in itinerary_before.transportations
      if transportation.added_as_attraction )
   transit_before = next(
      transportation
      for transportation in itinerary_before.transportations
      if not transportation.added_as_attraction )

   assert attraction_before.start_time is not None
   assert attraction_before.end_time is not None
   assert transit_before.bulk_transit_evaluated is True
   assert transit_before.legs
   transit_board_alight_before = [
      ( leg.from_station, leg.to_station )
      for leg in transit_before.legs
   ]
   attraction_duration_seconds = (
      _seconds( attraction_before.end_time )
      - _seconds( attraction_before.start_time )
   )

   assert unschedule_itinerary_item( 'attractions', ZOOMOBILE ).success

   itinerary_after = ItineraryCoordinator.get_itinerary()
   attraction_after = next(
      transportation
      for transportation in itinerary_after.transportations
      if transportation.added_as_attraction )
   transit_after = next(
      transportation
      for transportation in itinerary_after.transportations
      if not transportation.added_as_attraction )

   assert attraction_after.start_time is None
   assert attraction_after.end_time is None
   assert attraction_after.legs == []
   assert transit_after.bulk_transit_evaluated is True
   assert [
      ( leg.from_station, leg.to_station )
      for leg in transit_after.legs
   ] == transit_board_alight_before
   assert len( transit_after.legs ) == len( transit_before.legs )

   for before_leg, after_leg in zip(
         transit_before.legs,
         transit_after.legs ):
      assert _seconds( after_leg.start_time ) == (
         _seconds( before_leg.start_time ) - attraction_duration_seconds )
      assert _seconds( after_leg.end_time ) == (
         _seconds( before_leg.end_time ) - attraction_duration_seconds )


def test_unschedule_attraction_zoomobile_via_transportation_key_preserves_transit(
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

   assert unschedule_itinerary_item(
      'transportations',
      f'{ ZOOMOBILE }||1' ).success

   transit_after = next(
      transportation
      for transportation in ItineraryCoordinator.get_itinerary().transportations
      if not transportation.added_as_attraction )

   assert transit_after.bulk_transit_evaluated is True
   assert [
      ( leg.from_station, leg.to_station )
      for leg in transit_after.legs
   ] == transit_board_alight_before

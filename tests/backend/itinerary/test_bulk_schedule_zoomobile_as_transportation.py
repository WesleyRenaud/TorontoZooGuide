from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import itinerary_animals_for_exhibits
import pytest

from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.exhibits.coordinators.exhibit_coordinator import ExhibitCoordinator
from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.data_access.itinerary_transportation_input import ItineraryTransportationInput
from api.itinerary.domain.itinerary_transportation_stations import group_consecutive_transportation_leg_sequences
from api.models import Itinerary
from api.models.animal import Animal
from api.models.itinerary_transportation import ItineraryTransportation
from api.models.itinerary_transportation_leg import ItineraryTransportationLeg
from api.shared.calendar_dates import DateValues
from conftest import DbControllers

VISIT_DATE = '2026-07-11'
VISIT_DAY = date( 2026, 7, 11 )

MAIN = 'Main Zoomobile Station'
DOMAIN = 'Canadian Domain Zoomobile Station'
AFRICA = 'Africa Zoomobile Station'
TUNDRA = 'Tundra Zoomobile Station'


def _selected_exhibits_for_regions( region_names: list[ str ] ) -> list[ str ]:
   selected_exhibits: list[ str ] = []

   for region in ExhibitCoordinator.get_regions_with_exhibits():
      if region.name in region_names:
         selected_exhibits.extend( region.exhibits )

   assert selected_exhibits

   return selected_exhibits


def _save_transit_zoomobile_itinerary( *, region_names: list[ str ] ) -> None:
   selected_exhibits = _selected_exhibits_for_regions( region_names )
   save = ItineraryCoordinator.set_itinerary(
      date=VISIT_DATE,
      arrival_time='09:00',
      departure_time='18:00',
      animals=itinerary_animals_for_exhibits(
         selected_exhibits,
         visit_date=VISIT_DATE ),
      attractions=[],
      transportations=[
         ItineraryTransportationInput(
            name='Zoomobile',
            added_as_attraction=False ),
      ],
      guardians_talks=[],
      wild_encounters=[],
      selected_exhibits=selected_exhibits,
      confirming_early_admission=True,
   )

   assert save.success


def _transit_zoomobile( itinerary: Itinerary ) -> ItineraryTransportation:
   return next(
      transportation
      for transportation in itinerary.transportations
      if (
            transportation.name == 'Zoomobile'
            and transportation.added_as_attraction is False
      )
   )


def _ride_board_alight_pairs(
      legs: list[ ItineraryTransportationLeg ],
) -> list[ tuple[ str, str ] ]:
   return [
      ( sequence[ 0 ].from_station, sequence[ -1 ].to_station )
      for sequence in group_consecutive_transportation_leg_sequences( legs )
   ]


def _seconds( time_key: str | None ) -> int:
   value = DateValues.time_value_in_seconds( time_key )
   assert value is not None

   return value


def _zoomobile_hours_payload(
      *,
      weekday_start: str,
      weekday_end: str,
      weekend_start: str,
      weekend_end: str,
) -> dict:
   return {
      'attraction': 'Zoomobile',
      'start_date': '2026-07-01',
      'end_date': '2026-07-31',
      'weekday_start_time': weekday_start,
      'weekday_end_time': weekday_end,
      'weekend_holiday_start_time': weekend_start,
      'weekend_holiday_end_time': weekend_end,
   }


def _scheduled_animals_in_regions(
      itinerary: Itinerary,
      region_names: set[ str ],
) -> list[ Animal ]:
   exhibits = set( _selected_exhibits_for_regions( list( region_names ) ) )

   return [
      animal
      for animal in itinerary.animals
      if (
            animal.exhibit in exhibits
            and animal.start_time is not None
            and animal.end_time is not None
      )
   ]


def _assert_animals_between_rides(
      animals: list[ Animal ],
      *,
      after_ride_end: str,
      before_ride_start: str | None ) -> None:
   assert animals
   after_seconds = _seconds( after_ride_end )
   before_seconds = (
      None
      if before_ride_start is None
      else _seconds( before_ride_start )
   )

   for animal in animals:
      assert _seconds( animal.start_time ) >= after_seconds

      if before_seconds is not None:
         assert _seconds( animal.end_time ) <= before_seconds


def test_bulk_schedule_domain_only_uses_zoomobile_to_cut_long_walk(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( VISIT_DAY )
   _save_transit_zoomobile_itinerary( region_names=[ 'Canadian Domain' ] )

   result = ItineraryCoordinator.bulk_schedule_itinerary()

   assert result.success
   assert result.itinerary is not None
   assert _seconds( result.itinerary.arrival_time ) >= _seconds( '9:00 AM' )

   zoomobile = _transit_zoomobile( result.itinerary )
   rides = _ride_board_alight_pairs( zoomobile.legs )
   assert zoomobile.bulk_transit_evaluated is True
   assert len( rides ) >= 1
   assert rides[ 0 ][ 0 ] == MAIN
   assert rides[ 0 ][ 1 ] in { DOMAIN, AFRICA }
   assert rides[ -1 ][ 1 ] == MAIN
   assert rides[ -1 ][ 0 ] in { DOMAIN, AFRICA, TUNDRA }

   sequences = group_consecutive_transportation_leg_sequences( zoomobile.legs )
   domain_animals = _scheduled_animals_in_regions(
      result.itinerary,
      { 'Canadian Domain' } )

   if len( sequences ) >= 2:
      _assert_animals_between_rides(
         domain_animals,
         after_ride_end=sequences[ 0 ][ -1 ].end_time,
         before_ride_start=sequences[ -1 ][ 0 ].start_time )
   else:
      assert domain_animals
      assert _seconds( domain_animals[ 0 ].start_time ) >= _seconds(
         sequences[ 0 ][ -1 ].end_time )


def test_departure_after_return_to_main_uses_alighting_station_walk(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( VISIT_DAY )
   _save_transit_zoomobile_itinerary( region_names=[ 'Canadian Domain' ] )

   result = ItineraryCoordinator.bulk_schedule_itinerary()

   assert result.success
   assert result.itinerary is not None

   zoomobile = _transit_zoomobile( result.itinerary )
   assert _ride_board_alight_pairs( zoomobile.legs )[ -1 ][ 1 ] == MAIN
   assert zoomobile.end_time == result.itinerary.departure_time or (
      _seconds( result.itinerary.departure_time )
      - _seconds( zoomobile.end_time )
   ) <= 5 * 60
   # Boarding-station walk from Eurasia/Domain would pad ~15–20+ minutes.
   assert (
      _seconds( result.itinerary.departure_time )
      - _seconds( zoomobile.end_time )
   ) < 10 * 60


def test_bulk_schedule_zoomobile_does_not_pull_arrival_before_zoo_open(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( VISIT_DAY )
   selected_exhibits = _selected_exhibits_for_regions( [ 'Canadian Domain' ] )
   save = ItineraryCoordinator.set_itinerary(
      date=VISIT_DATE,
      arrival_time='09:30',
      departure_time='18:00',
      animals=itinerary_animals_for_exhibits(
         selected_exhibits,
         visit_date=VISIT_DATE ),
      attractions=[],
      transportations=[
         ItineraryTransportationInput(
            name='Zoomobile',
            added_as_attraction=False ),
      ],
      guardians_talks=[],
      wild_encounters=[],
      selected_exhibits=selected_exhibits,
   )

   assert save.success

   result = ItineraryCoordinator.bulk_schedule_itinerary()

   assert result.success
   assert result.itinerary is not None
   assert _seconds( result.itinerary.arrival_time ) >= _seconds( '9:30 AM' )
   assert _seconds( _transit_zoomobile( result.itinerary ).start_time ) >= (
      _seconds( result.itinerary.arrival_time ) )


def test_bulk_schedule_domain_and_tundra_inserts_rides_for_long_transfers(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( VISIT_DAY )
   _save_transit_zoomobile_itinerary(
      region_names=[ 'Canadian Domain', 'Tundra Trek' ] )

   result = ItineraryCoordinator.bulk_schedule_itinerary()

   assert result.success
   assert result.itinerary is not None

   zoomobile = _transit_zoomobile( result.itinerary )
   rides = _ride_board_alight_pairs( zoomobile.legs )
   assert len( rides ) >= 1
   assert any(
      { board, alight } & { MAIN, DOMAIN, AFRICA, TUNDRA }
      for board, alight in rides
   )

   domain_animals = _scheduled_animals_in_regions(
      result.itinerary,
      { 'Canadian Domain' } )
   tundra_animals = _scheduled_animals_in_regions(
      result.itinerary,
      { 'Tundra Trek' } )
   assert domain_animals
   assert tundra_animals


def test_bulk_schedule_africa_and_domain_rides_into_south_cluster(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( VISIT_DAY )
   _save_transit_zoomobile_itinerary(
      region_names=[ 'Africa', 'Canadian Domain' ] )

   result = ItineraryCoordinator.bulk_schedule_itinerary()

   assert result.success
   assert result.itinerary is not None

   south_animals = _scheduled_animals_in_regions(
      result.itinerary,
      { 'Africa', 'Canadian Domain' } )
   assert south_animals

   zoomobile = _transit_zoomobile( result.itinerary )
   rides = _ride_board_alight_pairs( zoomobile.legs )

   if rides:
      assert any(
         { board, alight } & { MAIN, DOMAIN, AFRICA }
         for board, alight in rides
      )


def test_bulk_schedule_multi_region_uses_zoomobile_for_long_hops(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( VISIT_DAY )
   _save_transit_zoomobile_itinerary(
      region_names=[
         'Indo-Malaya',
         'Africa',
         'Australasia',
         'Eurasia Wilds',
         'Tundra Trek',
      ] )

   result = ItineraryCoordinator.bulk_schedule_itinerary()

   assert result.success
   assert result.itinerary is not None

   zoomobile = _transit_zoomobile( result.itinerary )
   rides = _ride_board_alight_pairs( zoomobile.legs )
   assert len( rides ) >= 1
   assert any(
      { board, alight } & { MAIN, AFRICA, DOMAIN, TUNDRA }
      for board, alight in rides
   )

   north_animals = _scheduled_animals_in_regions(
      result.itinerary,
      { 'Australasia', 'Eurasia Wilds', 'Tundra Trek' } )
   south_animals = _scheduled_animals_in_regions(
      result.itinerary,
      { 'Indo-Malaya', 'Africa' } )
   assert north_animals
   assert south_animals

   tundra_start = min(
      _seconds( animal.start_time )
      for animal in _scheduled_animals_in_regions(
         result.itinerary,
         { 'Tundra Trek' } )
   )
   australasia_start = min(
      _seconds( animal.start_time )
      for animal in _scheduled_animals_in_regions(
         result.itinerary,
         { 'Australasia' } )
   )
   eurasia_start = min(
      _seconds( animal.start_time )
      for animal in _scheduled_animals_in_regions(
         result.itinerary,
         { 'Eurasia Wilds' } )
   )
   assert tundra_start < australasia_start < eurasia_start

   # With North packed Tundra → Australasia → Eurasia, transfers should not need
   # a near-full-loop ride (the failure mode before the cluster reorder).
   assert not any(
      board == 'Eurasia Zoomobile Station' and alight == TUNDRA
      for board, alight in rides
   )


def test_bulk_schedule_marks_transit_zoomobile_evaluated_when_no_rides_used(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ],
      monkeypatch: pytest.MonkeyPatch,
) -> None:
   freeze_database_today( VISIT_DAY )
   _save_transit_zoomobile_itinerary( region_names=[ 'Canadian Domain' ] )

   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.transportation_transit_rides._plan_rides_for_anchors',
      lambda **_kwargs: ( [], None ),
   )

   result = ItineraryCoordinator.bulk_schedule_itinerary()

   assert result.success
   assert result.itinerary is not None

   zoomobile = _transit_zoomobile( result.itinerary )

   assert zoomobile.legs == []
   assert zoomobile.bulk_transit_evaluated is True


def test_bulk_schedule_transit_zoomobile_respects_configured_operating_hours(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   freeze_database_today( VISIT_DAY )

   assert AttractionCoordinator.replace_attraction_hours_schedule_overlaps(
      **_zoomobile_hours_payload(
         weekday_start='10:00 AM',
         weekday_end='6:00 PM',
         weekend_start='10:00 AM',
         weekend_end='6:00 PM' ) )

   _save_transit_zoomobile_itinerary( region_names=[ 'Canadian Domain' ] )

   result = ItineraryCoordinator.bulk_schedule_itinerary()

   assert result.success
   assert result.itinerary is not None

   zoomobile = _transit_zoomobile( result.itinerary )
   open_seconds = _seconds( '10:00 AM' )
   close_seconds = _seconds( '6:00 PM' )

   assert zoomobile.bulk_transit_evaluated is True

   for leg in zoomobile.legs:
      leg_start = _seconds( leg.start_time )
      leg_end = _seconds( leg.end_time )
      assert leg_start >= open_seconds
      assert leg_end <= close_seconds

   if zoomobile.legs:
      assert _seconds( zoomobile.legs[ 0 ].start_time ) >= open_seconds


def test_bulk_schedule_transit_zoomobile_starts_after_attraction_mode_trip(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( VISIT_DAY )
   selected_exhibits = _selected_exhibits_for_regions( [ 'Canadian Domain' ] )

   save = ItineraryCoordinator.set_itinerary(
      date=VISIT_DATE,
      arrival_time='09:00',
      departure_time='18:00',
      animals=itinerary_animals_for_exhibits(
         selected_exhibits,
         visit_date=VISIT_DATE ),
      attractions=[],
      transportations=[
         ItineraryTransportationInput(
            name='Zoomobile',
            added_as_attraction=True ),
         ItineraryTransportationInput(
            name='Zoomobile',
            added_as_attraction=False ),
      ],
      guardians_talks=[],
      wild_encounters=[],
      selected_exhibits=selected_exhibits,
      confirming_early_admission=True,
   )

   assert save.success

   result = ItineraryCoordinator.bulk_schedule_itinerary()

   assert result.success
   assert result.itinerary is not None

   attraction_zoomobile = next(
      transportation
      for transportation in result.itinerary.transportations
      if (
            transportation.name == 'Zoomobile'
            and transportation.added_as_attraction is True
      )
   )
   transit_zoomobile = _transit_zoomobile( result.itinerary )

   assert attraction_zoomobile.start_time is not None
   assert attraction_zoomobile.end_time is not None
   assert attraction_zoomobile.legs
   assert transit_zoomobile.bulk_transit_evaluated is True
   assert transit_zoomobile.legs

   attraction_end = _seconds( attraction_zoomobile.end_time )

   for leg in transit_zoomobile.legs:
      assert _seconds( leg.start_time ) >= attraction_end

   transit_rides = _ride_board_alight_pairs( transit_zoomobile.legs )
   assert any(
      DOMAIN in { board, alight }
      for board, alight in transit_rides
   )

from __future__ import annotations

from collections.abc import Callable
from datetime import date, datetime

import pytest

from api.animals.controllers.animal_controller import AnimalController
from api.animals.data_access.animal_viewability_record import AnimalViewabilityRecord
from api.animals.logic.animal_viewability import calculate_animal_likelihood
from api.animals.logic.animal_viewability import get_active_exhibit_status
from api.animals.logic.animal_viewability import get_active_limited_viewing_status
from api.animals.logic.animal_viewability import get_active_off_display_status
from api.animals.logic.animal_viewability import get_active_viewing_alert_status
from api.attractions.logic.attraction import calculate_attraction_likelihood
from api.giftshops.logic.gift_shop import calculate_gift_shop_likelihood
from api.restaurants.logic.restaurant import calculate_restaurant_likelihood
from api.shared.date_values import DateValues
from api.shared.enums import ScheduleStatus
from api.types import DateInput, DateKey, SeasonalMultiplier
from conftest import DbControllers


def make_animal_viewability_record( **overrides: object ) -> AnimalViewabilityRecord:
   values: dict[ str, object ] = {
      'species': None,
      'latin_name': None,
      'min_temperature': None,
      'general_viewing_tips': None,
      'seasonal_viewing_tips': None,
      'identification': None,
      'habitat_and_range': None,
      'diet_and_feeding': None,
      'behaviour_and_social_life': None,
      'adaptations': None,
      'reproduction_and_life_cycle': None,
      'animals_at_the_zoo': None,
      'exhibit': None,
      'seasonal_viewing_summary': None,
      'seasonal_viewing_information': None,
      'enclosure_type': None,
      'seasonally_off_display_message': None,
      'x_coord': None,
      'y_coord': None,
      'is_off_display': None,
      'viewing_scope': None,
      'off_display_message': None,
      'off_display_start': None,
      'off_display_end': None,
      'schedule_start_date': None,
      'schedule_end_date': None,
      'daily_start_time': None,
      'daily_end_time': None,
      'viewing_message': None,
      'alert_message': None,
      'alert_start_date': None,
      'alert_end_date': None,
      'is_closed': None,
      'closed_message': None,
      'closed_start': None,
      'closed_end': None,
      'animal_day_seasonal_multiplier': None,
      'exhibit_day_seasonal_availability_multiplier': None,
   }
   values.update( overrides )

   return AnimalViewabilityRecord( **values )


def test_database_uses_injected_path( db: DbControllers ) -> None:
   assert AnimalController.get_animal_species_names()


def test_close_is_idempotent( db: DbControllers ) -> None:
   db.close()
   db.close()

   assert db.conn is None


@pytest.mark.parametrize(
   'value, expected',
   [
      ( None, None ),
      ( date( 2026, 6, 15 ), date( 2026, 6, 15 ) ),
      ( datetime( 2026, 6, 15, 9, 30 ), date( 2026, 6, 15 ) ),
      ( '2026-06-15', date( 2026, 6, 15 ) ),
      ( '2026-06-15 09:30', date( 2026, 6, 15 ) )
   ]
)
def test_parse_date_value( value: DateInput, expected: date | None ) -> None:
   assert DateValues.parse_date_value( value ) == expected


@pytest.mark.parametrize(
   'value, expected',
   [
      ( None, None ),
      ( '', None ),
      ( '  ', None ),
      ( '2026-06-15', '2026-06-15' ),
      ( date( 2026, 6, 15 ), '2026-06-15' ),
      ( datetime( 2026, 6, 15, 9, 30 ), '2026-06-15' ),
   ]
)
def test_normalize_date_key( value: DateInput, expected: DateKey | None ) -> None:
   assert DateValues.normalize_date_key( value ) == expected


def test_normalize_date_key_returns_none_for_unsupported_date_strings() -> None:
   assert DateValues.normalize_date_key( 'June 15, 2026' ) is None


def test_resolve_open_ended_date_range_keeps_open_end_date() -> None:
   date_range = DateValues.resolve_open_ended_date_range(
      start_date='2026-06-01',
      end_date=None )

   assert date_range.start_date == '2026-06-01'
   assert date_range.end_date is None


def test_resolve_open_ended_date_range_uses_today_for_missing_start(
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   date_range = DateValues.resolve_open_ended_date_range(
      start_date=None,
      end_date=None )

   assert date_range.start_date == '2026-06-15'
   assert date_range.end_date is None


@pytest.mark.parametrize(
   'value, expected',
   [
      ( None, None ),
      ( '2026-06-15 09:30 AM', datetime( 2026, 6, 15, 9, 30 ) ),
      ( '2026-06-15 17:45:00', datetime( 2026, 6, 15, 17, 45 ) ),
      ( '2026-06-15 17:45', datetime( 2026, 6, 15, 17, 45 ) )
   ]
)
def test_parse_datetime_value( value: str | None, expected: datetime | None ) -> None:
   assert DateValues.parse_datetime_value( value ) == expected


def test_parse_values_raise_for_unsupported_formats() -> None:
   with pytest.raises( ValueError ):
      DateValues.parse_date_value( 'June 15, 2026' )

   with pytest.raises( ValueError ):
      DateValues.parse_datetime_value( 'June 15, 2026 9:30' )


@pytest.mark.parametrize(
   'value, expected',
   [
      ( None, None ),
      ( '', None ),
      ( '   ', None ),
      ( '1:00 PM', '13:00' ),
      ( '13:45', '13:45' ),
      ( '10:00', '10:00' ),
   ]
)
def test_normalize_itinerary_schedule_time(
      value: str | None,
      expected: str | None ) -> None:
   assert DateValues.normalize_itinerary_schedule_time( value ) == expected


@pytest.mark.parametrize(
   'left, right, expected',
   [
      ( date( 2026, 6, 15 ), None, True ),
      ( date( 2026, 6, 15 ), '2026-06-15', True ),
      ( date( 2026, 6, 14 ), '2026-06-15', False ),
      ( date( 2026, 6, 16 ), '2026-06-14', True ),
   ]
)
def test_is_date_on_or_after( left: date, right: DateInput, expected: bool ) -> None:
   assert DateValues.is_date_on_or_after( left, right ) is expected


@pytest.mark.parametrize(
   'left, right, expected',
   [
      ( date( 2026, 6, 15 ), None, True ),
      ( date( 2026, 6, 15 ), '2026-06-15', True ),
      ( date( 2026, 6, 16 ), '2026-06-15', False ),
      ( date( 2026, 6, 14 ), '2026-06-14', True ),
   ]
)
def test_is_date_on_or_before( left: date, right: DateInput, expected: bool ) -> None:
   assert DateValues.is_date_on_or_before( left, right ) is expected


@pytest.mark.parametrize(
   'target, start, end, expected',
   [
      ( date( 2026, 6, 15 ), None, None, True ),
      ( date( 2026, 6, 15 ), '2026-06-15', '2026-06-15', True ),
      ( date( 2026, 6, 14 ), '2026-06-15', None, False ),
      ( date( 2026, 6, 16 ), None, '2026-06-15', False )
   ]
)
def test_is_date_in_range(
      target: date,
      start: DateInput,
      end: DateInput,
      expected: bool ) -> None:
   assert DateValues.is_date_in_range( target_date=target, start_date_value=start, end_date_value=end ) is expected


LikelihoodCalculator = Callable[ [ SeasonalMultiplier ], int ]


@pytest.mark.parametrize(
   'calculate_likelihood',
   [
      calculate_restaurant_likelihood,
      calculate_gift_shop_likelihood,
      calculate_attraction_likelihood
   ]
)
def test_simple_likelihood_calculators_clamp_and_round(
      calculate_likelihood: LikelihoodCalculator ) -> None:
   assert calculate_likelihood( None ) == 100
   assert calculate_likelihood( -0.5 ) == 0
   assert calculate_likelihood( 0.444 ) == 44
   assert calculate_likelihood( 1.5 ) == 100


def test_calculate_animal_likelihood_handles_indoor_and_outdoor_inputs() -> None:
   assert calculate_animal_likelihood(
      temp=-20,
      sigma=2,
      enclosure_type='indoor',
      min_temperature=30,
      day_seasonal_multiplier=0,
      exhibit_day_seasonal_availability_multiplier=1
   ) == 100

   assert calculate_animal_likelihood(
      temp=-20,
      sigma=2,
      enclosure_type='indoor',
      min_temperature=30,
      day_seasonal_multiplier=0,
      exhibit_day_seasonal_availability_multiplier=0
   ) == 0

   assert calculate_animal_likelihood(
      temp=20,
      sigma=2,
      enclosure_type='Outdoor',
      min_temperature=20,
      day_seasonal_multiplier=0.5,
      exhibit_day_seasonal_availability_multiplier=0.5
   ) == 12

   assert calculate_animal_likelihood(
      temp=None,
      sigma=2,
      enclosure_type='Outdoor',
      min_temperature=None,
      day_seasonal_multiplier=None,
      exhibit_day_seasonal_availability_multiplier=None
   ) == 100


def test_active_status_helpers() -> None:
   active_record = make_animal_viewability_record(
      is_off_display=1,
      off_display_message='Temporarily hidden.',
      off_display_start='2026-06-01',
      off_display_end='2026-06-30',
      schedule_start_date='2026-06-01',
      schedule_end_date='2026-06-30',
      daily_start_time='09:00',
      daily_end_time='11:00',
      viewing_message='Morning only.',
      alert_message='Low visibility.',
      alert_start_date='2026-06-01',
      alert_end_date='2026-06-30',
      is_closed=1,
      closed_message='Closed.',
      closed_start='2026-06-01',
      closed_end='2026-06-30' )
   target_date = date( 2026, 6, 15 )

   assert get_active_off_display_status( active_record, target_date ) == ( True, 'Temporarily hidden.' )
   assert get_active_limited_viewing_status( active_record, target_date ) == ( True, 'Morning only.' )
   assert get_active_viewing_alert_status( active_record, target_date ) == ( True, 'Low visibility.' )
   assert get_active_exhibit_status( active_record, target_date ) == ( ScheduleStatus.CLOSED, 'Closed.' )


def test_active_status_helpers_return_inactive_defaults() -> None:
   inactive_record = make_animal_viewability_record(
      is_off_display=0,
      off_display_message='Temporarily hidden.',
      off_display_start='2026-06-01',
      off_display_end='2026-06-30',
      schedule_start_date='2026-06-01',
      schedule_end_date='2026-06-30',
      daily_start_time=None,
      daily_end_time='11:00',
      viewing_message='Morning only.',
      alert_message=None,
      alert_start_date='2026-06-01',
      alert_end_date='2026-06-30',
      is_closed=None,
      closed_message='Closed.',
      closed_start='2026-06-01',
      closed_end='2026-06-30' )
   expired_record = make_animal_viewability_record(
      is_off_display=1,
      off_display_message='Temporarily hidden.',
      off_display_start='2026-06-01',
      off_display_end='2026-06-30',
      schedule_start_date='2026-06-01',
      schedule_end_date='2026-06-30',
      daily_start_time='09:00',
      daily_end_time='11:00',
      viewing_message='Morning only.',
      alert_message='Low visibility.',
      alert_start_date='2026-06-01',
      alert_end_date='2026-06-30',
      is_closed=0,
      closed_message='Closed.',
      closed_start='2026-06-01',
      closed_end='2026-06-30' )
   target_date = date( 2026, 7, 15 )

   assert get_active_off_display_status( inactive_record, target_date ) == ( False, None )
   assert get_active_limited_viewing_status( inactive_record, target_date ) == ( False, None )
   assert get_active_viewing_alert_status( inactive_record, target_date ) == ( False, None )
   assert get_active_exhibit_status( inactive_record, target_date ) == ( ScheduleStatus.UNKNOWN, None )

   assert get_active_off_display_status( expired_record, target_date ) == ( False, None )
   assert get_active_limited_viewing_status( expired_record, target_date ) == ( False, None )
   assert get_active_viewing_alert_status( expired_record, target_date ) == ( False, None )
   assert get_active_exhibit_status( expired_record, target_date ) == ( ScheduleStatus.UNKNOWN, None )
   assert get_active_exhibit_status( expired_record, date( 2026, 6, 15 ) ) == ( ScheduleStatus.OPEN, None )

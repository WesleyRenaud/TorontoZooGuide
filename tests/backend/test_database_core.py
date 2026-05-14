from datetime import date, datetime

import pytest

from api import zoo
from api.data_access.animal_viewability_mapper import map_animal_viewability_row
from api.enums import ExhibitStatus
from api.logic.animal_viewability import calculate_animal_likelihood
from api.logic.animal_viewability import get_active_exhibit_status
from api.logic.animal_viewability import get_active_limited_viewing_status
from api.logic.animal_viewability import get_active_off_display_status
from api.logic.animal_viewability import get_active_viewing_alert_status
from conftest import make_row


def test_database_uses_injected_path( db ):
   assert db.get_species()


def test_close_is_idempotent( db ):
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
def test_parse_date_value( value, expected ):
   assert zoo.ZooUtil.parse_date_value( value ) == expected


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
def test_normalize_date_key( value, expected ):
   assert zoo.ZooUtil.normalize_date_key( value ) == expected


def test_normalize_date_key_returns_none_for_unsupported_date_strings():
   assert zoo.ZooUtil.normalize_date_key( 'June 15, 2026' ) is None


@pytest.mark.parametrize(
   'value, expected',
   [
      ( None, None ),
      ( '2026-06-15 09:30 AM', datetime( 2026, 6, 15, 9, 30 ) ),
      ( '2026-06-15 17:45:00', datetime( 2026, 6, 15, 17, 45 ) ),
      ( '2026-06-15 17:45', datetime( 2026, 6, 15, 17, 45 ) )
   ]
)
def test_parse_datetime_value( value, expected ):
   assert zoo.ZooUtil.parse_datetime_value( value ) == expected


def test_parse_values_raise_for_unsupported_formats():
   with pytest.raises( ValueError ):
      zoo.ZooUtil.parse_date_value( 'June 15, 2026' )

   with pytest.raises( ValueError ):
      zoo.ZooUtil.parse_datetime_value( 'June 15, 2026 9:30' )


@pytest.mark.parametrize(
   'target, start, end, expected',
   [
      ( date( 2026, 6, 15 ), None, None, True ),
      ( date( 2026, 6, 15 ), '2026-06-15', '2026-06-15', True ),
      ( date( 2026, 6, 14 ), '2026-06-15', None, False ),
      ( date( 2026, 6, 16 ), None, '2026-06-15', False )
   ]
)
def test_is_date_in_range( target, start, end, expected ):
   assert zoo.ZooUtil.is_date_in_range( target_date=target, start_date_value=start, end_date_value=end ) is expected


@pytest.mark.parametrize(
   'method_name',
   [
      'calculate_restaurant_likelihood',
      'calculate_gift_shop_likelihood',
      'calculate_attraction_likelihood'
   ]
)
def test_simple_likelihood_calculators_clamp_and_round( db, method_name ):
   method = getattr( db, method_name )

   assert method( None ) == 100
   assert method( -0.5 ) == 0
   assert method( 0.444 ) == 44
   assert method( 1.5 ) == 100


def test_calculate_animal_likelihood_handles_indoor_and_outdoor_inputs():
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


def test_active_status_helpers():
   active_record = map_animal_viewability_row( make_row(
      {
         'IS_OFF_DISPLAY': 1,
         'OFF_DISPLAY_MESSAGE': 'Temporarily hidden.',
         'OFF_DISPLAY_START': '2026-06-01',
         'OFF_DISPLAY_END': '2026-06-30',
         'SCHEDULE_START_DATE': '2026-06-01',
         'SCHEDULE_END_DATE': '2026-06-30',
         'DAILY_START_TIME': '09:00',
         'DAILY_END_TIME': '11:00',
         'VIEWING_MESSAGE': 'Morning only.',
         'ALERT_MESSAGE': 'Low visibility.',
         'ALERT_START_DATE': '2026-06-01',
         'ALERT_END_DATE': '2026-06-30',
         'IS_CLOSED': 1,
         'CLOSED_MESSAGE': 'Closed.',
         'CLOSED_START': '2026-06-01',
         'CLOSED_END': '2026-06-30'
      }
   ) )
   target_date = date( 2026, 6, 15 )

   assert get_active_off_display_status( active_record, target_date ) == ( True, 'Temporarily hidden.' )
   assert get_active_limited_viewing_status( active_record, target_date ) == ( True, 'Morning only.' )
   assert get_active_viewing_alert_status( active_record, target_date ) == ( True, 'Low visibility.' )
   assert get_active_exhibit_status( active_record, target_date ) == ( ExhibitStatus.CLOSED, 'Closed.' )


def test_active_status_helpers_return_inactive_defaults():
   inactive_record = map_animal_viewability_row( make_row(
      {
         'IS_OFF_DISPLAY': 0,
         'OFF_DISPLAY_MESSAGE': 'Temporarily hidden.',
         'OFF_DISPLAY_START': '2026-06-01',
         'OFF_DISPLAY_END': '2026-06-30',
         'SCHEDULE_START_DATE': '2026-06-01',
         'SCHEDULE_END_DATE': '2026-06-30',
         'DAILY_START_TIME': None,
         'DAILY_END_TIME': '11:00',
         'VIEWING_MESSAGE': 'Morning only.',
         'ALERT_MESSAGE': None,
         'ALERT_START_DATE': '2026-06-01',
         'ALERT_END_DATE': '2026-06-30',
         'IS_CLOSED': None,
         'CLOSED_MESSAGE': 'Closed.',
         'CLOSED_START': '2026-06-01',
         'CLOSED_END': '2026-06-30'
      }
   ) )
   expired_record = map_animal_viewability_row( make_row(
      {
         'IS_OFF_DISPLAY': 1,
         'OFF_DISPLAY_MESSAGE': 'Temporarily hidden.',
         'OFF_DISPLAY_START': '2026-06-01',
         'OFF_DISPLAY_END': '2026-06-30',
         'SCHEDULE_START_DATE': '2026-06-01',
         'SCHEDULE_END_DATE': '2026-06-30',
         'DAILY_START_TIME': '09:00',
         'DAILY_END_TIME': '11:00',
         'VIEWING_MESSAGE': 'Morning only.',
         'ALERT_MESSAGE': 'Low visibility.',
         'ALERT_START_DATE': '2026-06-01',
         'ALERT_END_DATE': '2026-06-30',
         'IS_CLOSED': 0,
         'CLOSED_MESSAGE': 'Closed.',
         'CLOSED_START': '2026-06-01',
         'CLOSED_END': '2026-06-30'
      }
   ) )
   target_date = date( 2026, 7, 15 )

   assert get_active_off_display_status( inactive_record, target_date ) == ( False, None )
   assert get_active_limited_viewing_status( inactive_record, target_date ) == ( False, None )
   assert get_active_viewing_alert_status( inactive_record, target_date ) == ( False, None )
   assert get_active_exhibit_status( inactive_record, target_date ) == ( ExhibitStatus.UNKNOWN, None )

   assert get_active_off_display_status( expired_record, target_date ) == ( False, None )
   assert get_active_limited_viewing_status( expired_record, target_date ) == ( False, None )
   assert get_active_viewing_alert_status( expired_record, target_date ) == ( False, None )
   assert get_active_exhibit_status( expired_record, target_date ) == ( ExhibitStatus.UNKNOWN, None )
   assert get_active_exhibit_status( expired_record, date( 2026, 6, 15 ) ) == ( ExhibitStatus.OPEN, None )

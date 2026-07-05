from __future__ import annotations

from datetime import date

from api.animals.data_access.animal_viewability_record import AnimalViewabilityRecord
from api.animals.domain.animal_viewability import calculate_animal_likelihood
from api.animals.domain.animal_viewability import get_active_exhibit_status
from api.animals.domain.animal_viewability import get_active_limited_viewing_status
from api.animals.domain.animal_viewability import get_active_off_display_status
from api.animals.domain.animal_viewability import get_active_viewing_alert_status
from api.shared.enums import ScheduleStatus


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
      'enclosure_name': None,
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
      'include_all_viewing_spots': None,
   }
   values.update( overrides )

   return AnimalViewabilityRecord( **values )


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

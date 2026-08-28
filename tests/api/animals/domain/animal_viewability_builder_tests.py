from __future__ import annotations

from datetime import date

from api.animals.data_access.animal_viewability_record import AnimalViewabilityRecord
from api.animals.domain.animal_viewability_builder import AnimalViewabilityBuilder
from api.shared.enums import ScheduleStatus


TARGET_DATE = date( 2026, 6, 15 )
EXPIRED_TARGET_DATE = date( 2026, 7, 15 )
OFF_DISPLAY_MESSAGE = 'Temporarily hidden.'
LIMITED_VIEWING_MESSAGE = 'Morning only.'
VIEWING_ALERT_MESSAGE = 'Low visibility.'
CLOSED_MESSAGE = 'Closed.'
SCHEDULE_START_DATE = '2026-06-01'
SCHEDULE_END_DATE = '2026-06-30'
DAILY_START_TIME = '09:00'
DAILY_END_TIME = '11:00'


def _make_animal_viewability_record( **overrides: object ) -> AnimalViewabilityRecord:
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
      'is_zoomobile_only': False,
   }
   values.update( overrides )

   return AnimalViewabilityRecord( **values )


def Test_CalculateAnimalLikelihood_TestIndoorTemperature_ExpectFullLikelihoodWhenExhibitOpen() -> None:
   assert AnimalViewabilityBuilder.calculate_animal_likelihood(
      temp=-20,
      sigma=2,
      enclosure_type='indoor',
      min_temperature=30,
      day_seasonal_multiplier=0,
      exhibit_day_seasonal_availability_multiplier=1
   ) == 100


def Test_CalculateAnimalLikelihood_TestIndoorTemperature_ExpectZeroWhenExhibitClosed() -> None:
   assert AnimalViewabilityBuilder.calculate_animal_likelihood(
      temp=-20,
      sigma=2,
      enclosure_type='indoor',
      min_temperature=30,
      day_seasonal_multiplier=0,
      exhibit_day_seasonal_availability_multiplier=0
   ) == 0


def Test_CalculateAnimalLikelihood_TestOutdoorSeasonalMultipliers_ExpectScaledLikelihood() -> None:
   assert AnimalViewabilityBuilder.calculate_animal_likelihood(
      temp=20,
      sigma=2,
      enclosure_type='Outdoor',
      min_temperature=20,
      day_seasonal_multiplier=0.5,
      exhibit_day_seasonal_availability_multiplier=0.5
   ) == 12


def Test_CalculateAnimalLikelihood_TestMissingInputs_ExpectDefaultLikelihood() -> None:
   assert AnimalViewabilityBuilder.calculate_animal_likelihood(
      temp=None,
      sigma=2,
      enclosure_type='Outdoor',
      min_temperature=None,
      day_seasonal_multiplier=None,
      exhibit_day_seasonal_availability_multiplier=None
   ) == 100


def Test_GetActiveOffDisplayStatus_TestActiveRecord_ExpectMessage() -> None:
   active_record = _make_animal_viewability_record(
      is_off_display=1,
      off_display_message=OFF_DISPLAY_MESSAGE,
      off_display_start=SCHEDULE_START_DATE,
      off_display_end=SCHEDULE_END_DATE )

   assert AnimalViewabilityBuilder.get_active_off_display_status(
      active_record,
      TARGET_DATE ) == ( True, OFF_DISPLAY_MESSAGE )


def Test_GetActiveLimitedViewingStatus_TestActiveRecord_ExpectMessage() -> None:
   active_record = _make_animal_viewability_record(
      schedule_start_date=SCHEDULE_START_DATE,
      schedule_end_date=SCHEDULE_END_DATE,
      daily_start_time=DAILY_START_TIME,
      daily_end_time=DAILY_END_TIME,
      viewing_message=LIMITED_VIEWING_MESSAGE )

   assert AnimalViewabilityBuilder.get_active_limited_viewing_status(
      active_record,
      TARGET_DATE ) == ( True, LIMITED_VIEWING_MESSAGE )


def Test_GetActiveViewingAlertStatus_TestActiveRecord_ExpectMessage() -> None:
   active_record = _make_animal_viewability_record(
      alert_message=VIEWING_ALERT_MESSAGE,
      alert_start_date=SCHEDULE_START_DATE,
      alert_end_date=SCHEDULE_END_DATE )

   assert AnimalViewabilityBuilder.get_active_viewing_alert_status(
      active_record,
      TARGET_DATE ) == ( True, VIEWING_ALERT_MESSAGE )


def Test_GetActiveExhibitStatus_TestActiveRecord_ExpectClosedStatus() -> None:
   active_record = _make_animal_viewability_record(
      is_closed=1,
      closed_message=CLOSED_MESSAGE,
      closed_start=SCHEDULE_START_DATE,
      closed_end=SCHEDULE_END_DATE )

   assert AnimalViewabilityBuilder.get_active_exhibit_status(
      active_record,
      TARGET_DATE ) == ( ScheduleStatus.CLOSED, CLOSED_MESSAGE )


def Test_GetActiveOffDisplayStatus_TestInactiveRecord_ExpectInactiveDefault() -> None:
   inactive_record = _make_animal_viewability_record(
      is_off_display=0,
      off_display_message=OFF_DISPLAY_MESSAGE,
      off_display_start=SCHEDULE_START_DATE,
      off_display_end=SCHEDULE_END_DATE )

   assert AnimalViewabilityBuilder.get_active_off_display_status(
      inactive_record,
      TARGET_DATE ) == ( False, None )


def Test_GetActiveLimitedViewingStatus_TestInactiveRecord_ExpectInactiveDefault() -> None:
   inactive_record = _make_animal_viewability_record(
      schedule_start_date=SCHEDULE_START_DATE,
      schedule_end_date=SCHEDULE_END_DATE,
      daily_start_time=None,
      daily_end_time=DAILY_END_TIME,
      viewing_message=LIMITED_VIEWING_MESSAGE )

   assert AnimalViewabilityBuilder.get_active_limited_viewing_status(
      inactive_record,
      TARGET_DATE ) == ( False, None )


def Test_GetActiveViewingAlertStatus_TestInactiveRecord_ExpectInactiveDefault() -> None:
   inactive_record = _make_animal_viewability_record(
      alert_message=None,
      alert_start_date=SCHEDULE_START_DATE,
      alert_end_date=SCHEDULE_END_DATE )

   assert AnimalViewabilityBuilder.get_active_viewing_alert_status(
      inactive_record,
      TARGET_DATE ) == ( False, None )


def Test_GetActiveExhibitStatus_TestInactiveRecord_ExpectUnknownStatus() -> None:
   inactive_record = _make_animal_viewability_record(
      is_closed=None,
      closed_message=CLOSED_MESSAGE,
      closed_start=SCHEDULE_START_DATE,
      closed_end=SCHEDULE_END_DATE )

   assert AnimalViewabilityBuilder.get_active_exhibit_status(
      inactive_record,
      TARGET_DATE ) == ( ScheduleStatus.UNKNOWN, None )


def Test_GetActiveOffDisplayStatus_TestExpiredRecord_ExpectInactiveDefault() -> None:
   expired_record = _make_animal_viewability_record(
      is_off_display=1,
      off_display_message=OFF_DISPLAY_MESSAGE,
      off_display_start=SCHEDULE_START_DATE,
      off_display_end=SCHEDULE_END_DATE )

   assert AnimalViewabilityBuilder.get_active_off_display_status(
      expired_record,
      EXPIRED_TARGET_DATE ) == ( False, None )


def Test_GetActiveExhibitStatus_TestExpiredRecordOnTargetDate_ExpectOpenStatus() -> None:
   expired_record = _make_animal_viewability_record(
      is_closed=0,
      closed_message=CLOSED_MESSAGE,
      closed_start=SCHEDULE_START_DATE,
      closed_end=SCHEDULE_END_DATE )

   assert AnimalViewabilityBuilder.get_active_exhibit_status(
      expired_record,
      TARGET_DATE ) == ( ScheduleStatus.OPEN, None )

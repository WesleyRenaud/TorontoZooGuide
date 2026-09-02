from __future__ import annotations

from datetime import date

import pytest

from api.animals.data_access.animal_viewability_record import AnimalViewabilityRecord
from api.animals.domain.animal_viewability_builder import AnimalViewabilityBuilder
from api.animals.domain.indoor_outdoor_viewing_visibility_builder import IndoorOutdoorViewingVisibilityBuilder
from api.app_string_provider import AppStringProvider
from api.models import Animal
from api.shared.enums import ScheduleStatus
from api.walk_graph.viewing_walk_node_id_applier import ViewingWalkNodeIdApplier


TARGET_DATE = date( 2026, 6, 15 )
EXPIRED_TARGET_DATE = date( 2026, 7, 15 )
OFF_DISPLAY_MESSAGE = 'Temporarily hidden.'
LIMITED_VIEWING_MESSAGE = 'Morning only.'
VIEWING_ALERT_MESSAGE = 'Low visibility.'
CLOSED_MESSAGE = 'Closed.'
SEASONALLY_OFF_DISPLAY_MESSAGE = 'Seasonally unavailable.'
EXHIBIT_LIKELY_CLOSED_MESSAGE = 'Exhibit likely closed.'
SPECIES_LIKELY_OFF_DISPLAY_MESSAGE = 'Species likely off display.'
SCHEDULE_START_DATE = '2026-06-01'
SCHEDULE_END_DATE = '2026-06-30'
DAILY_START_TIME = '09:00'
DAILY_END_TIME = '11:00'
SPECIES = 'African Lion'
EXHIBIT = 'Africa Savanna'
TEMP = 20.0
SIGMA = 2


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


def Test_GetActiveLimitedViewingStatus_TestExpiredRecord_ExpectInactiveDefault() -> None:
   expired_record = _make_animal_viewability_record(
      schedule_start_date=SCHEDULE_START_DATE,
      schedule_end_date=SCHEDULE_END_DATE,
      daily_start_time=DAILY_START_TIME,
      daily_end_time=DAILY_END_TIME,
      viewing_message=LIMITED_VIEWING_MESSAGE )

   assert AnimalViewabilityBuilder.get_active_limited_viewing_status(
      expired_record,
      EXPIRED_TARGET_DATE ) == ( False, None )


def Test_GetActiveViewingAlertStatus_TestExpiredRecord_ExpectInactiveDefault() -> None:
   expired_record = _make_animal_viewability_record(
      alert_message=VIEWING_ALERT_MESSAGE,
      alert_start_date=SCHEDULE_START_DATE,
      alert_end_date=SCHEDULE_END_DATE )

   assert AnimalViewabilityBuilder.get_active_viewing_alert_status(
      expired_record,
      EXPIRED_TARGET_DATE ) == ( False, None )


def Test_GetActiveExhibitStatus_TestDateOutsideRange_ExpectUnknownStatus() -> None:
   record = _make_animal_viewability_record(
      is_closed=1,
      closed_message=CLOSED_MESSAGE,
      closed_start=SCHEDULE_START_DATE,
      closed_end=SCHEDULE_END_DATE )

   assert AnimalViewabilityBuilder.get_active_exhibit_status(
      record,
      EXPIRED_TARGET_DATE ) == ( ScheduleStatus.UNKNOWN, None )


def Test_BuildViewableAnimalFromRecord_TestOffDisplay_ExpectZeroLikelihoodAndMessage(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   record = _make_animal_viewability_record(
      species=SPECIES,
      exhibit=EXHIBIT,
      is_off_display=1,
      off_display_message=OFF_DISPLAY_MESSAGE,
      off_display_start=SCHEDULE_START_DATE,
      off_display_end=SCHEDULE_END_DATE,
      enclosure_type='Outdoor',
      min_temperature=0,
      animal_day_seasonal_multiplier=1.0,
      exhibit_day_seasonal_availability_multiplier=1.0 )
   monkeypatch.setattr( ViewingWalkNodeIdApplier, 'apply', lambda _animal: None )

   animal = AnimalViewabilityBuilder.build_viewable_animal_from_record(
      record,
      target_date=TARGET_DATE,
      temp=TEMP,
      sigma=SIGMA )

   assert animal.species == SPECIES
   assert animal.likelihood == 0
   assert animal.off_display_message == OFF_DISPLAY_MESSAGE


def Test_BuildViewableAnimalFromRecord_TestClosedExhibit_ExpectZeroLikelihoodAndClosedMessage(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   record = _make_animal_viewability_record(
      species=SPECIES,
      exhibit=EXHIBIT,
      is_closed=1,
      closed_message=CLOSED_MESSAGE,
      closed_start=SCHEDULE_START_DATE,
      closed_end=SCHEDULE_END_DATE,
      enclosure_type='Indoor' )
   monkeypatch.setattr( ViewingWalkNodeIdApplier, 'apply', lambda _animal: None )

   animal = AnimalViewabilityBuilder.build_viewable_animal_from_record(
      record,
      target_date=TARGET_DATE,
      temp=TEMP,
      sigma=SIGMA )

   assert animal.likelihood == 0
   assert animal.off_display_message == CLOSED_MESSAGE


def Test_BuildViewableAnimalFromRecord_TestLimitedViewingAndAlert_ExpectFlagsAndMessages(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   record = _make_animal_viewability_record(
      species=SPECIES,
      exhibit=EXHIBIT,
      enclosure_type='Indoor',
      schedule_start_date=SCHEDULE_START_DATE,
      schedule_end_date=SCHEDULE_END_DATE,
      daily_start_time=DAILY_START_TIME,
      daily_end_time=DAILY_END_TIME,
      viewing_message=LIMITED_VIEWING_MESSAGE,
      alert_message=VIEWING_ALERT_MESSAGE,
      alert_start_date=SCHEDULE_START_DATE,
      alert_end_date=SCHEDULE_END_DATE,
      is_closed=0,
      closed_start=SCHEDULE_START_DATE,
      closed_end=SCHEDULE_END_DATE,
      animal_day_seasonal_multiplier=1.0,
      exhibit_day_seasonal_availability_multiplier=1.0 )
   monkeypatch.setattr( ViewingWalkNodeIdApplier, 'apply', lambda _animal: None )

   animal = AnimalViewabilityBuilder.build_viewable_animal_from_record(
      record,
      target_date=TARGET_DATE,
      temp=TEMP,
      sigma=SIGMA )

   assert animal.likelihood == 100
   assert animal.has_limited_viewing_schedule is True
   assert animal.limited_viewing_message == LIMITED_VIEWING_MESSAGE
   assert animal.viewing_alert_messages == [ VIEWING_ALERT_MESSAGE ]
   assert animal.off_display_message is None


def Test_BuildViewableAnimalFromRecord_TestUnknownExhibitMultiplierZero_ExpectExhibitClosedMessage(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   record = _make_animal_viewability_record(
      species=SPECIES,
      exhibit=EXHIBIT,
      enclosure_type='Indoor',
      exhibit_day_seasonal_availability_multiplier=0,
      animal_day_seasonal_multiplier=1.0 )
   monkeypatch.setattr( ViewingWalkNodeIdApplier, 'apply', lambda _animal: None )
   monkeypatch.setattr(
      AppStringProvider,
      'format',
      lambda key, **kwargs: EXHIBIT_LIKELY_CLOSED_MESSAGE
      if key == 'guestStatus.animals.exhibitLikelyClosedOnDay' and kwargs.get( 'exhibit' ) == EXHIBIT
      else key )

   animal = AnimalViewabilityBuilder.build_viewable_animal_from_record(
      record,
      target_date=TARGET_DATE,
      temp=TEMP,
      sigma=SIGMA )

   assert animal.likelihood == 0
   assert animal.off_display_message == EXHIBIT_LIKELY_CLOSED_MESSAGE


def Test_BuildViewableAnimalFromRecord_TestSeasonallyOffDisplayMessage_ExpectSeasonalMessage(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   record = _make_animal_viewability_record(
      species=SPECIES,
      exhibit=EXHIBIT,
      enclosure_type='Outdoor',
      min_temperature=100,
      animal_day_seasonal_multiplier=0,
      exhibit_day_seasonal_availability_multiplier=1.0,
      seasonally_off_display_message=SEASONALLY_OFF_DISPLAY_MESSAGE )
   monkeypatch.setattr( ViewingWalkNodeIdApplier, 'apply', lambda _animal: None )
   monkeypatch.setattr(
      AnimalViewabilityBuilder,
      'calculate_animal_likelihood',
      lambda **_kwargs: 0 )

   animal = AnimalViewabilityBuilder.build_viewable_animal_from_record(
      record,
      target_date=TARGET_DATE,
      temp=TEMP,
      sigma=SIGMA )

   assert animal.likelihood == 0
   assert animal.off_display_message == SEASONALLY_OFF_DISPLAY_MESSAGE


def Test_BuildViewableAnimalFromRecord_TestZeroLikelihoodWithoutSeasonalMessage_ExpectSpeciesMessage(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   record = _make_animal_viewability_record(
      species=SPECIES,
      exhibit=EXHIBIT,
      enclosure_type='Outdoor',
      animal_day_seasonal_multiplier=0,
      exhibit_day_seasonal_availability_multiplier=1.0 )
   monkeypatch.setattr( ViewingWalkNodeIdApplier, 'apply', lambda _animal: None )
   monkeypatch.setattr(
      AnimalViewabilityBuilder,
      'calculate_animal_likelihood',
      lambda **_kwargs: 0 )
   monkeypatch.setattr(
      AppStringProvider,
      'format',
      lambda key, **kwargs: SPECIES_LIKELY_OFF_DISPLAY_MESSAGE
      if key == 'guestStatus.animals.speciesLikelyOffDisplayOnDay' and kwargs.get( 'species' ) == SPECIES
      else key )

   animal = AnimalViewabilityBuilder.build_viewable_animal_from_record(
      record,
      target_date=TARGET_DATE,
      temp=TEMP,
      sigma=SIGMA )

   assert animal.likelihood == 0
   assert animal.off_display_message == SPECIES_LIKELY_OFF_DISPLAY_MESSAGE


def Test_BuildViewableAnimalsOnDay_TestThresholdAndIncludeOffDisplay_ExpectFiltered(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   high = Animal( species='High', exhibit=EXHIBIT, likelihood=80 )
   low = Animal( species='Low', exhibit=EXHIBIT, likelihood=10 )
   off_display = Animal( species='Off', exhibit=EXHIBIT, likelihood=0 )
   records = [
      _make_animal_viewability_record( species='High', exhibit=EXHIBIT ),
      _make_animal_viewability_record( species='Low', exhibit=EXHIBIT ),
      _make_animal_viewability_record( species='Off', exhibit=EXHIBIT ),
   ]
   built = {
      'High': high,
      'Low': low,
      'Off': off_display,
   }

   monkeypatch.setattr(
      AnimalViewabilityBuilder,
      'build_viewable_animal_from_record',
      lambda record, **_kwargs: built[ record.species ] )
   monkeypatch.setattr(
      IndoorOutdoorViewingVisibilityBuilder,
      'apply',
      lambda animals: animals )

   assert [
      animal.species
      for animal in AnimalViewabilityBuilder.build_viewable_animals_on_day(
         records,
         target_date=TARGET_DATE,
         temp=TEMP,
         sigma=SIGMA,
         threshold=50 )
   ] == [ 'High' ]

   assert [
      animal.species
      for animal in AnimalViewabilityBuilder.build_viewable_animals_on_day(
         records,
         target_date=TARGET_DATE,
         temp=TEMP,
         sigma=SIGMA,
         include_off_display_animals=True )
   ] == [ 'High', 'Low', 'Off' ]

   assert [
      animal.species
      for animal in AnimalViewabilityBuilder.build_viewable_animals_on_day(
         records,
         target_date=TARGET_DATE,
         temp=TEMP,
         sigma=SIGMA )
   ] == [ 'High', 'Low' ]

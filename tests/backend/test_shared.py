from __future__ import annotations

from typing import Any

import pytest

from api.itinerary.domain.itinerary_adjustment_type import ItineraryAdjustmentType
from api.itinerary.scheduling import ItineraryActivityScheduler
from api.models import Animal
from api.models import Attraction
from api.models import GuardiansTalk
from api.models import Itinerary
from api.models import WildEncounter
from api.shared.constants import ANIMAL_VISIBILITY_CHANGE_THRESHOLD
from api.shared.constants import ITINERARY_ANIMAL_MIN_LIKELIHOOD
from api.shared.constants import itinerary_config_to_dict
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ItineraryEventType
from api.shared.value_conversion import ValueConversion
from api.shared.weather import Weather


def test_itinerary_config_exposes_animal_visibility_change_threshold() -> None:
   assert itinerary_config_to_dict()[
      'animal_visibility_change_threshold'
   ] == ANIMAL_VISIBILITY_CHANGE_THRESHOLD


def test_itinerary_config_exposes_itinerary_animal_min_likelihood() -> None:
   assert itinerary_config_to_dict()[
      'itinerary_animal_min_likelihood'
   ] == ITINERARY_ANIMAL_MIN_LIKELIHOOD


def test_itinerary_activity_scheduler_sets_activity_times_and_events() -> None:
   itinerary = Itinerary(
      date='2026-06-15',
      animals=[ Animal( species='Lion', exhibit='Savanna' ) ],
      attractions=[ Attraction( name='Carousel', free_with_admission=True ) ],
      guardians_talks=[
         GuardiansTalk(
            name='Rhino Talk',
            location='Rhino House',
            x_coord=1.0,
            y_coord=2.0 )
      ],
      wild_encounters=[
         WildEncounter(
            name='Capybara',
            meeting_spot='Mayan Temple Meeting Spot',
            link='capybara' )
      ] )
   scheduler = ItineraryActivityScheduler( itinerary )

   assert scheduler.schedule_animal( 'Lion', 'Savanna', '10:00', '10:20' )
   assert scheduler.schedule_attraction( 'Carousel', '11:00', '11:30' )
   assert scheduler.schedule_guardians_talk( 'Rhino Talk', '12:00', '12:30' )
   assert scheduler.schedule_wild_encounter( 'Capybara', '13:00', '13:45' )

   scheduler.schedule_event( ItineraryEventType.LUNCH, '14:00', '14:30' )

   assert itinerary.animals[ 0 ].start_time == '10:00 AM'
   assert itinerary.attractions[ 0 ].end_time == '11:30 AM'
   assert itinerary.guardians_talks[ 0 ].start_time == '12:00 PM'
   assert itinerary.wild_encounters[ 0 ].end_time == '1:45 PM'
   assert itinerary.events[ 0 ].to_dict() == {
      'event_type': 'lunch',
      'start_time': '2:00 PM',
      'end_time': '2:30 PM',
      'type': 'itineraryEvent',
   }


def test_itinerary_config_exposes_event_types() -> None:
   assert itinerary_config_to_dict()[ 'itinerary_event_types' ] == [
      event_type.value for event_type in ItineraryEventType
   ]


def test_itinerary_config_exposes_visit_boundary_event_types() -> None:
   assert itinerary_config_to_dict()[ 'itinerary_visit_boundary_event_types' ] == {
      'arrival': ItineraryEventType.ARRIVAL.value,
      'departure': ItineraryEventType.DEPARTURE.value,
   }


def test_itinerary_config_exposes_error_types() -> None:
   assert itinerary_config_to_dict()[ 'itinerary_error_types' ] == {
      error_type.name: error_type.value
      for error_type in ItineraryErrorType
   }


def test_itinerary_config_exposes_adjustment_types() -> None:
   assert itinerary_config_to_dict()[ 'itinerary_adjustment_types' ] == {
      adjustment_type.name: adjustment_type.value
      for adjustment_type in ItineraryAdjustmentType
   }


def test_itinerary_config_exposes_suppressed_error_types_without_connection() -> None:
   assert itinerary_config_to_dict()[ 'suppressed_error_types' ] == []


def test_itinerary_config_exposes_itinerary_statuses_without_connection() -> None:
   assert itinerary_config_to_dict()[ 'itinerary_statuses' ] == []


@pytest.mark.parametrize(
   'value, expected',
   [
      ( True, True ),
      ( False, False ),
      ( 1, True ),
      ( 0, False ),
      ( None, False ),
      ( 'true', False )
   ]
)
def test_as_boolean( value: Any, expected: bool ) -> None:
   assert ValueConversion.as_boolean( value ) is expected


@pytest.mark.parametrize(
   'value, expected',
   [
      ( None, '' ),
      ( '  Lion  ', 'Lion' ),
      ( 42, '42' ),
   ]
)
def test_as_trimmed_string( value: Any, expected: str ) -> None:
   assert ValueConversion.as_trimmed_string( value ) == expected


@pytest.mark.parametrize(
   'value, expected',
   [
      ( None, None ),
      ( '   ', None ),
      ( '  Lion  ', 'Lion' ),
   ]
)
def test_as_nullable_string( value: Any, expected: str | None ) -> None:
   assert ValueConversion.as_nullable_string( value ) == expected


@pytest.mark.parametrize(
   'value, expected',
   [
      ( None, [] ),
      ( 'Alert message.', [ 'Alert message.' ] ),
   ]
)
def test_as_singleton_list( value: str | None, expected: list[ str ] ) -> None:
   assert ValueConversion.as_singleton_list( value ) == expected


def test_temperature_helpers_are_stable() -> None:
   assert Weather.get_average_temperature( 'Jan', 1 ) == -5.0
   assert Weather.get_average_temperature( 'Jul', 1 ) == 26.0
   assert Weather.get_temperature_probability( mu=20, sigma=2, min_temperature=20 ) == 0.5
   assert Weather.get_temperature_probability( mu=25, sigma=2, min_temperature=20 ) > 0.99

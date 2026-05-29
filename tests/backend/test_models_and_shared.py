from __future__ import annotations

from datetime import date, datetime
from typing import Any

import pytest

from api.itinerary.scheduling import ItineraryActivityScheduler
from api.models import Animal
from api.models import Attraction
from api.models import Defibrillator
from api.models import DrinkingFountain
from api.models import EmergencyIntercom
from api.models import EventSite
from api.models import GiftShop
from api.models import GuardiansTalk
from api.models import GuestService
from api.models import Itinerary
from api.models import Pavilion
from api.models import PicnicSite
from api.models import Restaurant
from api.models import Restroom
from api.models import Update
from api.models import WildEncounter
from api.models import ZoomobileRoute
from api.models import ZoomobileRouteMarker
from api.models import ZoomobileStation
from api.shared.calendar_dates import CalendarDates
from api.shared.constants import itinerary_config_to_dict
import api.shared.date_values as date_values
from api.shared.enums import ItineraryEventType
from api.shared.value_conversion import ValueConversion
from api.shared.weather import Weather
from api.types import MonthInput, VisitMonth


def test_domain_objects_serialize_to_frontend_shapes() -> None:
   assert Pavilion( name='Pavilion', region='Region', x_coord=1, y_coord=2 ).to_dict() == {
      'name': 'Pavilion',
      'region': 'Region',
      'description': None,
      'x_coord': 1,
      'y_coord': 2
   }

   assert Restaurant(
      name='Cafe',
      location='North',
      sub_location='Inside',
      is_closed=1,
      likelihood=0
   ).to_dict()[ 'is_closed' ] is True

   assert GiftShop( name='Shop', location='Gate', is_closed=0 ).to_dict()[ 'is_closed' ] is False
   assert Attraction( name='Ride', free_with_admission=1 ).to_dict()[ 'free_with_admission' ] is True
   assert Attraction( name='Ride', free_with_admission=1 ).to_dict()[ 'is_deleted' ] is False
   assert Restroom( title='Restroom', x_coord=3, y_coord=4 ).to_dict()[ 'title' ] == 'Restroom'
   assert ZoomobileStation( name='Station' ).to_dict()[ 'name' ] == 'Station'
   assert ZoomobileRouteMarker( route_type='summer', x_coord=1, y_coord=2 ).to_dict()[ 'route_type' ] == 'summer'
   assert GuardiansTalk( name='Talk', location='Habitat', x_coord=1, y_coord=2 ).to_dict()[ 'is_available' ] is True
   assert GuardiansTalk( name='Talk', location='Habitat', x_coord=1, y_coord=2 ).to_dict()[ 'is_deleted' ] is False
   assert WildEncounter( name='Encounter', meeting_spot='Spot', link='https://example.test' ).to_dict()[ 'is_available' ] is True
   assert WildEncounter( name='Encounter', meeting_spot='Spot', link='https://example.test' ).to_dict()[ 'is_deleted' ] is False
   assert DrinkingFountain( x_coord=1, y_coord=2, is_closed=1, likelihood=0.0 ).to_dict() == {
      'x_coord': 1,
      'y_coord': 2,
      'is_closed': True,
      'closed_message': None,
      'likelihood': 0.0
   }
   assert Defibrillator( x_coord=5, y_coord=6 ).to_dict() == {
      'x_coord': 5,
      'y_coord': 6
   }
   assert EmergencyIntercom( x_coord=7, y_coord=8 ).to_dict() == {
      'x_coord': 7,
      'y_coord': 8
   }
   assert GuestService(
      service_type='Information',
      x_coord=9,
      y_coord=10
   ).to_dict() == {
      'service_type': 'Information',
      'x_coord': 9,
      'y_coord': 10
   }
   assert PicnicSite(
      x_coord=11,
      y_coord=12
   ).to_dict() == {
      'x_coord': 11,
      'y_coord': 12
   }
   assert EventSite(
      name='Special Events Center',
      x_coord=13,
      y_coord=14
   ).to_dict() == {
      'name': 'Special Events Center',
      'x_coord': 13,
      'y_coord': 14
   }
   assert Update(
      title='New baby giraffe',
      description='Come meet the new calf.',
      update_type='New Arrival',
      start_date='2026-06-01',
      end_date='2026-06-30'
   ).to_dict() == {
      'title': 'New baby giraffe',
      'description': 'Come meet the new calf.',
      'type': 'New Arrival',
      'start_date': '2026-06-01',
      'end_date': '2026-06-30'
   }


def test_animal_to_dict_converts_boolean_flags() -> None:
   animal = Animal(
      species='Amur Tiger',
      has_limited_viewing_schedule=1,
      has_viewing_alert=0
   )

   result = animal.to_dict()

   assert result[ 'species' ] == 'Amur Tiger'
   assert result[ 'has_limited_viewing_schedule' ] is True
   assert result[ 'has_viewing_alert' ] is False
   assert result[ 'is_deleted' ] is False


def test_itinerary_serializes_objects_and_dicts_with_types() -> None:
   itinerary = Itinerary(
      date='2026-06-15',
      animals=[
         Animal(
            species='Amur Tiger',
            latin_name='Panthera tigris altaica',
            general_viewing_tips='Look near the shaded areas.',
            seasonal_viewing_tips='Most active on cool days.',
            identification='Orange coat with black stripes.',
            habitat_and_range='Temperate forests.',
            diet_and_feeding='Carnivore.',
            behaviour_and_life_cycle='Solitary and territorial.',
            adaptations='Thick winter coat.',
            reproduction_and_life_cycle='Cubs stay with mother.',
            animals_at_the_zoo='One male tiger.',
            exhibit='Eurasia Wilds',
            seasonal_viewing_summary='Good spring and fall viewing.',
            seasonal_viewing_information='Indoor access during extreme weather.',
            off_display_message='Temporarily resting.',
            enclosure_type='Outdoor',
            x_coord=12,
            y_coord=34,
            has_limited_viewing_schedule=1,
            limited_viewing_message='Visible from 10:00 AM to 2:00 PM.',
            has_viewing_alert=1,
            viewing_alert_message='May be difficult to spot.',
            likelihood=85 )
      ],
      attractions=[
         {
            'name': 'Carousel',
            'type': 'customAttraction',
            'is_closed': False,
            'is_deleted': False
         }
      ],
      guardians_talks=[
         GuardiansTalk(
            name='Tiger Talk',
            location='Eurasia Wilds',
            x_coord=1,
            y_coord=2,
            start_time='10:00',
            maximum_duration=30,
            is_available=1 )
      ],
      wild_encounters=[
         WildEncounter(
            name='Encounter',
            meeting_spot='Spot',
            link='link',
            start_time='14:00',
            maximum_duration=30,
            is_available=0,
            unavailable_message='Unavailable.' )
      ]
   )

   result = itinerary.to_dict()

   assert result == {
      'date': '2026-06-15',
      'arrival_time': None,
      'departure_time': None,
      'animals': [
         {
            'species': 'Amur Tiger',
            'latin_name': 'Panthera tigris altaica',
            'general_viewing_tips': 'Look near the shaded areas.',
            'seasonal_viewing_tips': 'Most active on cool days.',
            'identification': 'Orange coat with black stripes.',
            'habitat_and_range': 'Temperate forests.',
            'diet_and_feeding': 'Carnivore.',
            'behaviour_and_life_cycle': 'Solitary and territorial.',
            'adaptations': 'Thick winter coat.',
            'reproduction_and_life_cycle': 'Cubs stay with mother.',
            'animals_at_the_zoo': 'One male tiger.',
            'exhibit': 'Eurasia Wilds',
            'seasonal_viewing_summary': 'Good spring and fall viewing.',
            'seasonal_viewing_information': 'Indoor access during extreme weather.',
            'off_display_message': 'Temporarily resting.',
            'enclosure_type': 'Outdoor',
            'x_coord': 12,
            'y_coord': 34,
            'likelihood': 85,
            'has_limited_viewing_schedule': True,
            'limited_viewing_message': 'Visible from 10:00 AM to 2:00 PM.',
            'has_viewing_alert': True,
            'viewing_alert_message': 'May be difficult to spot.',
            'is_deleted': False,
            'old_likelihood': None,
            'is_added': False,
            'start_time': None,
            'end_time': None,
            'type': 'animal'
         }
      ],
      'attractions': [
         {
            'name': 'Carousel',
            'type': 'customAttraction',
            'is_closed': False,
            'is_deleted': False
         }
      ],
      'guardians_talks': [
         {
            'name': 'Tiger Talk',
            'location': 'Eurasia Wilds',
            'x_coord': 1,
            'y_coord': 2,
            'start_time': '10:00',
            'maximum_duration': 30,
            'end_time': None,
            'is_available': True,
            'unavailable_message': None,
            'is_deleted': False,
            'type': 'guardiansTalk'
         }
      ],
      'wild_encounters': [
         {
            'name': 'Encounter',
            'meeting_spot': 'Spot',
            'link': 'link',
            'start_time': '14:00',
            'maximum_duration': 30,
            'end_time': None,
            'x_coord': None,
            'y_coord': None,
            'is_available': False,
            'unavailable_message': 'Unavailable.',
            'is_deleted': False,
            'type': 'wildEncounter'
         }
      ],
      'events': []
   }


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

   assert itinerary.animals[ 0 ].start_time == '10:00'
   assert itinerary.attractions[ 0 ].end_time == '11:30'
   assert itinerary.guardians_talks[ 0 ].start_time == '12:00'
   assert itinerary.wild_encounters[ 0 ].end_time == '13:45'
   assert itinerary.events[ 0 ].to_dict() == {
      'event_type': 'lunch',
      'start_time': '14:00',
      'end_time': '14:30',
      'type': 'itineraryEvent',
   }


def test_itinerary_config_exposes_event_types() -> None:
   assert itinerary_config_to_dict()[ 'itinerary_event_types' ] == [
      event_type.value for event_type in ItineraryEventType
   ]


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
      ( 1, 1 ),
      ( '1', None ),
      ( 'January', 1 ),
      ( 'Jan', 1 ),
      ( 'JAN', 1 ),
      ( 'September', 9 ),
      ( 'december', None ),
      ( 13, None ),
      ( None, None )
   ]
)
def test_normalize_month_documents_current_inputs(
      value: MonthInput,
      expected: VisitMonth | None ) -> None:
   assert CalendarDates.normalize_month( value ) == expected


@pytest.mark.parametrize(
   'value, expected',
   [
      ( 1, 'Jan' ),
      ( '1', 'Jan' ),
      ( 'January', 'Jan' ),
      ( 'sept', 'Sep' ),
      ( 'DECEMBER', 'Dec' )
   ]
)
def test_get_month_abbreviation( value: MonthInput, expected: str ) -> None:
   assert CalendarDates.get_month_abbreviation( value ) == expected


def test_get_month_abbreviation_rejects_invalid_values() -> None:
   with pytest.raises( ValueError ):
      CalendarDates.get_month_abbreviation( 13 )


@pytest.mark.parametrize(
   'value, expected',
   [
      ( 1, 1 ),
      ( 6, 6 ),
      ( '06', 6 ),
      ( 'June', 6 ),
      ( 'JUN', 6 ),
      ( 'January', 1 ),
      ( 'december', 12 ),
   ]
)
def test_resolve_visit_calendar_month_returns_int_one_through_twelve(
      value: MonthInput,
      expected: VisitMonth ) -> None:
   got = CalendarDates.resolve_visit_calendar_month( value )
   assert got == expected
   assert isinstance( got, int )


def test_resolve_visit_calendar_month_rejects_invalid_values() -> None:
   with pytest.raises( ValueError ):
      CalendarDates.resolve_visit_calendar_month( 13 )


def test_resolve_visit_day_of_month() -> None:
   assert CalendarDates.resolve_visit_day_of_month( '15' ) == 15
   assert CalendarDates.resolve_visit_day_of_month( 7 ) == 7


def test_resolve_visit_calendar_year_explicit() -> None:
   assert CalendarDates.resolve_visit_calendar_year( 2029 ) == 2029


def test_resolve_visit_calendar_year_none_uses_module_datetime( monkeypatch: pytest.MonkeyPatch ) -> None:
   from datetime import datetime as std_datetime

   class Fixed( std_datetime ):
      @classmethod
      def now( cls, tz: datetime.tzinfo | None = None ) -> datetime:
         return std_datetime( 2032, 3, 1, 0, 0, 0 )

   monkeypatch.setattr( date_values, 'datetime', Fixed )
   assert CalendarDates.resolve_visit_calendar_year( None ) == 2032


def test_visit_target_date() -> None:
   from datetime import date as date_cls

   assert CalendarDates.visit_target_date( 'June', 15, 2026 ) == date_cls( 2026, 6, 15 )
   assert CalendarDates.visit_target_date( 6, 15, 2026 ) == date_cls( 2026, 6, 15 )
   assert CalendarDates.visit_target_date( 'January', 10, '2028' ) == date_cls( 2028, 1, 10 )


def test_schedule_includes_weekday_monday_first() -> None:
   flags = ( True, False, False, False, False, False, False )

   assert CalendarDates.schedule_includes_weekday( 0, flags ) is True
   assert CalendarDates.schedule_includes_weekday( 1, flags ) is False


def test_schedule_includes_weekday_rejects_bad_index() -> None:
   flags = ( True, ) * 7

   assert CalendarDates.schedule_includes_weekday( -1, flags ) is False
   assert CalendarDates.schedule_includes_weekday( 7, flags ) is False


def test_temperature_helpers_are_stable() -> None:
   assert Weather.get_average_temperature( 'Jan', 1 ) == -5.0
   assert Weather.get_average_temperature( 'Jul', 1 ) == 26.0
   assert Weather.get_temperature_probability( mu=20, sigma=2, min_temperature=20 ) == 0.5
   assert Weather.get_temperature_probability( mu=25, sigma=2, min_temperature=20 ) > 0.99


def test_calendar_helpers_for_fixed_years() -> None:
   assert CalendarDates.get_family_day( 2026 ) == date( 2026, 2, 16 )
   assert CalendarDates.get_good_friday( 2026 ) == date( 2026, 4, 3 )
   assert CalendarDates.get_victoria_day( 2026 ) == date( 2026, 5, 18 )
   assert CalendarDates.get_civic_holiday( 2026 ) == date( 2026, 8, 3 )
   assert CalendarDates.get_labour_day( 2026 ) == date( 2026, 9, 7 )
   assert CalendarDates.get_thanksgiving( 2026 ) == date( 2026, 10, 12 )
   assert CalendarDates.is_holiday( date( 2026, 12, 25 ) ) is True
   assert CalendarDates.is_holiday( date( 2026, 12, 24 ) ) is False

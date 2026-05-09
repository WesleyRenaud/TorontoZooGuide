from datetime import date

import pytest

import zoo


def test_domain_objects_serialize_to_frontend_shapes():
   assert zoo.Pavilion( name='Pavilion', region='Region', x_coord=1, y_coord=2 ).to_dict() == {
      'name': 'Pavilion',
      'region': 'Region',
      'description': None,
      'x_coord': 1,
      'y_coord': 2
   }

   assert zoo.Restaurant(
      name='Cafe',
      location='North',
      sub_location='Inside',
      is_closed=1,
      likelihood=0
   ).to_dict()[ 'is_closed' ] is True

   assert zoo.GiftShop( name='Shop', location='Gate', is_closed=0 ).to_dict()[ 'is_closed' ] is False
   assert zoo.Attraction( name='Ride', free_with_admission=1 ).to_dict()[ 'free_with_admission' ] is True
   assert zoo.Restroom( title='Restroom', x_coord=3, y_coord=4 ).to_dict()[ 'title' ] == 'Restroom'
   assert zoo.ZoomobileStation( name='Station' ).to_dict()[ 'name' ] == 'Station'
   assert zoo.ZoomobileRouteMarker( route_type='summer', x_coord=1, y_coord=2 ).to_dict()[ 'route_type' ] == 'summer'
   assert zoo.GuardiansTalk( name='Talk', location='Habitat', x_coord=1, y_coord=2 ).to_dict()[ 'is_available' ] is True
   assert zoo.WildEncounter( name='Encounter', meeting_spot='Spot', link='https://example.test' ).to_dict()[ 'is_available' ] is True
   assert zoo.DrinkingFountain( x_coord=1, y_coord=2, is_closed=1, likelihood=0.0 ).to_dict() == {
      'x_coord': 1,
      'y_coord': 2,
      'is_closed': True,
      'closed_message': None,
      'likelihood': 0.0
   }
   assert zoo.Defibrillator( x_coord=5, y_coord=6 ).to_dict() == {
      'x_coord': 5,
      'y_coord': 6
   }
   assert zoo.EmergencyIntercom( x_coord=7, y_coord=8 ).to_dict() == {
      'x_coord': 7,
      'y_coord': 8
   }
   assert zoo.GuestService(
      service_type='Information',
      x_coord=9,
      y_coord=10
   ).to_dict() == {
      'service_type': 'Information',
      'x_coord': 9,
      'y_coord': 10
   }
   assert zoo.PicnicSite(
      x_coord=11,
      y_coord=12
   ).to_dict() == {
      'x_coord': 11,
      'y_coord': 12
   }
   assert zoo.EventSite(
      name='Special Events Center',
      x_coord=13,
      y_coord=14
   ).to_dict() == {
      'name': 'Special Events Center',
      'x_coord': 13,
      'y_coord': 14
   }
   assert zoo.Update(
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


def test_animal_to_dict_converts_boolean_flags():
   animal = zoo.Animal(
      species='Amur Tiger',
      has_limited_viewing_schedule=1,
      has_viewing_alert=0
   )

   result = animal.to_dict()

   assert result[ 'species' ] == 'Amur Tiger'
   assert result[ 'has_limited_viewing_schedule' ] is True
   assert result[ 'has_viewing_alert' ] is False


def test_itinerary_serializes_objects_and_dicts_with_types():
   itinerary = zoo.Itinerary(
      date='2026-06-15',
      animals=[
         zoo.Animal(
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
            'is_closed': False
         }
      ],
      guardians_talks=[
         zoo.GuardiansTalk(
            name='Tiger Talk',
            location='Eurasia Wilds',
            x_coord=1,
            y_coord=2,
            time_of_day='10:00',
            maximum_duration=30,
            is_available=1 )
      ],
      wild_encounters=[
         zoo.WildEncounter(
            name='Encounter',
            meeting_spot='Spot',
            link='link',
            time_of_day='14:00',
            maximum_duration=30,
            is_available=0,
            unavailable_message='Unavailable.' )
      ]
   )

   result = itinerary.to_dict()

   assert result == {
      'date': '2026-06-15',
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
            'type': 'animal'
         }
      ],
      'attractions': [
         {
            'name': 'Carousel',
            'type': 'customAttraction',
            'is_closed': False
         }
      ],
      'guardians_talks': [
         {
            'name': 'Tiger Talk',
            'location': 'Eurasia Wilds',
            'x_coord': 1,
            'y_coord': 2,
            'time_of_day': '10:00',
            'maximum_duration': 30,
            'start_time': None,
            'end_time': None,
            'is_available': True,
            'unavailable_message': None,
            'type': 'guardiansTalk'
         }
      ],
      'wild_encounters': [
         {
            'name': 'Encounter',
            'meeting_spot': 'Spot',
            'link': 'link',
            'time_of_day': '14:00',
            'maximum_duration': 30,
            'start_time': None,
            'end_time': None,
            'x_coord': None,
            'y_coord': None,
            'is_available': False,
            'unavailable_message': 'Unavailable.',
            'type': 'wildEncounter'
         }
      ]
   }


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
def test_as_boolean( value, expected ):
   assert zoo.ZooUtil.as_boolean( value ) is expected


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
def test_normalize_month_documents_current_inputs( value, expected ):
   assert zoo.ZooUtil.normalize_month( value ) == expected


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
def test_get_month_abbreviation( value, expected ):
   assert zoo.ZooUtil.get_month_abbreviation( value ) == expected


def test_get_month_abbreviation_rejects_invalid_values():
   with pytest.raises( ValueError ):
      zoo.ZooUtil.get_month_abbreviation( 13 )


def test_temperature_helpers_are_stable():
   assert zoo.ZooUtil.get_average_temperature( 'Jan', 1 ) == -5.0
   assert zoo.ZooUtil.get_average_temperature( 'Jul', 1 ) == 26.0
   assert zoo.ZooUtil.get_temperature_probability( mu=20, sigma=2, min_temperature=20 ) == 0.5
   assert zoo.ZooUtil.get_temperature_probability( mu=25, sigma=2, min_temperature=20 ) > 0.99


def test_calendar_helpers_for_fixed_years():
   assert zoo.ZooUtil.get_family_day( 2026 ) == date( 2026, 2, 16 )
   assert zoo.ZooUtil.get_good_friday( 2026 ) == date( 2026, 4, 3 )
   assert zoo.ZooUtil.get_victoria_day( 2026 ) == date( 2026, 5, 18 )
   assert zoo.ZooUtil.get_civic_holiday( 2026 ) == date( 2026, 8, 3 )
   assert zoo.ZooUtil.get_labour_day( 2026 ) == date( 2026, 9, 7 )
   assert zoo.ZooUtil.get_thanksgiving( 2026 ) == date( 2026, 10, 12 )
   assert zoo.ZooUtil.is_holiday( date( 2026, 12, 25 ) ) is True
   assert zoo.ZooUtil.is_holiday( date( 2026, 12, 24 ) ) is False

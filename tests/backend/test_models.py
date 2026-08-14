from __future__ import annotations

from api.models import Animal
from api.models import Attraction
from api.models import Defibrillator
from api.models import DrinkingFountain
from api.models import EmergencyIntercom
from api.models import Event
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
from api.models import ZoomobileRouteMarker
from api.models import ZoomobileStation
from api.models.guardians_talk_linked_animal import GuardiansTalkLinkedAnimal


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
   assert Attraction(
      name='Ride',
      free_with_admission=1,
      region='Front Courtyard',
   ).to_dict()[ 'free_with_admission' ] is True
   assert Attraction(
      name='Ride',
      free_with_admission=1,
      region='Front Courtyard',
   ).to_dict()[ 'region' ] == 'Front Courtyard'
   assert Attraction( name='Ride', free_with_admission=1 ).to_dict()[ 'is_deleted' ] is False
   assert Attraction(
      name='Zoomobile',
      free_with_admission=0,
      is_also_transportation=1,
   ).to_dict()[ 'is_also_transportation' ] is True
   assert Attraction(
      name='Ride',
      free_with_admission=1,
   ).to_dict()[ 'is_also_transportation' ] is False
   assert Restroom( title='Restroom', x_coord=3, y_coord=4 ).to_dict()[ 'title' ] == 'Restroom'
   assert ZoomobileStation(
      name='Station',
      description='Stop',
      x_coord=1.0,
      y_coord=2.0,
   ).to_dict()[ 'name' ] == 'Station'
   assert ZoomobileRouteMarker( route_type='summer', x_coord=1, y_coord=2 ).to_dict()[ 'route_type' ] == 'summer'
   assert GuardiansTalk( name='Talk', location='Habitat', x_coord=1, y_coord=2 ).to_dict()[ 'is_available' ] is True
   assert GuardiansTalk( name='Talk', location='Habitat', x_coord=1, y_coord=2 ).to_dict()[ 'is_deleted' ] is False
   assert WildEncounter(
      name='Encounter',
      meeting_spot='Spot',
      link='https://example.test',
      region='Africa',
   ).to_dict()[ 'is_available' ] is True
   assert WildEncounter(
      name='Encounter',
      meeting_spot='Spot',
      link='https://example.test',
      region='Africa',
   ).to_dict()[ 'region' ] == 'Africa'
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
   assert Event(
      name='Conservation Carousel Ride Night',
      location='Front Courtyard',
      description='Evening carousel rides for a special cause.',
      link='https://www.torontozoo.com/events/carousel-night',
      start_date='2026-06-15',
      end_date='2026-06-30'
   ).to_dict() == {
      'name': 'Conservation Carousel Ride Night',
      'location': 'Front Courtyard',
      'description': 'Evening carousel rides for a special cause.',
      'link': 'https://www.torontozoo.com/events/carousel-night',
      'start_date': '2026-06-15',
      'end_date': '2026-06-30'
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
      viewing_alert_messages=[]
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
            viewing_alert_messages=[ 'May be difficult to spot.' ],
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
            start_time='10:00 AM',
            maximum_duration=30,
            is_available=1,
            linked_animals=[
               GuardiansTalkLinkedAnimal(
                  species='Amur Tiger',
                  exhibit='Eurasia Wilds' ),
            ] )
      ],
      wild_encounters=[
         WildEncounter(
            name='Encounter',
            meeting_spot='Spot',
            link='link',
            start_time='2:00 PM',
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
      'selected_exhibits': [],
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
            'enclosure_name': None,
            'x_coord': 12,
            'y_coord': 34,
            'likelihood': 85,
            'has_limited_viewing_schedule': True,
            'limited_viewing_message': 'Visible from 10:00 AM to 2:00 PM.',
            'has_viewing_alert': True,
            'viewing_alert_messages': [ 'May be difficult to spot.' ],
            'is_deleted': False,
            'old_likelihood': None,
            'is_added': False,
            'covered_by_talk': False,
            'start_time': None,
            'end_time': None,
            'viewing_walk_node_id': None,
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
            'start_time': '10:00 AM',
            'maximum_duration': 30,
            'end_time': None,
            'is_available': True,
            'unavailable_message': None,
            'is_deleted': False,
            'linked_animals': [
               {
                  'species': 'Amur Tiger',
                  'exhibit': 'Eurasia Wilds',
               },
            ],
            'type': 'guardiansTalk'
         }
      ],
      'wild_encounters': [
         {
            'name': 'Encounter',
            'meeting_spot': 'Spot',
            'link': 'link',
            'start_time': '2:00 PM',
            'maximum_duration': 30,
            'end_time': None,
            'x_coord': None,
            'y_coord': None,
            'region': None,
            'is_available': False,
            'unavailable_message': 'Unavailable.',
            'is_deleted': False,
            'type': 'wildEncounter'
         }
      ],
      'events': []
   }

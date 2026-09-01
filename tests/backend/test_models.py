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
from api.models import Pavilion
from api.models import PicnicSite
from api.models import Restaurant
from api.models import Restroom
from api.models import TransportationRouteMarker
from api.models import TransportationStation
from api.models import Update
from api.models import WildEncounter


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
   assert TransportationStation(
      name='Station',
      description='Stop',
      x_coord=1.0,
      y_coord=2.0,
   ).to_dict()[ 'name' ] == 'Station'
   assert TransportationRouteMarker( route_type='summer', x_coord=1, y_coord=2 ).to_dict()[ 'route_type' ] == 'summer'
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

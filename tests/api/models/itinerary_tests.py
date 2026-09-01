from __future__ import annotations

from api.models import Animal
from api.models import GuardiansTalk
from api.models import Itinerary
from api.models import WildEncounter
from api.models.guardians_talk_linked_animal import GuardiansTalkLinkedAnimal


def Test_ToDict_TestMixedObjectsAndDicts_ExpectSerializedItinerary() -> None:
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

   assert itinerary.to_dict() == {
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
      'transportations': [],
      'transportation_stations': [],
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

from __future__ import annotations

from api.models import Animal
from api.models import GuardiansTalk
from api.models import Itinerary
from api.models import WildEncounter
from api.models.guardians_talk_linked_animal import GuardiansTalkLinkedAnimal
from api.shared.enums.item_type import ItemType
from api.shared.typed_dict_mapper import TypedDictMapper


def Test_ToDict_TestMixedObjectsAndDicts_ExpectSerializedItinerary() -> None:
   animal = Animal(
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
   attraction = {
      'name': 'Carousel',
      'type': 'customAttraction',
      'is_closed': False,
      'is_deleted': False
   }
   talk = GuardiansTalk(
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
   encounter = WildEncounter(
      name='Encounter',
      meeting_spot='Spot',
      link='link',
      start_time='2:00 PM',
      maximum_duration=30,
      is_available=0,
      unavailable_message='Unavailable.' )
   itinerary = Itinerary(
      date='2026-06-15',
      animals=[ animal ],
      attractions=[ attraction ],
      guardians_talks=[ talk ],
      wild_encounters=[ encounter ] )

   result = itinerary.to_dict()

   assert result[ 'date' ] == itinerary.date
   assert result[ 'arrival_time' ] == itinerary.arrival_time
   assert result[ 'departure_time' ] == itinerary.departure_time
   assert result[ 'selected_exhibits' ] == list( itinerary.selected_exhibits )
   assert result[ 'animals' ] == [
      TypedDictMapper.to_dict_with_type( itinerary_animal, ItemType.ANIMAL.value )
      for itinerary_animal in itinerary.animals
   ]
   assert result[ 'attractions' ] == [
      TypedDictMapper.to_dict_with_type( itinerary_attraction, ItemType.ATTRACTION.value )
      for itinerary_attraction in itinerary.attractions
   ]
   assert result[ 'transportations' ] == [
      TypedDictMapper.to_dict_with_type(
         transportation,
         ItemType.TRANSPORTATION.value )
      for transportation in itinerary.transportations
   ]
   assert result[ 'transportation_stations' ] == [
      station.to_dict() for station in itinerary.transportation_stations
   ]
   assert result[ 'guardians_talks' ] == [
      TypedDictMapper.to_dict_with_type( itinerary_talk, ItemType.GUARDIANS_TALK.value )
      for itinerary_talk in itinerary.guardians_talks
   ]
   assert result[ 'wild_encounters' ] == [
      TypedDictMapper.to_dict_with_type(
         itinerary_encounter,
         ItemType.WILD_ENCOUNTER.value )
      for itinerary_encounter in itinerary.wild_encounters
   ]
   assert result[ 'events' ] == [
      TypedDictMapper.to_dict_with_type( event, ItemType.ITINERARY_EVENT.value )
      for event in itinerary.events
   ]

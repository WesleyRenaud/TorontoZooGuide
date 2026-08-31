from __future__ import annotations

from api.itinerary.data_access.itinerary_save_input_mapper import ItinerarySaveInputMapper
from api.itinerary.data_access.itinerary_transportation_input import ItineraryTransportationInput
from api.itinerary.wild_encounter_schedule_item_key import WildEncounterScheduleItemKey


def Test_MapNamedStrings_TestWhitespaceAndEmpty_ExpectTrimmedNonEmpty() -> None:
   assert ItinerarySaveInputMapper.map_named_strings(
      [ '  Africa Savanna  ', '', '  ', 'Canadian Domain' ] ) == [
      'Africa Savanna',
      'Canadian Domain',
   ]


def Test_MapAnimalInputs_TestEnclosureOptional_ExpectInputs() -> None:
   animals = ItinerarySaveInputMapper.map_animal_inputs(
      [
         {
            'species': 'African Lion',
            'exhibit': 'Africa Savanna',
         },
         {
            'species': 'African Penguin',
            'exhibit': 'Africa Savanna',
            'enclosure_name': 'Outdoor',
         },
      ] )

   assert [
      ( animal.species, animal.exhibit, animal.enclosure_name )
      for animal in animals
   ] == [
      ( 'African Lion', 'Africa Savanna', None ),
      ( 'African Penguin', 'Africa Savanna', 'Outdoor' ),
   ]


def Test_MapGuardiansTalkInputs_TestTimes_ExpectNormalizedInputs() -> None:
   talks = ItinerarySaveInputMapper.map_guardians_talk_inputs(
      [
         {
            'name': "Grevy's Zebra",
            'start_time': '12:00',
            'end_time': '12:30',
         },
      ] )

   assert talks[ 0 ].name == "Grevy's Zebra"
   assert talks[ 0 ].start_time == '12:00 PM'
   assert talks[ 0 ].end_time == '12:30 PM'


def Test_MapItinerarySaveInput_TestWireFields_ExpectSaveInput() -> None:
   save_input = ItinerarySaveInputMapper.map_itinerary_save_input(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      selected_exhibits=[ ' Africa Savanna ' ],
      animals=[
         {
            'species': 'African Lion',
            'exhibit': 'Africa Savanna',
         },
      ],
      attractions=[ ' Conservation Carousel ' ],
      guardians_talks=[
         {
            'name': "Grevy's Zebra",
            'start_time': '12:00',
            'end_time': None,
         },
      ],
      wild_encounters=[
         WildEncounterScheduleItemKey( name='African Rainforest', start_time='14:00' ),
      ],
      transportations=[
         ItineraryTransportationInput( name='Zoomobile', added_as_attraction=False ),
      ],
   )

   assert save_input.date.isoformat() == '2026-06-15'
   assert save_input.arrival_time == '9:30 AM'
   assert save_input.departure_time == '5:00 PM'
   assert save_input.selected_exhibits == [ 'Africa Savanna' ]
   assert save_input.attractions == [ 'Conservation Carousel' ]
   assert len( save_input.animals ) == 1
   assert len( save_input.guardians_talks ) == 1
   assert len( save_input.wild_encounters ) == 1
   assert save_input.transportations[ 0 ].name == 'Zoomobile'

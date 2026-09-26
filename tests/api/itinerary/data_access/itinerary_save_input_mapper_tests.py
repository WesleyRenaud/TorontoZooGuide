from __future__ import annotations

from api.itinerary.data_access.itinerary_save_input_mapper import ItinerarySaveInputMapper
from api.itinerary.data_access.itinerary_transportation_input import ItineraryTransportationInput
from api.itinerary.wild_encounter_schedule_item_key import WildEncounterScheduleItemKey
from api.shared.date_values import DateValues
from api.shared.enums.position import Position
from api.shared.enums.transportation_name import TransportationName


def Test_MapNamedStrings_TestWhitespaceAndEmpty_ExpectTrimmedNonEmpty() -> None:
   savanna = 'Africa Savanna'
   domain = 'Canadian Domain'
   names = [ f'  { savanna }  ', '', '  ', domain ]

   mapped = ItinerarySaveInputMapper.map_named_strings( names )

   assert mapped == [ savanna, domain ]


def Test_MapAnimalInputs_TestEnclosureOptional_ExpectInputs() -> None:
   lion_species = 'African Lion'
   penguin_species = 'African Penguin'
   exhibit = 'Africa Savanna'
   enclosure_name = 'Outdoor'
   animals = [
      {
         'species': lion_species,
         'exhibit': exhibit,
      },
      {
         'species': penguin_species,
         'exhibit': exhibit,
         'enclosure_name': enclosure_name,
      },
   ]

   mapped = ItinerarySaveInputMapper.map_animal_inputs( animals )

   assert mapped[ Position.FIRST ].species == lion_species
   assert mapped[ Position.FIRST ].exhibit == exhibit
   assert mapped[ Position.FIRST ].enclosure_name is None
   assert mapped[ Position.SECOND ].species == penguin_species
   assert mapped[ Position.SECOND ].exhibit == exhibit
   assert mapped[ Position.SECOND ].enclosure_name == enclosure_name


def Test_MapGuardiansTalkInputs_TestTimes_ExpectNormalizedInputs() -> None:
   talk_name = "Grevy's Zebra"
   start_time = '12:00'
   duration_minutes = 30
   end_time = DateValues.add_minutes_to_time( start_time, duration_minutes )
   talks = [
      {
         'name': talk_name,
         'start_time': start_time,
         'end_time': end_time,
      },
   ]

   mapped = ItinerarySaveInputMapper.map_guardians_talk_inputs( talks )

   talk = mapped[ Position.FIRST ]
   assert talk.name == talk_name
   assert talk.start_time == DateValues.normalize_itinerary_schedule_time(
      start_time )
   assert talk.end_time == end_time


def Test_MapItinerarySaveInput_TestWireFields_ExpectSaveInput() -> None:
   visit_date = '2026-06-15'
   arrival_time = '09:30'
   departure_time = '17:00'
   exhibit = 'Africa Savanna'
   attraction = 'Conservation Carousel'
   talk_name = "Grevy's Zebra"
   talk_start_time = '12:00'
   encounter_name = 'African Rainforest'
   encounter_start_time = '14:00'
   transportation = TransportationName.ZOOMOBILE
   species = 'African Lion'
   selected_exhibits = [ f' { exhibit } ' ]
   attractions = [ f' { attraction } ' ]
   animals = [
      {
         'species': species,
         'exhibit': exhibit,
      },
   ]
   guardians_talks = [
      {
         'name': talk_name,
         'start_time': talk_start_time,
         'end_time': None,
      },
   ]
   wild_encounters = [
      WildEncounterScheduleItemKey(
         name=encounter_name,
         start_time=encounter_start_time ),
   ]
   transportations = [
      ItineraryTransportationInput(
         name=transportation,
         added_as_attraction=False ),
   ]

   save_input = ItinerarySaveInputMapper.map_itinerary_save_input(
      date=visit_date,
      arrival_time=arrival_time,
      departure_time=departure_time,
      selected_exhibits=selected_exhibits,
      animals=animals,
      attractions=attractions,
      guardians_talks=guardians_talks,
      wild_encounters=wild_encounters,
      transportations=transportations )

   assert save_input.date == DateValues.parse_date_value( visit_date )
   assert save_input.arrival_time == DateValues.normalize_itinerary_schedule_time(
      arrival_time )
   assert save_input.departure_time == DateValues.normalize_itinerary_schedule_time(
      departure_time )
   assert save_input.selected_exhibits == ItinerarySaveInputMapper.map_named_strings(
      selected_exhibits )
   assert save_input.attractions == ItinerarySaveInputMapper.map_named_strings(
      attractions )
   assert len( save_input.animals ) == len( animals )
   assert len( save_input.guardians_talks ) == len( guardians_talks )
   assert len( save_input.wild_encounters ) == len( wild_encounters )
   assert save_input.transportations[ Position.FIRST ].name == transportation

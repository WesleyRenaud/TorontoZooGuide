from __future__ import annotations

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.data_access.itinerary_transportation_record import ItineraryTransportationRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.scheduling.bulk.bulk_schedule_stop_selector import BulkScheduleStopSelector


CAROUSEL = 'Conservation Carousel'
ZOOMOBILE = 'Zoomobile'
AFRICAN_RAINFOREST_PAVILION = 'African Rainforest Pavilion'
ALDABRA_INDOOR_ENCLOSURE = 'Ring-Tailed Lemur Enclosure'


def _saved() -> SavedItinerary:
   return SavedItinerary(
      date_value='2026-06-20',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animal_rows=[
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100,
            start_time='10:00 AM',
            end_time='10:08 AM' ),
         ItineraryAnimalRecord(
            species='Cheetah',
            exhibit='Indo-Malaya Outdoor',
            old_likelihood=None,
            new_likelihood=100 ),
      ],
      attraction_rows=[
         ItineraryAttractionRecord(
            attraction=CAROUSEL,
            old_likelihood=None,
            new_likelihood=100 ),
      ],
      transportation_rows=[
         ItineraryTransportationRecord(
            transportation=ZOOMOBILE,
            old_likelihood=None,
            new_likelihood=100,
            added_as_attraction=True,
            start_time='11:00 AM',
            end_time='11:20 AM' ),
         ItineraryTransportationRecord(
            transportation=ZOOMOBILE,
            old_likelihood=None,
            new_likelihood=100,
            added_as_attraction=False ),
      ],
   )


def Test_Attractions_TestNone_ExpectEmpty() -> None:
   assert BulkScheduleStopSelector.attractions(
      None,
      only_previously_scheduled=False ) == []
   assert BulkScheduleStopSelector.stops(
      None,
      only_previously_scheduled=False ) == []


def Test_Attractions_TestAllVersusScheduledOnly_ExpectFiltered() -> None:
   saved = _saved()

   assert [
      attraction.attraction
      for attraction in BulkScheduleStopSelector.attractions(
         saved,
         only_previously_scheduled=False )
   ] == [ CAROUSEL ]
   assert BulkScheduleStopSelector.attractions(
      saved,
      only_previously_scheduled=True ) == []


def Test_Animals_TestScheduledOnly_ExpectTimedAnimals() -> None:
   assert [
      animal.species
      for animal in BulkScheduleStopSelector.animals(
         _saved(),
         only_previously_scheduled=True )
   ] == [ 'African Lion' ]


def Test_Transportations_TestAttractionModeOnly_ExpectAttractionModeRows() -> None:
   assert [
      ( row.transportation, row.added_as_attraction )
      for row in BulkScheduleStopSelector.transportations(
         _saved(),
         only_previously_scheduled=False )
   ] == [ ( ZOOMOBILE, True ) ]


def Test_TransitTransportations_TestTransitMode_ExpectTransitRows() -> None:
   assert [
      ( row.transportation, row.added_as_attraction )
      for row in BulkScheduleStopSelector.transit_transportations( _saved() )
   ] == [ ( ZOOMOBILE, False ) ]


def Test_StopsMatchingPrevious_TestPreviouslyScheduledSpecies_ExpectPostSaveRows() -> None:
   before = SavedItinerary(
      date_value='2026-06-20',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animal_rows=[
         ItineraryAnimalRecord(
            species='Aldabra Tortoise',
            exhibit='Australasia Pavilion',
            enclosure_name='Outdoor',
            old_likelihood=None,
            new_likelihood=100,
            start_time='10:00 AM',
            end_time='10:08 AM' ),
      ],
   )
   after = SavedItinerary(
      date_value='2026-06-20',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animal_rows=[
         ItineraryAnimalRecord(
            species='Aldabra Tortoise',
            exhibit='Australasia Pavilion',
            enclosure_name='Indoor',
            old_likelihood=None,
            new_likelihood=100 ),
      ],
   )

   stops = BulkScheduleStopSelector.stops_matching_previous( before, after )

   assert [
      ( animal.species, animal.enclosure_name )
      for animal in stops
   ] == [ ( 'Aldabra Tortoise', 'Indoor' ) ]


def Test_StopsMatchingPrevious_TestLionScheduledPenguinNot_ExpectLionOnly() -> None:
   before = SavedItinerary(
      date_value='2026-06-20',
      arrival_time='9:00 AM',
      departure_time='5:00 PM',
      animal_rows=[
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100,
            start_time='10:00 AM',
            end_time='10:08 AM' ),
         ItineraryAnimalRecord(
            species='African Penguin',
            exhibit='Africa Savanna',
            enclosure_name='Outdoor',
            old_likelihood=None,
            new_likelihood=100 ),
      ],
   )
   after = SavedItinerary(
      date_value='2026-06-20',
      arrival_time='9:00 AM',
      departure_time='5:00 PM',
      animal_rows=[
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100 ),
         ItineraryAnimalRecord(
            species='African Penguin',
            exhibit='Africa Savanna',
            enclosure_name='Outdoor',
            old_likelihood=None,
            new_likelihood=100 ),
      ],
   )

   stops = BulkScheduleStopSelector.stops_matching_previous( before, after )

   assert [ animal.species for animal in stops ] == [ 'African Lion' ]


def Test_StopsMatchingPrevious_TestAldabraRainforestOutdoorToIndoor_ExpectIndoorRow() -> None:
   before = SavedItinerary(
      date_value='2026-07-19',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animal_rows=[
         ItineraryAnimalRecord(
            species='Aldabra Tortoise',
            exhibit=AFRICAN_RAINFOREST_PAVILION,
            enclosure_name='Outdoor',
            old_likelihood=None,
            new_likelihood=100,
            start_time='10:00 AM',
            end_time='10:08 AM',
         ),
      ],
   )
   after = SavedItinerary(
      date_value='2026-07-20',
      arrival_time='11:00 AM',
      departure_time='5:00 PM',
      animal_rows=[
         ItineraryAnimalRecord(
            species='Aldabra Tortoise',
            exhibit=AFRICAN_RAINFOREST_PAVILION,
            enclosure_name=ALDABRA_INDOOR_ENCLOSURE,
            old_likelihood=None,
            new_likelihood=100,
         ),
      ],
   )

   stops = BulkScheduleStopSelector.stops_matching_previous( before, after )

   assert [
      ( animal.species, animal.enclosure_name )
      for animal in stops
   ] == [ ( 'Aldabra Tortoise', ALDABRA_INDOOR_ENCLOSURE ) ]


def Test_Stops_TestClearedAttractionSchedule_ExpectCarouselStillSelected() -> None:
   saved = SavedItinerary(
      date_value='2026-06-20',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animal_rows=[
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100,
            start_time='10:00 AM',
            end_time='10:08 AM' ),
      ],
      attraction_rows=[
         ItineraryAttractionRecord(
            attraction=CAROUSEL,
            old_likelihood=None,
            new_likelihood=100 ),
      ],
   )

   stops = BulkScheduleStopSelector.stops(
      saved,
      only_previously_scheduled=False )

   assert [
      attraction.attraction
      for attraction in BulkScheduleStopSelector.attractions(
         saved,
         only_previously_scheduled=False )
   ] == [ CAROUSEL ]
   assert BulkScheduleStopSelector.attractions(
      saved,
      only_previously_scheduled=True ) == []
   assert len( stops ) == 2


def Test_Stops_TestAllGuestStops_ExpectAnimalsAttractionsAndTransportation() -> None:
   stops = BulkScheduleStopSelector.stops(
      _saved(),
      only_previously_scheduled=False )

   assert [
      ( getattr( stop, 'species', None ), getattr( stop, 'attraction', None ), getattr( stop, 'transportation', None ) )
      for stop in stops
   ] == [
      ( 'African Lion', None, None ),
      ( 'Cheetah', None, None ),
      ( None, CAROUSEL, None ),
      ( None, ZOOMOBILE, ZOOMOBILE ),
   ]

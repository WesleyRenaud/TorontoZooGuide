from __future__ import annotations

from api.animals.search.species_exhibit_key_builder import SpeciesExhibitKeyBuilder
from api.animals.search.viewing_spot_key_builder import ViewingSpotKeyBuilder
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.shared.date_values import DateValues
from api.walk_graph.domain.master_route_stop_key_builder import MasterRouteStopKeyBuilder


def Test_SpeciesExhibitKey_TestRecord_ExpectNormalizedKey() -> None:
   species = 'African Lion'
   exhibit = 'Africa Savanna'
   start_time = '10:00 AM'
   duration_minutes = 8
   record = ItineraryAnimalRecord(
      species=species,
      exhibit=exhibit,
      start_time=start_time,
      end_time=DateValues.add_minutes_to_time( start_time, duration_minutes ) )

   key = record.species_exhibit_key()

   assert key == SpeciesExhibitKeyBuilder.from_values( record.species, record.exhibit )


def Test_ViewingSpotKey_TestRecordWithEnclosure_ExpectThreePartKey() -> None:
   species = 'African Penguin'
   exhibit = 'Africa Savanna'
   enclosure_name = 'Outdoor'
   record = ItineraryAnimalRecord(
      species=species,
      exhibit=exhibit,
      enclosure_name=enclosure_name )

   key = record.viewing_spot_key()

   assert key == ViewingSpotKeyBuilder.from_values(
      record.species,
      record.exhibit,
      record.enclosure_name )


def Test_MasterRouteStopKey_TestRecord_ExpectAnimalStopKey() -> None:
   species = 'African Lion'
   exhibit = 'Africa Savanna'
   start_time = '10:00 AM'
   duration_minutes = 8
   record = ItineraryAnimalRecord(
      species=species,
      exhibit=exhibit,
      start_time=start_time,
      end_time=DateValues.add_minutes_to_time( start_time, duration_minutes ) )

   stop_key = record.master_route_stop_key()

   assert stop_key == MasterRouteStopKeyBuilder.animal(
      record.species,
      record.exhibit,
      record.enclosure_name )

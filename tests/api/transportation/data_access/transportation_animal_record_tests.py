from __future__ import annotations

from api.animals.search.species_exhibit_key import SpeciesExhibitKey
from api.animals.search.viewing_spot_key_builder import ViewingSpotKeyBuilder
from api.transportation.data_access.transportation_animal_record import TransportationAnimalRecord


def Test_ViewingSpotKey_TestGiraffeOutdoor_ExpectNormalizedKey() -> None:
   record = TransportationAnimalRecord(
      transportation='Zoomobile',
      from_station='Canadian Domain Zoomobile Station',
      to_station='Africa Zoomobile Station',
      species='Masai Giraffe',
      exhibit='Africa Savanna',
      enclosure_name='Outdoor' )

   key = record.viewing_spot_key()

   assert key == ViewingSpotKeyBuilder.from_values(
      record.species,
      record.exhibit,
      record.enclosure_name )


def Test_LegKey_TestGiraffeOutdoor_ExpectStations() -> None:
   record = TransportationAnimalRecord(
      transportation='Zoomobile',
      from_station='Canadian Domain Zoomobile Station',
      to_station='Africa Zoomobile Station',
      species='Masai Giraffe',
      exhibit='Africa Savanna',
      enclosure_name='Outdoor' )

   key = record.leg_key()

   assert key == (
      record.transportation,
      record.from_station,
      record.to_station )


def Test_SpeciesExhibitKey_TestGiraffeOutdoor_ExpectNormalizedSpecies() -> None:
   record = TransportationAnimalRecord(
      transportation='Zoomobile',
      from_station='Canadian Domain Zoomobile Station',
      to_station='Africa Zoomobile Station',
      species='Masai Giraffe',
      exhibit='Africa Savanna',
      enclosure_name='Outdoor' )

   key = record.species_exhibit_key()

   assert key == SpeciesExhibitKey.from_values( record.species, record.exhibit )

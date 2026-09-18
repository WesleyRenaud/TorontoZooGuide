from __future__ import annotations

from api.shared.enums.position import Position
from api.transportation.data_access.transportation_animal_record import TransportationAnimalRecord


def Test_ViewingSpotAndLegKey_TestGiraffeOutdoor_ExpectNormalizedKeys() -> None:
   record = TransportationAnimalRecord(
      transportation='Zoomobile',
      from_station='Canadian Domain Zoomobile Station',
      to_station='Africa Zoomobile Station',
      species='Masai Giraffe',
      exhibit='Africa Savanna',
      enclosure_name='Outdoor' )

   assert record.viewing_spot_key()[ Position.FIRST ] == 'masai giraffe'
   assert record.leg_key() == (
      'Zoomobile',
      'Canadian Domain Zoomobile Station',
      'Africa Zoomobile Station',
   )
   assert record.species_exhibit_key().species == 'masai giraffe'

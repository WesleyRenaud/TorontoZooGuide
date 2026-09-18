from __future__ import annotations

from .transportation_animal_record import TransportationAnimalRecord
from ...types import Types


class TransportationAnimalMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> TransportationAnimalRecord:
      return TransportationAnimalRecord(
         transportation=row[ 'TRANSPORTATION' ],
         from_station=row[ 'FROM_STATION' ],
         to_station=row[ 'TO_STATION' ],
         species=row[ 'SPECIES' ],
         exhibit=row[ 'EXHIBIT' ],
         enclosure_name=row[ 'ENCLOSURE_NAME' ] )


   @classmethod
   def map_records( cls, rows: list[ Types.Row ] ) -> list[ TransportationAnimalRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]

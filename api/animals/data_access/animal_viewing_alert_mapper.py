from __future__ import annotations

from ..status.animal_viewing_alert import AnimalViewingAlert
from ...types import Types


class AnimalViewingAlertMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> AnimalViewingAlert:
      return AnimalViewingAlert(
         species=row[ 'SPECIES' ],
         exhibit=row[ 'EXHIBIT' ],
         start_date=row[ 'ALERT_START_DATE' ],
         end_date=row[ 'ALERT_END_DATE' ],
         message=row[ 'ALERT_MESSAGE' ] )


   @classmethod
   def map_records( cls, rows: list[ Types.Row ] ) -> list[ AnimalViewingAlert ]:
      return [
         cls.map_record( row )
         for row in rows
      ]

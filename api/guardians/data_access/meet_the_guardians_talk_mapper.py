from __future__ import annotations

from .meet_the_guardians_talk_record import MeetTheGuardiansTalkRecord
from ...types import Row


class MeetTheGuardiansTalkMapper():
   @classmethod
   def map_record( cls, row: Row ) -> MeetTheGuardiansTalkRecord:
      return MeetTheGuardiansTalkRecord(
         name=row[ 'NAME' ],
         location=row[ 'LOCATION' ],
         x_coord=row[ 'X_COORD' ],
         y_coord=row[ 'Y_COORD' ],
         maximum_duration=row[ 'MAXIMUM_DURATION' ] )


   @classmethod
   def map_records( cls, rows: list[ Row ] ) -> list[ MeetTheGuardiansTalkRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]

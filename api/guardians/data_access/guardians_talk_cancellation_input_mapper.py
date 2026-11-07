from __future__ import annotations

from ..cancellations.guardians_talk_cancellation_builder import GuardiansTalkCancellationBuilder
from ..cancellations.guardians_talk_cancellation_input import GuardiansTalkCancellationInput
from ...types import Types


class GuardiansTalkCancellationInputMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> GuardiansTalkCancellationInput:
      return GuardiansTalkCancellationBuilder.build(
         row[ 'TALK_NAME' ],
         row[ 'LOCATION' ],
         str( row[ 'CANCELLATION_DATE' ] ),
         row[ 'TALK_TIME' ],
         enclosure_name=row[ 'ENCLOSURE_NAME' ],
      )


   @classmethod
   def map_records( cls, rows: list[ Types.Row ] ) -> list[ GuardiansTalkCancellationInput ]:
      return [
         cls.map_record( row )
         for row in rows
      ]

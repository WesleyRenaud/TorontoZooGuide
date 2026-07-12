from __future__ import annotations

from collections.abc import Iterable

from .guardians_talk_animal_record import GuardiansTalkAnimalRecord
from ...types import Row


def map_guardians_talk_animal_record( row: Row ) -> GuardiansTalkAnimalRecord:
   return GuardiansTalkAnimalRecord(
      talk_name=row[ 'TALK_NAME' ],
      location=row[ 'LOCATION' ],
      species=row[ 'SPECIES' ],
      exhibit=row[ 'EXHIBIT' ],
      enclosure_name=row[ 'ENCLOSURE_NAME' ] )


def map_guardians_talk_animal_records(
      rows: Iterable[ Row ] ) -> list[ GuardiansTalkAnimalRecord ]:
   return [
      map_guardians_talk_animal_record( row )
      for row in rows
   ]

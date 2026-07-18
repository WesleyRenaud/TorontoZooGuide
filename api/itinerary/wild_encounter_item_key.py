from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Self

from ..shared.calendar_dates import DateValues
from ..types import ScheduleTimeKey

WILD_ENCOUNTER_ITEM_KEY_SEPARATOR = '||'


@dataclass( frozen=True )
class WildEncounterScheduleItemKey:
   name: str
   start_time: ScheduleTimeKey
   end_time: ScheduleTimeKey = None

   @classmethod
   def from_wire( cls, wire: str ) -> Self | None:
      parts = wire.split( WILD_ENCOUNTER_ITEM_KEY_SEPARATOR, 2 )
      name = parts[ 0 ].strip()

      if not name or len( parts ) < 2:
         return None

      start_time = DateValues.normalize_schedule_time( parts[ 1 ] )

      if not start_time:
         return None

      end_time = None

      if len( parts ) > 2:
         end_time = DateValues.normalize_schedule_time( parts[ 2 ] )

         if not end_time:
            return None

      return cls( name=name, start_time=start_time, end_time=end_time )


   def __post_init__( self ) -> None:
      normalized_start_time = DateValues.normalize_schedule_time(
         self.start_time )

      if not normalized_start_time:
         raise ValueError( 'Invalid wild encounter start time: ' + repr( self.start_time ) )

      object.__setattr__( self, 'start_time', normalized_start_time )

      if self.end_time is None:
         return

      normalized_end_time = DateValues.normalize_schedule_time(
         self.end_time )

      if normalized_end_time is None:
         raise ValueError( 'Invalid wild encounter end time: ' + repr( self.end_time ) )

      object.__setattr__( self, 'end_time', normalized_end_time )


   @classmethod
   def from_wires(
         cls,
         wires: list[ str ] | None,
      ) -> list[ Self ]:
      keys: list[ Self ] = []

      for wire in wires or []:
         key = cls.from_wire( str( wire ) )

         if key is not None:
            keys.append( key )

      return keys


   @classmethod
   def from_row( cls, row: Any ) -> Self | None:
      if hasattr( row, 'wild_encounter' ):
         name = row.wild_encounter
         start_time = row.start_time
         end_time = row.end_time
      else:
         source = row if isinstance( row, dict ) else {}
         name = source.get( 'wild_encounter' ) or source.get( 'name' ) or ''
         start_time = source.get( 'start_time' )
         end_time = source.get( 'end_time' )

      normalized_start_time = DateValues.normalize_schedule_time(
         start_time )

      if not str( name ).strip() or not normalized_start_time:
         return None

      end_time_was_provided = bool(
         DateValues.normalize_schedule_time_key( end_time ) )
      normalized_end_time = DateValues.normalize_schedule_time(
         end_time )

      if end_time_was_provided and normalized_end_time is None:
         return None

      return cls(
         name=str( name ).strip(),
         start_time=normalized_start_time,
         end_time=normalized_end_time )


   def __eq__( self, other: Any ) -> bool:
      if not isinstance( other, WildEncounterScheduleItemKey ):
         return NotImplemented

      return (
         self.name == other.name
         and self.start_time == other.start_time )


   def __hash__( self ) -> int:
      return hash( ( self.name, self.start_time ) )


   def to_wire( self ) -> str:
      parts = [ self.name.strip(), str( self.start_time ).strip() ]

      if self.end_time:
         parts.append( str( self.end_time ).strip() )

      return WILD_ENCOUNTER_ITEM_KEY_SEPARATOR.join( parts )

from __future__ import annotations

from .schedule_slot import ScheduleSlot


class EncounterScheduleSlots():
   by_name: dict[ str, set[ ScheduleSlot ] ]


   def __init__( self ) -> None:
      self.by_name = {}


   def add( self, name: str, slot: ScheduleSlot ) -> None:
      self.by_name.setdefault( name, set() ).add( slot )


   def add_slots( self, name: str, slots: set[ ScheduleSlot ] ) -> None:
      self.by_name.setdefault( name, set() ).update( slots )


   def names( self ) -> set[ str ]:
      return set( self.by_name )


   def for_name( self, name: str ) -> set[ ScheduleSlot ]:
      return self.by_name[ name ]

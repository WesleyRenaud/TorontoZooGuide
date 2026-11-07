from __future__ import annotations

from dataclasses import dataclass
from datetime import time

from api.app_string_provider import AppStringProvider
from api.shared.calendar_dates import CalendarDates
from api.shared.date_values import DateValues
from .schedule_slot import ScheduleSlot


@dataclass( frozen=True )
class ScheduleSlotGroup:
   time: time
   slots: frozenset[ ScheduleSlot ]


   def weekdays( self ) -> set[ int ]:
      return {
         slot.weekday
         for slot in self.slots
      }


   def description( self ) -> str:
      return (
         f'{ DateValues.format_display_time_value( self.time ) } '
         f'{ CalendarDates.format_weekdays( self.weekdays() ) }'
      )


   @classmethod
   def from_slots( cls, slots: set[ ScheduleSlot ] ) -> list[ ScheduleSlotGroup ]:
      by_time: dict[ time, set[ ScheduleSlot ] ] = {}

      for slot in slots:
         by_time.setdefault( slot.time, set() ).add( slot )

      return [
         cls( time=slot_time, slots=frozenset( grouped ) )
         for slot_time, grouped in sorted( by_time.items() )
      ]


   @classmethod
   def describe( cls, slots: set[ ScheduleSlot ] ) -> str:
      return AppStringProvider.values()[ 'format.semicolonJoin' ].join(
         group.description()
         for group in cls.from_slots( slots )
      )

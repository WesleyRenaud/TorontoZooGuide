from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Generic
from typing import TypeVar

from ..request_connection import get_connection
from ..types import Connection
from ..types import DateInput


TOpeningSchedule = TypeVar( 'TOpeningSchedule' )
TScheduleOverride = TypeVar( 'TScheduleOverride' )


@dataclass( frozen=True )
class AmenityCoordinatorMutations( Generic[ TOpeningSchedule, TScheduleOverride ] ):
   build_closed_schedule: Callable[ [ str, DateInput, DateInput, str ], TOpeningSchedule ]
   build_opening_schedule: Callable[
      [
         str,
         DateInput,
         DateInput,
         bool,
         bool,
         bool,
         bool,
         bool,
         bool,
         bool,
         bool,
         str,
      ],
      TOpeningSchedule,
   ]
   build_closure_override: Callable[ [ str, DateInput, DateInput, str ], TScheduleOverride ]
   save_opening_schedule: Callable[ [ Connection, TOpeningSchedule ], bool ]
   save_schedule_override: Callable[ [ Connection, TScheduleOverride ], bool ]
   save_replacing_overlaps: Callable[ [ Connection, TOpeningSchedule ], bool ]
   save_trimming_overlaps: Callable[ [ Connection, TOpeningSchedule ], bool ]


   def set_as_closed(
         self,
         name: str,
         start_date: DateInput,
         end_date: DateInput,
         message: str ) -> bool:
      schedule = self.build_closed_schedule(
         name,
         start_date,
         end_date,
         message )

      return self.save_opening_schedule( get_connection(), schedule )


   def set_closure_override(
         self,
         name: str,
         start_date: DateInput,
         end_date: DateInput,
         message: str ) -> bool:
      override = self.build_closure_override(
         name,
         start_date,
         end_date,
         message )

      return self.save_schedule_override( get_connection(), override )


   def set_opening_schedule(
         self,
         name: str,
         start_date: DateInput,
         end_date: DateInput,
         monday: bool,
         tuesday: bool,
         wednesday: bool,
         thursday: bool,
         friday: bool,
         saturday: bool,
         sunday: bool,
         holidays_only: bool,
         message: str ) -> bool:
      schedule = self._build_opening_schedule(
         name,
         start_date,
         end_date,
         monday,
         tuesday,
         wednesday,
         thursday,
         friday,
         saturday,
         sunday,
         holidays_only,
         message )

      return self.save_opening_schedule( get_connection(), schedule )


   def replace_opening_schedule_overlaps(
         self,
         name: str,
         start_date: DateInput,
         end_date: DateInput,
         monday: bool,
         tuesday: bool,
         wednesday: bool,
         thursday: bool,
         friday: bool,
         saturday: bool,
         sunday: bool,
         holidays_only: bool,
         message: str ) -> bool:
      schedule = self._build_opening_schedule(
         name,
         start_date,
         end_date,
         monday,
         tuesday,
         wednesday,
         thursday,
         friday,
         saturday,
         sunday,
         holidays_only,
         message )

      return self.save_replacing_overlaps( get_connection(), schedule )


   def trim_opening_schedule_overlaps(
         self,
         name: str,
         start_date: DateInput,
         end_date: DateInput,
         monday: bool,
         tuesday: bool,
         wednesday: bool,
         thursday: bool,
         friday: bool,
         saturday: bool,
         sunday: bool,
         holidays_only: bool,
         message: str ) -> bool:
      schedule = self._build_opening_schedule(
         name,
         start_date,
         end_date,
         monday,
         tuesday,
         wednesday,
         thursday,
         friday,
         saturday,
         sunday,
         holidays_only,
         message )

      return self.save_trimming_overlaps( get_connection(), schedule )


   def _build_opening_schedule(
         self,
         name: str,
         start_date: DateInput,
         end_date: DateInput,
         monday: bool,
         tuesday: bool,
         wednesday: bool,
         thursday: bool,
         friday: bool,
         saturday: bool,
         sunday: bool,
         holidays_only: bool,
         message: str ) -> TOpeningSchedule:
      return self.build_opening_schedule(
         name,
         start_date,
         end_date,
         monday,
         tuesday,
         wednesday,
         thursday,
         friday,
         saturday,
         sunday,
         holidays_only,
         message )

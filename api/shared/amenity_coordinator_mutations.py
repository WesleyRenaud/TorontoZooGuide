from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Generic
from typing import TypeVar

from ..request_connection_provider import RequestConnectionProvider
from ..types import Types


TOpeningSchedule = TypeVar( 'TOpeningSchedule' )
TScheduleOverride = TypeVar( 'TScheduleOverride' )


@dataclass( frozen=True )
class AmenityCoordinatorMutations( Generic[ TOpeningSchedule, TScheduleOverride ] ):
   build_closed_schedule: Callable[ [ str, Types.DateInput, Types.DateInput, str ], TOpeningSchedule ]
   build_opening_schedule: Callable[
      [
         str,
         Types.DateInput,
         Types.DateInput,
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
   build_closure_override: Callable[ [ str, Types.DateInput, Types.DateInput, str ], TScheduleOverride ]
   save_opening_schedule: Callable[ [ Types.Connection, TOpeningSchedule ], bool ]
   save_schedule_override: Callable[ [ Types.Connection, TScheduleOverride ], bool ]
   save_replacing_overlaps: Callable[ [ Types.Connection, TOpeningSchedule ], bool ]
   save_trimming_overlaps: Callable[ [ Types.Connection, TOpeningSchedule ], bool ]


   def set_as_closed(
         self,
         name: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         message: str ) -> bool:
      schedule = self.build_closed_schedule(
         name,
         start_date,
         end_date,
         message )

      return self.save_opening_schedule( RequestConnectionProvider.get(), schedule )


   def set_closure_override(
         self,
         name: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         message: str ) -> bool:
      override = self.build_closure_override(
         name,
         start_date,
         end_date,
         message )

      return self.save_schedule_override( RequestConnectionProvider.get(), override )


   def set_opening_schedule(
         self,
         name: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
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

      return self.save_opening_schedule( RequestConnectionProvider.get(), schedule )


   def replace_opening_schedule_overlaps(
         self,
         name: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
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

      return self.save_replacing_overlaps( RequestConnectionProvider.get(), schedule )


   def trim_opening_schedule_overlaps(
         self,
         name: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
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

      return self.save_trimming_overlaps( RequestConnectionProvider.get(), schedule )


   def _build_opening_schedule(
         self,
         name: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
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

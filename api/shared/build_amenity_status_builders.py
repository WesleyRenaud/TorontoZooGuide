from __future__ import annotations

from dataclasses import dataclass
from typing import Generic
from typing import TypeVar

from .build_closed_opening_schedule_fields import build_closed_opening_schedule_fields
from .build_closure_override_fields import build_closure_override_fields
from .build_opening_schedule_weekday_fields import build_opening_schedule_weekday_fields
from .opening_schedule_weekday_fields import OpeningScheduleWeekdayFields
from ..types import DateInput


TOpeningSchedule = TypeVar( 'TOpeningSchedule' )
TScheduleOverride = TypeVar( 'TScheduleOverride' )


@dataclass( frozen=True )
class AmenityStatusBuilders( Generic[ TOpeningSchedule, TScheduleOverride ] ):
   name_field: str
   opening_schedule_class: type[ TOpeningSchedule ]
   schedule_override_class: type[ TScheduleOverride ]

   def build_closed_schedule(
         self,
         name: str,
         start_date: DateInput,
         end_date: DateInput,
         message: str ) -> TOpeningSchedule:
      fields = build_closed_opening_schedule_fields(
         name=name,
         start_date=start_date,
         end_date=end_date,
         message=message )

      return self._opening_schedule( name, fields )


   def build_opening_schedule(
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
      fields = build_opening_schedule_weekday_fields(
         name=name,
         start_date=start_date,
         end_date=end_date,
         monday=monday,
         tuesday=tuesday,
         wednesday=wednesday,
         thursday=thursday,
         friday=friday,
         saturday=saturday,
         sunday=sunday,
         holidays_only=holidays_only,
         message=message )

      return self._opening_schedule( name, fields )


   def build_closure_override(
         self,
         name: str,
         start_date: DateInput,
         end_date: DateInput,
         message: str ) -> TScheduleOverride:
      fields = build_closure_override_fields(
         name=name,
         start_date=start_date,
         end_date=end_date,
         message=message )

      return self.schedule_override_class(
         **{
            self.name_field: name,
            'start_date': fields.start_date,
            'end_date': fields.end_date,
            'is_closed': fields.is_closed,
            'message': fields.message,
         } )


   def _opening_schedule(
         self,
         name: str,
         fields: OpeningScheduleWeekdayFields ) -> TOpeningSchedule:
      return self.opening_schedule_class(
         **{
            self.name_field: name,
            'start_date': fields.start_date,
            'end_date': fields.end_date,
            'monday': fields.monday,
            'tuesday': fields.tuesday,
            'wednesday': fields.wednesday,
            'thursday': fields.thursday,
            'friday': fields.friday,
            'saturday': fields.saturday,
            'sunday': fields.sunday,
            'holidays_only': fields.holidays_only,
            'message': fields.message,
         } )

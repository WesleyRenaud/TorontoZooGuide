from __future__ import annotations

from datetime import date

from ... import zoo
from ...types import MonthInput, VisitDay, VisitYear
from ..data_access.restroom_record import RestroomRecord
from .restroom_context import RestroomContext


def resolve_restroom_context(
      day: VisitDay,
      month: MonthInput,
      year: VisitYear ) -> RestroomContext:
   return RestroomContext(
      target_date=zoo.ZooUtil.visit_target_date(
         month=month,
         day=day,
         year=year ) )


def is_restroom_status_active(
      restroom_record: RestroomRecord,
      target_date: date ) -> bool:
   if restroom_record.is_closed == None:
      return False

   return zoo.ZooUtil.is_date_in_range(
      target_date=target_date,
      start_date_value=restroom_record.closed_start,
      end_date_value=restroom_record.closed_end )


def is_restroom_alert_active(
      restroom_record: RestroomRecord,
      target_date: date ) -> bool:
   if restroom_record.alert_message == None:
      return False

   return zoo.ZooUtil.is_date_in_range(
      target_date=target_date,
      start_date_value=restroom_record.alert_start_date,
      end_date_value=restroom_record.alert_end_date )


def build_restroom(
      restroom_record: RestroomRecord,
      context: RestroomContext ) -> zoo.Restroom:
   is_closed = (
      bool( restroom_record.is_closed )
      and is_restroom_status_active(
         restroom_record=restroom_record,
         target_date=context.target_date ) )
   has_alert = is_restroom_alert_active(
      restroom_record=restroom_record,
      target_date=context.target_date )

   return zoo.Restroom(
      title=restroom_record.title,
      x_coord=restroom_record.x_coord,
      y_coord=restroom_record.y_coord,
      is_closed=is_closed,
      closed_message=restroom_record.closed_message if is_closed else None,
      has_alert=has_alert,
      alert_message=restroom_record.alert_message if has_alert else None )


def build_restrooms(
      restroom_records: list[ RestroomRecord ],
      context: RestroomContext,
      include_closed_restrooms: bool ) -> list[ zoo.Restroom ]:

   restrooms = []

   for restroom_record in restroom_records:
      restroom = build_restroom(
         restroom_record=restroom_record,
         context=context )

      if restroom.is_closed and not include_closed_restrooms:
         continue

      restrooms.append( restroom )

   return restrooms

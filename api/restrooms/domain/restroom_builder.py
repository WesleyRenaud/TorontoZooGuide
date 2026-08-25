from __future__ import annotations

from datetime import date

from ..data_access.restroom_record import RestroomRecord
from ...models import Restroom
from .restroom_context import RestroomContext
from ...shared.calendar_dates import DateValues


class RestroomBuilder():
   @classmethod
   def is_status_active(
         cls,
         restroom_record: RestroomRecord,
         target_date: date ) -> bool:
      if restroom_record.is_closed == None:
         return False

      return DateValues.is_date_in_range(
         target_date=target_date,
         start_date_value=restroom_record.closed_start,
         end_date_value=restroom_record.closed_end )


   @classmethod
   def is_alert_active(
         cls,
         restroom_record: RestroomRecord,
         target_date: date ) -> bool:
      if restroom_record.alert_message == None:
         return False

      return DateValues.is_date_in_range(
         target_date=target_date,
         start_date_value=restroom_record.alert_start_date,
         end_date_value=restroom_record.alert_end_date )


   @classmethod
   def build_restroom(
         cls,
         restroom_record: RestroomRecord,
         context: RestroomContext ) -> Restroom:
      is_closed = (
         bool( restroom_record.is_closed )
         and cls.is_status_active(
            restroom_record=restroom_record,
            target_date=context.target_date ) )
      has_alert = cls.is_alert_active(
         restroom_record=restroom_record,
         target_date=context.target_date )

      return Restroom(
         title=restroom_record.title,
         x_coord=restroom_record.x_coord,
         y_coord=restroom_record.y_coord,
         is_closed=is_closed,
         closed_message=restroom_record.closed_message if is_closed else None,
         has_alert=has_alert,
         alert_message=restroom_record.alert_message if has_alert else None )


   @classmethod
   def build_restrooms(
         cls,
         restroom_records: list[ RestroomRecord ],
         context: RestroomContext,
         include_closed_restrooms: bool ) -> list[ Restroom ]:
      restrooms = []

      for restroom_record in restroom_records:
         restroom = cls.build_restroom(
            restroom_record=restroom_record,
            context=context )

         if restroom.is_closed and not include_closed_restrooms:
            continue

         restrooms.append( restroom )

      return restrooms

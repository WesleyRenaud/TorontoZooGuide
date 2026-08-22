from __future__ import annotations

from ..data_access.transportation_record import TransportationRecord
from ...models.transportation import Transportation
from ...shared.opening_schedule_visit_context import OpeningScheduleVisitContext


def build_transportation(
      record: TransportationRecord,
      context: OpeningScheduleVisitContext ) -> Transportation:
   if context.is_weekend_or_holiday:
      open_time = record.weekend_holiday_start_time
      close_time = record.weekend_holiday_end_time
   else:
      open_time = record.weekday_start_time
      close_time = record.weekday_end_time

   return Transportation(
      name=record.name,
      is_also_attraction=record.is_also_attraction,
      free_with_admission=record.free_with_admission,
      description=record.description,
      info_link=record.info_link,
      hyperlink_text=record.hyperlink_text,
      x_coord=record.x_coord,
      y_coord=record.y_coord,
      region=record.region,
      open_time=open_time,
      close_time=close_time )


def build_transportations(
      records: list[ TransportationRecord ],
      context: OpeningScheduleVisitContext ) -> list[ Transportation ]:
   return [
      build_transportation( record, context )
      for record in records
   ]

from __future__ import annotations

from ..data_access.zoo_hours_record import ZooHoursRecord
from ...models import ZooHours


class ZooHoursBuilder():
   @classmethod
   def build( cls, zoo_hours_record: ZooHoursRecord ) -> ZooHours:
      return ZooHours(
         date=zoo_hours_record.operating_date,
         early_admission_time=zoo_hours_record.early_admission_time,
         open_time=zoo_hours_record.open_time,
         last_admission_time=zoo_hours_record.last_admission_time,
         close_time=zoo_hours_record.close_time )

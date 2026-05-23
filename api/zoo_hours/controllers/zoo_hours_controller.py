from __future__ import annotations

from ... import zoo
from ...types import MonthInput, VisitDay, VisitYear
from ..data_access.zoo_hours import fetch_zoo_hours_record
from ..logic.zoo_hours import build_zoo_hours
from ...request_connection import get_connection


class ZooHoursController():


   @classmethod
   def get_zoo_hours(
         cls,
         day: VisitDay,
         month: MonthInput,
         year: VisitYear ) -> zoo.ZooHours | None:
      operating_date = zoo.ZooUtil.visit_target_date(
         month,
         day,
         year )

      zoo_hours_record = fetch_zoo_hours_record(
         get_connection(),
         operating_date )

      if zoo_hours_record == None:
         return None

      return build_zoo_hours( zoo_hours_record )

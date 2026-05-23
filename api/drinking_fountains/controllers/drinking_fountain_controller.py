from __future__ import annotations

from ...models import DrinkingFountain
from ...zoo_util import ZooUtil
from ...types import DateInput, MonthInput, VisitDay, VisitYear
from ..data_access.drinking_fountain import fetch_drinking_fountain_records
from ..data_access.drinking_fountain_status import save_drinking_fountain_closed_status
from ..data_access.drinking_fountain_status import save_drinking_fountain_open_status
from ..data_access.drinking_fountain_status import fetch_drinking_fountain_seasonal_likelihood
from ..data_access.drinking_fountain_status import fetch_drinking_fountain_status_record
from ..logic.drinking_fountain import build_drinking_fountains
from ..logic.drinking_fountain_status import build_drinking_fountain_closed_status
from ..logic.drinking_fountain_status import build_drinking_fountain_open_status
from ..logic.drinking_fountain_status import build_drinking_fountain_seasonal_status
from ..logic.drinking_fountain_status import build_drinking_fountain_status
from ..logic.drinking_fountain_status import drinking_fountain_status_applies_to_date
from ...request_connection import get_connection


class DrinkingFountainController():


   @classmethod
   def get_drinking_fountains(
         cls,
         month: MonthInput,
         day: VisitDay,
         year: VisitYear ) -> list[ DrinkingFountain ]:
      target_date = ZooUtil.visit_target_date(
         month=month,
         day=day,
         year=year )

      status_record = fetch_drinking_fountain_status_record( get_connection() )

      if status_record and drinking_fountain_status_applies_to_date( status_record, target_date ):
         is_closed, closed_message, likelihood = build_drinking_fountain_status(
            status_record )
      else:
         seasonal_likelihood = fetch_drinking_fountain_seasonal_likelihood(
            get_connection(),
            target_date )
         is_closed, closed_message, likelihood = build_drinking_fountain_seasonal_status(
            seasonal_likelihood )

      fountain_records = fetch_drinking_fountain_records( get_connection() )

      return build_drinking_fountains(
         fountain_records,
         is_closed,
         closed_message,
         likelihood )


   @classmethod
   def set_drinking_fountains_as_closed(
         cls,
         start_date: DateInput | None = None,
         end_date: DateInput | None = None,
         message: str | None = None ) -> bool:
      status = build_drinking_fountain_closed_status(
         start_date=start_date,
         end_date=end_date,
         message=message )

      return save_drinking_fountain_closed_status(
         get_connection(),
         status=status )


   @classmethod
   def set_drinking_fountains_as_open(
         cls,
         start_date: DateInput | None = None,
         end_date: DateInput | None = None ) -> bool:
      status = build_drinking_fountain_open_status(
         start_date=start_date,
         end_date=end_date )

      return save_drinking_fountain_open_status(
         get_connection(),
         status=status )

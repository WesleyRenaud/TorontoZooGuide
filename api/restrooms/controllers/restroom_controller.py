from __future__ import annotations

from ..data_access.restroom import fetch_restroom_names
from ..data_access.restroom import fetch_restroom_records
from ..data_access.restroom_alert import delete_restroom_alert
from ..data_access.restroom_alert import save_restroom_alert
from ..data_access.restroom_status import save_restroom_closed_status
from ..data_access.restroom_status import save_restroom_open_status
from ..logic.restroom import build_restrooms
from ..logic.restroom import resolve_restroom_context
from ..logic.restroom_alert_builder import build_restroom_alert
from ..logic.restroom_status import build_restroom_closed_status
from ..logic.restrooms_matching_query import build_restrooms_matching_query
from ...models import Restroom
from ...request_connection import get_connection
from ...shared.date_values import DateValues
from ...types import DateInput, MonthInput, VisitDay, VisitYear


class RestroomController():


   @classmethod
   def get_restroom_names( cls ) -> list[ str ]:
      return fetch_restroom_names( get_connection() )


   @classmethod
   def get_restrooms(
         cls,
         day: VisitDay,
         month: MonthInput,
         year: VisitYear,
         include_closed_restrooms: bool = False ) -> list[ Restroom ]:

      return build_restrooms(
         restroom_records=fetch_restroom_records( get_connection() ),
         context=resolve_restroom_context(
            day=day,
            month=month,
            year=year ),
         include_closed_restrooms=include_closed_restrooms )


   @classmethod
   def get_restrooms_matching_query(
         cls,
         query: str,
         day: VisitDay,
         month: MonthInput,
         year: VisitYear,
         include_closed_restrooms: bool ) -> list[ Restroom ]:

      restrooms = cls.get_restrooms(
         day=day,
         month=month,
         year=year,
         include_closed_restrooms=include_closed_restrooms )

      return build_restrooms_matching_query(
         restrooms,
         query )


   @classmethod
   def set_restroom_as_closed(
         cls,
         restroom: str,
         start_date: DateInput,
         end_date: DateInput,
         message: str ) -> bool:
      status = build_restroom_closed_status(
         restroom=restroom,
         start_date=start_date,
         end_date=end_date,
         message=message )

      return save_restroom_closed_status(
         get_connection(),
         restroom=status.restroom,
         start_date=status.start_date,
         end_date=status.end_date,
         message=status.message )


   @classmethod
   def set_restroom_as_open(
         cls,
         restroom: str,
         start_date: DateInput,
         end_date: DateInput ) -> bool:
      date_range = DateValues.resolve_open_ended_date_range(
         start_date=start_date,
         end_date=end_date )

      return save_restroom_open_status(
         get_connection(),
         restroom=restroom,
         start_date=date_range.start_date,
         end_date=date_range.end_date )


   @classmethod
   def set_restroom_alert(
         cls,
         restroom: str,
         alert_start_date: DateInput,
         alert_end_date: DateInput,
         message: str ) -> bool:
      alert = build_restroom_alert(
         restroom=restroom,
         alert_start_date=alert_start_date,
         alert_end_date=alert_end_date,
         message=message )

      return save_restroom_alert(
         get_connection(),
         restroom=alert.restroom,
         alert_start_date=alert.start_date,
         alert_end_date=alert.end_date,
         message=alert.message )


   @classmethod
   def remove_restroom_alert( cls, restroom: str ) -> bool:
      return delete_restroom_alert(
         get_connection(),
         restroom=restroom )

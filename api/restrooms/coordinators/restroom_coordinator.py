from __future__ import annotations

from ..data_access.restroom_alert_provider import RestroomAlertProvider
from ..data_access.restroom_provider import RestroomProvider
from ..data_access.restroom_status_provider import RestroomStatusProvider
from ..domain.restroom_builder import RestroomBuilder
from ..domain.restroom_context_builder import RestroomContextBuilder
from ...models import Restroom
from ...request_connection_provider import RequestConnectionProvider
from ..search.restrooms_matching_query_builder import RestroomsMatchingQueryBuilder
from ...shared.calendar_dates import DateValues
from ..status.restroom_alert_builder import RestroomAlertBuilder
from ..status.restroom_status_builder import RestroomStatusBuilder
from ...types import Types


class RestroomCoordinator():
   @classmethod
   def get_restroom_names( cls ) -> list[ str ]:
      return RestroomProvider.fetch_restroom_names( RequestConnectionProvider.get() )


   @classmethod
   def get_restrooms(
         cls,
         day: Types.VisitDay,
         month: Types.MonthInput,
         year: Types.VisitYear,
         include_closed_restrooms: bool = False ) -> list[ Restroom ]:

      return RestroomBuilder.build_restrooms(
         restroom_records=RestroomProvider.fetch_restroom_records( RequestConnectionProvider.get() ),
         context=RestroomContextBuilder.resolve(
            day=day,
            month=month,
            year=year ),
         include_closed_restrooms=include_closed_restrooms )


   @classmethod
   def get_restrooms_matching_query(
         cls,
         query: str,
         day: Types.VisitDay,
         month: Types.MonthInput,
         year: Types.VisitYear,
         include_closed_restrooms: bool ) -> list[ Restroom ]:

      restrooms = cls.get_restrooms(
         day=day,
         month=month,
         year=year,
         include_closed_restrooms=include_closed_restrooms )

      return RestroomsMatchingQueryBuilder.build(
         restrooms,
         query )


   @classmethod
   def set_restroom_as_closed(
         cls,
         restroom: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         message: str ) -> bool:
      status = RestroomStatusBuilder.build_closed_status(
         restroom=restroom,
         start_date=start_date,
         end_date=end_date,
         message=message )

      return RestroomStatusProvider.save_closed_status(
         RequestConnectionProvider.get(),
         restroom=status.restroom,
         start_date=status.start_date,
         end_date=status.end_date,
         message=status.message )


   @classmethod
   def set_restroom_as_open(
         cls,
         restroom: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput ) -> bool:
      date_range = DateValues.resolve_open_ended_date_range(
         start_date=start_date,
         end_date=end_date )

      return RestroomStatusProvider.save_open_status(
         RequestConnectionProvider.get(),
         restroom=restroom,
         start_date=date_range.start_date,
         end_date=date_range.end_date )


   @classmethod
   def set_restroom_alert(
         cls,
         restroom: str,
         alert_start_date: Types.DateInput,
         alert_end_date: Types.DateInput,
         message: str ) -> bool:
      alert = RestroomAlertBuilder.build_alert(
         restroom=restroom,
         alert_start_date=alert_start_date,
         alert_end_date=alert_end_date,
         message=message )

      return RestroomAlertProvider.save_alert(
         RequestConnectionProvider.get(),
         restroom=alert.restroom,
         alert_start_date=alert.start_date,
         alert_end_date=alert.end_date,
         message=alert.message )


   @classmethod
   def remove_restroom_alert( cls, restroom: str ) -> bool:
      return RestroomAlertProvider.delete_alert(
         RequestConnectionProvider.get(),
         restroom=restroom )

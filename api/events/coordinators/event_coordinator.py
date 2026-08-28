from __future__ import annotations

from ..data_access.event_provider import EventProvider
from ...models import Event
from ...request_connection_provider import RequestConnectionProvider
from ...shared.calendar_dates import CalendarDates
from ...types import Types


class EventCoordinator():
   @classmethod
   def get_events_for_visit_date(
         cls,
         month: Types.MonthInput,
         day: Types.VisitDay,
         year: Types.VisitYear ) -> list[ Event ]:
      target_date = CalendarDates.visit_target_date(
         month=month,
         day=day,
         year=year )

      return EventProvider.fetch_events( RequestConnectionProvider.get(), target_date )


   @classmethod
   def create_event(
         cls,
         name: str,
         location: str,
         description: str,
         link: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput ) -> bool:
      return EventProvider.insert_event(
         RequestConnectionProvider.get(),
         event=Event(
            name=name,
            location=location,
            description=description,
            link=link,
            start_date=start_date,
            end_date=end_date ) )

from __future__ import annotations

from ..data_access.event_provider import EventProvider
from ...models import Event
from ...request_connection import get_connection
from ...shared.calendar_dates import CalendarDates
from ...types import DateInput, MonthInput, VisitDay, VisitYear


class EventCoordinator():
   @classmethod
   def get_events_for_visit_date(
         cls,
         month: MonthInput,
         day: VisitDay,
         year: VisitYear ) -> list[ Event ]:
      target_date = CalendarDates.visit_target_date(
         month=month,
         day=day,
         year=year )

      return EventProvider.fetch_events( get_connection(), target_date )


   @classmethod
   def create_event(
         cls,
         name: str,
         location: str,
         description: str,
         link: str,
         start_date: DateInput,
         end_date: DateInput ) -> bool:
      return EventProvider.insert_event(
         get_connection(),
         event=Event(
            name=name,
            location=location,
            description=description,
            link=link,
            start_date=start_date,
            end_date=end_date ) )

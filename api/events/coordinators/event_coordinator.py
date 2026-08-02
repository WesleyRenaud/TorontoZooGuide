from __future__ import annotations

from ..data_access.event import insert_event
from ...models import Event
from ...request_connection import get_connection
from ...types import DateInput


class EventCoordinator():
   @classmethod
   def create_event(
         cls,
         name: str,
         location: str,
         description: str,
         link: str,
         start_date: DateInput,
         end_date: DateInput ) -> bool:
      return insert_event(
         get_connection(),
         event=Event(
            name=name,
            location=location,
            description=description,
            link=link,
            start_date=start_date,
            end_date=end_date ) )

from __future__ import annotations

from pathlib import Path

from api.app_string_provider import AppStringProvider
from api.database_connection_provider import DatabaseConnectionProvider
from api.events.coordinators.event_coordinator import EventCoordinator
from api.models import Event
from api.request_connection_provider import RequestConnectionProvider
from tools.checks.check_report import CheckReport
from tools.checks.website_zoo_event import WebsiteZooEvent


class ZooEventFixer():
   @classmethod
   def add( cls, events: list[ WebsiteZooEvent ] ) -> list[ WebsiteZooEvent ]:
      saved = []

      for event in events:
         wrote = EventCoordinator.create_event(
            name=event.name,
            location='',
            description=WebsiteZooEvent.limited( event.description ),
            link=event.link,
            start_date=event.start.isoformat(),
            end_date=event.end.isoformat(),
         )

         if not wrote:
            raise RuntimeError( AppStringProvider.format( 'checks.couldNotReadZooEventDates' ) )

         saved.append( event )

      return saved


   @classmethod
   def remove( cls, events: list[ Event ] ) -> list[ Event ]:
      removed = []

      for event in events:
         if EventCoordinator.remove_event( event.name, event.start_date ):
            removed.append( event )

      return removed


   @classmethod
   def apply(
         cls,
         database: Path,
         missing: list[ WebsiteZooEvent ],
         extra: list[ Event ] ) -> tuple[ list[ WebsiteZooEvent ], list[ Event ] ]:
      if len( missing ) == 0 and len( extra ) == 0:
         return [], []

      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         saved = cls.add( missing )
         removed = cls.remove( extra )
      finally:
         RequestConnectionProvider.clear()
         connection.close()

      changed = len( saved ) + len( removed )

      if changed > 0:
         CheckReport.note_fixed( changed )

      return saved, removed

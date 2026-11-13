from __future__ import annotations

from pathlib import Path

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.database_connection_provider import DatabaseConnectionProvider
from api.request_connection_provider import RequestConnectionProvider
from tools.checks.check_report import CheckReport
from tools.checks.viewing_hours_plan import ViewingHoursPlan


class ViewingHoursFixer():
   @classmethod
   def save( cls, plan: ViewingHoursPlan ) -> None:
      for hours in plan.added + plan.extended + plan.trimmed + plan.realigned:
         AnimalCoordinator.set_animal_limited_viewing_schedule(
            species=hours.species,
            exhibit=hours.exhibit,
            start_date=hours.start,
            end_date=hours.end,
            daily_start_time=hours.opens,
            daily_end_time=hours.closes,
            message=hours.guest_message(),
         )


   @classmethod
   def remove( cls, plan: ViewingHoursPlan ) -> None:
      for hours in plan.removed:
         AnimalCoordinator.remove_animal_visibility_schedule(
            hours.species,
            hours.exhibit,
         )


   @classmethod
   def apply( cls, database: Path, plan: ViewingHoursPlan ) -> None:
      if plan.count() == 0:
         return

      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         cls.save( plan )
         cls.remove( plan )
      finally:
         RequestConnectionProvider.clear()
         connection.close()

      CheckReport.note_fixed( plan.count() )

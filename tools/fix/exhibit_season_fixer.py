from __future__ import annotations

from datetime import date
from pathlib import Path

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.database_connection_provider import DatabaseConnectionProvider
from api.exhibits.coordinators.exhibit_coordinator import ExhibitCoordinator
from api.request_connection_provider import RequestConnectionProvider
from tools.checks.check_report import CheckReport
from tools.checks.exhibit_window import ExhibitWindow


class ExhibitSeasonFixer():
   @classmethod
   def line( cls, exhibit: str, window: ExhibitWindow ) -> str:
      return CheckReport.join_lines( [ exhibit, window.detail() ] )


   @classmethod
   def apply( cls, database: Path, exhibit: str, window: ExhibitWindow ) -> str:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         if window.closed:
            ExhibitCoordinator.set_exhibit_as_closed(
               exhibit,
               window.start,
               window.end,
               '',
               True )
            cls.set_animals_off_display( exhibit, window.start, window.end )
         else:
            ExhibitCoordinator.set_exhibit_as_open( exhibit, window.start, window.end )
      finally:
         RequestConnectionProvider.clear()
         connection.close()

      CheckReport.note_fixed( 1 )
      return cls.line( exhibit, window )


   @classmethod
   def align_animals( cls, database: Path, exhibit: str, start: date, end: date ) -> None:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         cls.set_animals_off_display( exhibit, start, end )
      finally:
         RequestConnectionProvider.clear()
         connection.close()


   @classmethod
   def set_animals_off_display( cls, exhibit: str, start: date, end: date ) -> None:
      for species in ExhibitCoordinator.get_names_of_animals_in_exhibit( exhibit ):
         scopes = AnimalCoordinator.get_animal_viewing_scopes( species, exhibit )

         if not scopes:
            continue

         AnimalCoordinator.set_animal_as_off_display(
            species,
            exhibit,
            start,
            end,
            '',
            scopes,
            True,
            None,
            None )

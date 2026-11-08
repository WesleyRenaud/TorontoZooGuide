from __future__ import annotations

from datetime import date
from pathlib import Path

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.animals.domain.closure_linked_off_display_animals import ClosureLinkedOffDisplayAnimals
from api.app_string_provider import AppStringProvider
from api.database_connection_provider import DatabaseConnectionProvider
from api.request_connection_provider import RequestConnectionProvider
from api.shared.date_values import DateValues
from api.updates.coordinators.update_coordinator import UpdateCoordinator
from tools.checks.animal_detail_image import AnimalDetailImage
from tools.checks.check_report import CheckReport


class ClosureOffDisplayExtensionFixer():
   @classmethod
   def line( cls, species: str, exhibit: str, end: date ) -> str:
      lines = [
         AppStringProvider.format(
            'format.middleDotPair',
            first=species,
            second=exhibit,
         )
      ]
      lines.append( CheckReport.detail_item(
         CheckReport.text( 'checks.photo' )
         + AnimalDetailImage.source( exhibit, species )
      ) )
      lines.append( CheckReport.detail_item(
         CheckReport.text( 'checks.extendedOffDisplayThrough' )
         + DateValues.format_display_date_value( end )
         + CheckReport.text( 'checks.period' )
      ) )
      return '\n'.join( lines )


   @classmethod
   def extend_closure( cls, group: ClosureLinkedOffDisplayAnimals, end: date ) -> None:
      start = group.start.isoformat()
      end_key = end.isoformat()
      UpdateCoordinator.end_update(
         title=group.title,
         start_date=start,
         end_date=end_key )
      AnimalCoordinator.extend_closure_linked_off_display(
         title=group.title,
         start_date=start,
         end_date=end_key )


   @classmethod
   def fix(
         cls,
         database: Path,
         groups: list[ ClosureLinkedOffDisplayAnimals ],
         end: date ) -> list[ str ]:
      if groups == []:
         return []

      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         lines = []

         for group in groups:
            cls.extend_closure( group, end )
            lines.extend(
               cls.line( enclosure.species, enclosure.exhibit, end )
               for enclosure in group.enclosures()
            )

         CheckReport.note_fixed( len( lines ) )
         return sorted( lines, key=str.casefold )
      finally:
         RequestConnectionProvider.clear()
         connection.close()

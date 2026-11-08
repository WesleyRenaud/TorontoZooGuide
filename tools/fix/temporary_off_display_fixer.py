from __future__ import annotations

from datetime import date
from pathlib import Path

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.animals.domain.animal_species_exhibit import AnimalSpeciesExhibit
from api.app_string_provider import AppStringProvider
from api.database_connection_provider import DatabaseConnectionProvider
from api.request_connection_provider import RequestConnectionProvider
from api.shared.calendar_dates import CalendarDates
from api.shared.date_values import DateValues
from tools.checks.animal_detail_image import AnimalDetailImage
from tools.checks.check_report import CheckReport


class TemporaryOffDisplayFixer():
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
         CheckReport.text( 'checks.setOffDisplayThrough' )
         + DateValues.format_display_date_value( end )
         + CheckReport.text( 'checks.period' )
      ) )
      return '\n'.join( lines )


   @classmethod
   def fix(
         cls,
         database: Path,
         enclosures: list[ AnimalSpeciesExhibit ],
         today: date ) -> list[ str ]:
      if enclosures == []:
         return []

      end = CalendarDates.one_week_later( today )
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         lines = []

         for enclosure in enclosures:
            AnimalCoordinator.set_animal_as_off_display(
               species=enclosure.species,
               exhibit=enclosure.exhibit,
               start_date=today,
               end_date=end,
               message='',
               viewing_scopes=AnimalCoordinator.get_animal_viewing_scopes(
                  enclosure.species,
                  enclosure.exhibit,
               ),
               is_off_display_for_season=False,
               closure_update_title=None,
               closure_update_start=None,
            )
            lines.append( cls.line( enclosure.species, enclosure.exhibit, end ) )

         CheckReport.note_fixed( len( lines ) )
         return lines
      finally:
         RequestConnectionProvider.clear()
         connection.close()

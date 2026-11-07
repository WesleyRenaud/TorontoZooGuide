from __future__ import annotations

from datetime import date
from pathlib import Path

from .animal_detail_image import AnimalDetailImage
from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.app_string_provider import AppStringProvider
from api.database_connection_provider import DatabaseConnectionProvider
from api.request_connection_provider import RequestConnectionProvider
from api.shared.calendar_dates import CalendarDates
from api.shared.date_values import DateValues
from .check_report import CheckReport
from .website_off_display_animal import WebsiteOffDisplayAnimal
from .website_page import WebsitePage


class SeasonalOffDisplayCorrection():
   @classmethod
   def line(
         cls,
         species: str,
         exhibit: str,
         photo: str,
         start: date,
         end: date ) -> str:
      lines = [
         AppStringProvider.format(
            'format.middleDotPair',
            first=species,
            second=exhibit,
         )
      ]

      if photo != '':
         lines.append(
            CheckReport.detail_item( CheckReport.text( 'checks.photo' ) + photo )
         )

      lines.append( CheckReport.detail_item(
         CheckReport.text( 'checks.setOffDisplayForSeasonFrom' )
         + DateValues.format_display_date_value( start )
         + CheckReport.text( 'checks.dateThrough' )
         + DateValues.format_display_date_value( end )
         + CheckReport.text( 'checks.period' )
      ) )
      return '\n'.join( lines )


   @classmethod
   def same_animal( cls, website_name: str, app_name: str ) -> bool:
      return WebsitePage.normalize_name( website_name ) == WebsitePage.normalize_name( app_name )


   @classmethod
   def correct(
         cls,
         database: Path,
         website_only: list[ WebsiteOffDisplayAnimal ],
         today: date ) -> list[ str ]:
      if website_only == []:
         return []

      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         enclosures = AnimalCoordinator.get_enclosure_off_display_months()
         lines: list[ str ] = []
         fixed_names: set[ str ] = set()

         for listing in website_only:
            matched = False

            for enclosure in enclosures:
               if (
                  cls.same_animal( listing.section, enclosure.exhibit )
                  and cls.same_animal( listing.name, enclosure.species )
               ):
                  end = CalendarDates.next_month_end( enclosure.until_month, today )
                  AnimalCoordinator.set_off_display_for_season_until(
                     species=enclosure.species,
                     exhibit=enclosure.exhibit,
                     today=today )
                  lines.append( cls.line(
                     enclosure.species,
                     enclosure.exhibit,
                     AnimalDetailImage.source( enclosure.exhibit, enclosure.species ),
                     today,
                     end,
                  ) )
                  fixed_names.add( listing.name )
                  matched = True

            if not matched:
               lines.append( listing.name )

         CheckReport.note_fixed( len( fixed_names ) )
         return sorted( lines, key=str.casefold )
      finally:
         RequestConnectionProvider.clear()
         connection.close()

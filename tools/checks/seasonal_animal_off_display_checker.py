from __future__ import annotations

import argparse
from datetime import date
from html import unescape
from pathlib import Path
import re
import sys
from urllib.parse import unquote

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.animals.domain.seasonal_off_display_animal import SeasonalOffDisplayAnimal
from api.app_string_provider import AppStringProvider
from api.database_connection_provider import DatabaseConnectionProvider
from api.exhibits.coordinators.exhibit_coordinator import ExhibitCoordinator
from api.exhibits.domain.seasonal_exhibit import SeasonalExhibit
from api.request_connection_provider import RequestConnectionProvider
from .check_args_parser import CheckArgsParser
from .check_exit_code import CheckExitCode
from .check_report import CheckReport
from .website_off_display_animal import WebsiteOffDisplayAnimal
from .website_page import WebsitePage


class SeasonalAnimalOffDisplayChecker():
   SECTION_RE = re.compile(
      r'(?is)<div class="atitle[^"]*" id="(?P<id>[^"]+)">(?P<body>.*?)(?=<div class="atitle|\Z)',
   )


   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse(
         AppStringProvider.format( 'reports.seasonalOffDisplay.description' )
      )


   @classmethod
   def parse_website_animals( cls, page_html: str ) -> list[ WebsiteOffDisplayAnimal ]:
      animals = []

      for section in cls.SECTION_RE.finditer( page_html ):
         animals.extend( cls.animals_in_section(
            unescape( unquote( section.group( 'id' ) ) ).strip(),
            section.group( 'body' ),
         ) )

      return animals


   @classmethod
   def animals_in_section( cls, section: str, body: str ) -> list[ WebsiteOffDisplayAnimal ]:
      animals = []

      for href, card in re.findall( r'(?is)<a href="/animals/([^"]+)"(.*?)</a>', body ):
         if 'status sseason' not in card.casefold():
            continue

         if AppStringProvider.format( 'checks.offForSeason' ) not in WebsitePage.clean_html( card ).casefold():
            continue

         animals.append( WebsiteOffDisplayAnimal(
            section=section,
            name=WebsitePage.clean_website_name( href ),
         ) )

      return animals


   @classmethod
   def covered_by_exhibit(
         cls,
         section: str,
         exhibits: list[ SeasonalExhibit ],
         today: date ) -> bool:
      exhibit = SeasonalExhibit.lookup( section, exhibits )
      return exhibit != None and exhibit.closed_for_season_on( today )


   @classmethod
   def same_animal( cls, website_name: str, app_name: str ) -> bool:
      return WebsitePage.normalize_name( website_name ) == WebsitePage.normalize_name( app_name )


   @classmethod
   def off_in_app(
         cls,
         name: str,
         animals: list[ SeasonalOffDisplayAnimal ],
         today: date ) -> bool:
      return any(
         cls.same_animal( name, animal.name ) and animal.off_for_season_on( today )
         for animal in animals
      )


   @classmethod
   def listed_on_website( cls, name: str, listings: list[ WebsiteOffDisplayAnimal ] ) -> bool:
      return any( cls.same_animal( listing.name, name ) for listing in listings )


   @classmethod
   def website_only(
         cls,
         listings: list[ WebsiteOffDisplayAnimal ],
         animals: list[ SeasonalOffDisplayAnimal ],
         exhibits: list[ SeasonalExhibit ],
         today: date ) -> list[ str ]:
      names = {
         listing.name
         for listing in listings
         if (
            not cls.covered_by_exhibit( listing.section, exhibits, today )
            and not cls.off_in_app( listing.name, animals, today )
         )
      }
      return sorted( names, key=str.casefold )


   @classmethod
   def app_only(
         cls,
         listings: list[ WebsiteOffDisplayAnimal ],
         animals: list[ SeasonalOffDisplayAnimal ],
         today: date ) -> list[ str ]:
      names = {
         animal.name
         for animal in animals
         if animal.off_for_season_on( today ) and not cls.listed_on_website( animal.name, listings )
      }
      return sorted( names, key=str.casefold )


   @classmethod
   def fetch_off_display_animals( cls ) -> list[ WebsiteOffDisplayAnimal ]:
      return cls.parse_website_animals(
         WebsitePage.fetch_text( WebsitePage.url( WebsitePage.ALERTS ) )
      )


   @classmethod
   def load_off_display_animals( cls, database: Path ) -> list[ SeasonalOffDisplayAnimal ]:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         return AnimalCoordinator.get_seasonal_off_display_animals()
      finally:
         RequestConnectionProvider.clear()
         connection.close()


   @classmethod
   def load_seasonal_exhibits( cls, database: Path ) -> list[ SeasonalExhibit ]:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         return ExhibitCoordinator.get_seasonal_exhibits()
      finally:
         RequestConnectionProvider.clear()
         connection.close()


   @classmethod
   def report(
         cls,
         today: date,
         website_only: list[ str ],
         app_only: list[ str ] ) -> None:
      print( CheckReport.heading( 'seasonalOffDisplay', today ) )
      print()
      CheckReport.print_category( AppStringProvider.format( 'checks.offForSeasonWebsiteOnly' ), website_only )
      CheckReport.print_category( AppStringProvider.format( 'checks.offForSeasonAppOnly' ), app_only )


   @classmethod
   def check_schedules( cls, database: Path, today: date ) -> int:
      animals = cls.load_off_display_animals( database )
      exhibits = cls.load_seasonal_exhibits( database )
      listings = cls.fetch_off_display_animals()
      website_only = cls.website_only( listings, animals, exhibits, today )
      app_only = cls.app_only( listings, animals, today )
      cls.report( today, website_only, app_only )
      return CheckReport.count_differences( website_only, app_only )


   @classmethod
   def main( cls ) -> int:
      args = cls.parse_args()

      if not args.database.exists():
         print(
            AppStringProvider.format( 'checks.couldNotFindDatabase' ),
            file=sys.stderr,
         )
         return CheckExitCode.COULD_NOT_FINISH

      try:
         issues = cls.check_schedules( args.database, date.today() )
      except RuntimeError as error:
         print( error, file=sys.stderr )
         return CheckExitCode.COULD_NOT_FINISH

      if issues:
         return CheckExitCode.DIFFERENCES

      return CheckExitCode.CLEAR


if __name__ == '__main__':
   raise SystemExit( SeasonalAnimalOffDisplayChecker.main() )

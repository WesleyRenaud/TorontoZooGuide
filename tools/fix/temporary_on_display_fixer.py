from __future__ import annotations

from pathlib import Path

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.animals.domain.animal_species_exhibit import AnimalSpeciesExhibit
from api.animals.domain.animal_viewing_scope import AnimalViewingScope
from api.animals.domain.temporary_off_display_animal import TemporaryOffDisplayAnimal
from api.app_string_provider import AppStringProvider
from api.database_connection_provider import DatabaseConnectionProvider
from api.request_connection_provider import RequestConnectionProvider
from tools.checks.animal_detail_image import AnimalDetailImage
from tools.checks.check_report import CheckReport


class TemporaryOnDisplayFixer():
   @classmethod
   def line( cls, species: str, exhibit: str ) -> str:
      return CheckReport.join_lines( [
         AppStringProvider.format(
            'format.middleDotPair',
            first=species,
            second=exhibit,
         ),
         CheckReport.detail_item(
            CheckReport.text( 'checks.photo' )
            + AnimalDetailImage.source( exhibit, species )
         ),
         CheckReport.detail_item( CheckReport.text( 'checks.setOnDisplay' ) ),
      ] )


   @classmethod
   def scopes(
         cls,
         enclosure: AnimalSpeciesExhibit,
         animals: list[ TemporaryOffDisplayAnimal ] ) -> list[ AnimalViewingScope ]:
      return [
         animal.scope()
         for animal in animals
         if animal.enclosure() == enclosure
      ]


   @classmethod
   def fix(
         cls,
         database: Path,
         animals: list[ TemporaryOffDisplayAnimal ] ) -> list[ str ]:
      if animals == []:
         return []

      enclosures = list( dict.fromkeys( animal.enclosure() for animal in animals ) )
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         lines = []

         for enclosure in enclosures:
            AnimalCoordinator.set_animal_as_on_display(
               enclosure.species,
               enclosure.exhibit,
               cls.scopes( enclosure, animals ),
            )
            lines.append( cls.line( enclosure.species, enclosure.exhibit ) )

         CheckReport.note_fixed( len( lines ) )
         return sorted( lines, key=str.casefold )
      finally:
         RequestConnectionProvider.clear()
         connection.close()

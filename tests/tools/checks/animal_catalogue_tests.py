from __future__ import annotations

from urllib.parse import quote

from api.animals.domain.animal_species_exhibit import AnimalSpeciesExhibit
from tools.checks.animal_catalogue import AnimalCatalogue


LION = 'African Lion'


def _page( names: list[ str ], exhibit: str = 'Africa Savanna' ) -> str:
   parts = [ f'<h1>{ exhibit }</h1><a href="/animals/africa">Africa</a>' ]

   for name in names:
      href = quote( name, safe='' )
      parts.append( f'<a href="/animals/{ href }" class="thm"></a>' )

   return ''.join( parts )


def Test_ParseWebsiteAnimals_TestHeadingWithBreak_ExpectExhibitName() -> None:
   page = _page( [ LION ], 'Americas Outdoor<br />Mayan Temple Ruins' )

   listings = AnimalCatalogue.parse_website_animals( page )

   assert listings == [
      AnimalSpeciesExhibit(
         species=LION,
         exhibit='Americas Outdoor Mayan Temple Ruins',
      ),
   ]

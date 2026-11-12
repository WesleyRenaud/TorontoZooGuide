from __future__ import annotations

from api_test_support.sqlite_row import make_row

from api.exhibits.data_access.exhibit_species_mapper import ExhibitSpeciesMapper
from api.exhibits.domain.exhibit_species import ExhibitSpecies
from api.types import Types


MAYAN = 'Americas Outdoor Mayan Temple Ruins'
CANADIAN = 'Canadian Domain'
VULTURE = 'Turkey Vulture'
CAPYBARA = 'Capybara'
MOOSE = 'Moose'


def _row( exhibit: str, species: str ) -> Types.Row:
   return make_row( {
      'EXHIBIT': exhibit,
      'SPECIES': species,
   } )


def Test_MapRecords_TestDuplicateSpecies_ExpectOneListPerExhibit() -> None:
   rows = [
      _row( MAYAN, CAPYBARA ),
      _row( MAYAN, VULTURE ),
      _row( MAYAN, VULTURE ),
      _row( CANADIAN, MOOSE ),
   ]

   groups = ExhibitSpeciesMapper.map_records( rows )

   assert groups == [
      ExhibitSpecies( exhibit=MAYAN, species=[ CAPYBARA, VULTURE ] ),
      ExhibitSpecies( exhibit=CANADIAN, species=[ MOOSE ] ),
   ]

from __future__ import annotations

from api_test_support.sqlite_row import make_row

from api.animals.data_access.animal_species_exhibit_mapper import AnimalSpeciesExhibitMapper
from api.animals.domain.animal_species_exhibit import AnimalSpeciesExhibit


SPECIES = 'African Lion'
EXHIBIT = 'Africa Savanna'


def Test_MapRecord_TestRow_ExpectSpeciesAndExhibit() -> None:
   row = make_row( {
      'SPECIES': SPECIES,
      'EXHIBIT': EXHIBIT,
   } )

   animal = AnimalSpeciesExhibitMapper.map_record( row )

   assert animal == AnimalSpeciesExhibit( species=SPECIES, exhibit=EXHIBIT )

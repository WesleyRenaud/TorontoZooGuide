from __future__ import annotations

from datetime import date

from api_test_support.sqlite_row import make_row

from api.animals.data_access.closure_linked_off_display_animal_mapper import ClosureLinkedOffDisplayAnimalMapper
from api.animals.domain.closure_linked_off_display_animal import ClosureLinkedOffDisplayAnimal


SPECIES = 'Sumatran Orangutan'
EXHIBIT = 'Indo-Malaya Pavilion'
TITLE = 'Indoor Orangutan Habitat Closure'


def Test_MapRecords_TestRow_ExpectClosureLinkedAnimal() -> None:
   row = make_row( {
      'SPECIES': SPECIES,
      'EXHIBIT': EXHIBIT,
      'OFF_DISPLAY_END': '2026-11-09',
      'CLOSURE_UPDATE_TITLE': TITLE,
      'CLOSURE_UPDATE_START': '2026-05-13',
   } )

   records = ClosureLinkedOffDisplayAnimalMapper.map_records( [ row ] )

   assert records == [
      ClosureLinkedOffDisplayAnimal(
         species=SPECIES,
         exhibit=EXHIBIT,
         end=date( 2026, 11, 9 ),
         closure_update_title=TITLE,
         closure_update_start=date( 2026, 5, 13 ) ),
   ]

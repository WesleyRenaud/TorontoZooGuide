from __future__ import annotations

from datetime import date

from api.animals.domain.animal_species_exhibit import AnimalSpeciesExhibit
from api.animals.domain.closure_linked_off_display_animal import ClosureLinkedOffDisplayAnimal
from api.animals.domain.closure_linked_off_display_animals import ClosureLinkedOffDisplayAnimals


ORANGUTAN_UPDATE = 'Indoor Orangutan Habitat Closure'
ORANGUTAN_START = date( 2026, 5, 13 )
EURASIA_UPDATE = 'Eurasia Loop Partial Closure'
EURASIA_START = date( 2026, 5, 3 )


def _animal( species: str, title: str, start: date ) -> ClosureLinkedOffDisplayAnimal:
   return ClosureLinkedOffDisplayAnimal(
      species=species,
      exhibit='Indo-Malaya Pavilion',
      end=date( 2026, 11, 9 ),
      closure_update_title=title,
      closure_update_start=start,
   )


def Test_Groups_TestTwoClosures_ExpectOneGroupPerUpdate() -> None:
   orangutan = _animal( 'Sumatran Orangutan', ORANGUTAN_UPDATE, ORANGUTAN_START )
   gibbon = _animal( 'White-Handed Gibbon', ORANGUTAN_UPDATE, ORANGUTAN_START )
   panda = _animal( 'Red Panda', EURASIA_UPDATE, EURASIA_START )

   groups = ClosureLinkedOffDisplayAnimals.groups( [ orangutan, gibbon, panda ] )

   assert groups == [
      ClosureLinkedOffDisplayAnimals(
         title=ORANGUTAN_UPDATE,
         start=ORANGUTAN_START,
         animals=[ orangutan, gibbon ],
      ),
      ClosureLinkedOffDisplayAnimals(
         title=EURASIA_UPDATE,
         start=EURASIA_START,
         animals=[ panda ],
      ),
   ]
   assert groups[ 0 ].ends_on( date( 2026, 11, 9 ) )
   assert groups[ 0 ].enclosures() == [
      AnimalSpeciesExhibit( species='Sumatran Orangutan', exhibit='Indo-Malaya Pavilion' ),
      AnimalSpeciesExhibit( species='White-Handed Gibbon', exhibit='Indo-Malaya Pavilion' ),
   ]

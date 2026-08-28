from __future__ import annotations

from typing import Any

from api.models.animal import Animal
from api.shared.enums import AnimalViewingScope


class StubAnimalCoordinator():
   instances: list[ StubAnimalCoordinator ] = []
   default_success: bool = True


   def __init__(
         self,
         *,
         animal_name: str,
         animal_exhibit: str,
         species_names: list[ str ],
         viewability_likelihood: int = 100 ) -> None:
      self.animal_name = animal_name
      self.animal_exhibit = animal_exhibit
      self.species_names = species_names
      self.viewability_likelihood = viewability_likelihood
      self.calls: list[ tuple[ str, dict[ str, Any ] ] ] = []
      self.closed = False
      StubAnimalCoordinator.instances.append( self )


   def close( self ) -> None:
      self.closed = True


   def get_animals_viewable_on_day( self, **kwargs: Any ) -> list[ Animal ]:
      self.calls.append( ( 'get_animals_viewable_on_day', kwargs ) )
      return [
         Animal(
            species=self.animal_name,
            exhibit=self.animal_exhibit,
            likelihood=self.viewability_likelihood )
      ]


   def get_animal_viewing_scopes(
         self,
         species: str,
         exhibit: str ) -> list[ AnimalViewingScope ]:
      self.calls.append(
         (
            'get_animal_viewing_scopes',
            {
               'species': species,
               'exhibit': exhibit,
            }
         )
      )
      return [ AnimalViewingScope.INDOOR, AnimalViewingScope.OUTDOOR ]


   def get_animal_information( self, species: str, exhibit: str ) -> Animal:
      self.calls.append(
         (
            'get_animal_information',
            {
               'species': species,
               'exhibit': exhibit,
            }
         )
      )
      return Animal( species=species, exhibit=exhibit )


   def get_animal_species_names( self ) -> list[ str ]:
      self.calls.append( ( 'get_animal_species_names', {} ) )
      return list( self.species_names )


   def set_animal_as_off_display( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'set_animal_as_off_display', kwargs ) )
      return StubAnimalCoordinator.default_success


   def set_animal_as_on_display( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'set_animal_as_on_display', kwargs ) )
      return StubAnimalCoordinator.default_success


   def set_animal_limited_viewing_schedule( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'set_animal_limited_viewing_schedule', kwargs ) )
      return StubAnimalCoordinator.default_success


   def remove_animal_visibility_schedule( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'remove_animal_visibility_schedule', kwargs ) )
      return StubAnimalCoordinator.default_success


   def set_animal_viewing_alert( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'set_animal_viewing_alert', kwargs ) )
      return StubAnimalCoordinator.default_success


   def remove_animal_viewing_alert( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'remove_animal_viewing_alert', kwargs ) )
      return StubAnimalCoordinator.default_success

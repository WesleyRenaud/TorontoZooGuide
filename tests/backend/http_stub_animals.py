from __future__ import annotations

from typing import Any

from http_support_constants import ANIMAL_EXHIBIT
from http_support_constants import ANIMAL_NAME

from api.models import Animal
from api.models import Region
from api.models import RegionWithExhibits
from api.shared.enums import AnimalViewingScope

class AnimalsExhibitsStubMixin:
   def get_animals_viewable_on_day( self, **kwargs: Any ) -> list[ Animal ]:
         self.calls.append( ( 'get_animals_viewable_on_day', kwargs ) )
         return [ Animal( species=ANIMAL_NAME, exhibit=ANIMAL_EXHIBIT, likelihood=100 ) ]


   def get_exhibits_in_region( self, region: str ) -> list[ str ]:
         self.calls.append( ( 'get_exhibits_in_region', { 'region': region } ) )
         return [ ANIMAL_EXHIBIT ]


   def get_regions( self ) -> list[ Region ]:
         self.calls.append( ( 'get_regions', {} ) )
         return [ Region( name='Africa', has_exhibits=True ) ]


   def get_names_of_animals_in_exhibit( self, exhibit: str ) -> list[ str ]:
         self.calls.append( ( 'get_names_of_animals_in_exhibit', { 'exhibit': exhibit } ) )
         return [ ANIMAL_NAME ]


   def get_animal_viewing_scopes(
            self,
            species: str,
            exhibit: str ) -> list[ AnimalViewingScope ]:
         self.calls.append(
            (
               'get_animal_viewing_scopes',
               {
                  'species': species,
                  'exhibit': exhibit
               }
            )
         )
         return [ AnimalViewingScope.INDOOR, AnimalViewingScope.OUTDOOR ]


   def get_animal_information( self, species: str ) -> Animal:
         self.calls.append( ( 'get_animal_information', { 'species': species } ) )
         return Animal( species=species, exhibit=ANIMAL_EXHIBIT )


   def get_closed_exhibits( self, **kwargs: Any ) -> list[ str ]:
         self.calls.append( ( 'get_closed_exhibits', kwargs ) )
         return [ ANIMAL_EXHIBIT ]


   def get_closed_exhibits_for_visit_date( self, **kwargs: Any ) -> list[ str ]:
         return self.get_closed_exhibits( **kwargs )


   def get_animals_matching_query( self, **kwargs: Any ) -> list[ Animal ]:
         self.calls.append( ( 'get_animals_matching_query', kwargs ) )
         return [ Animal( species=ANIMAL_NAME, exhibit=ANIMAL_EXHIBIT, likelihood=100 ) ]


   def get_animal_species_names( self ) -> list[ str ]:
         self.calls.append( ( 'get_animal_species_names', {} ) )
         return [ ANIMAL_NAME, 'Amur Tiger' ]


   def get_exhibits( self ) -> list[ str ]:
         self.calls.append( ( 'get_exhibits', {} ) )
         return [ ANIMAL_EXHIBIT, 'Eurasia Wilds' ]


   def get_regions_with_exhibits( self, **kwargs: Any ) -> list[ RegionWithExhibits ]:
         self.calls.append( ( 'get_regions_with_exhibits', kwargs ) )
         return [
            RegionWithExhibits(
               name='Africa',
               exhibits=[ ANIMAL_EXHIBIT ] )
         ]

from __future__ import annotations

from typing import Any

from api.models.region import Region
from api.models.region_with_exhibits import RegionWithExhibits


class StubExhibitCoordinator():
   instances: list[ StubExhibitCoordinator ] = []
   default_success: bool = True


   def __init__(
         self,
         *,
         region_name: str,
         exhibit_name: str,
         animal_names: list[ str ],
         exhibit_names: list[ str ],
         closed_exhibit_names: list[ str ] ) -> None:
      self.region_name = region_name
      self.exhibit_name = exhibit_name
      self.animal_names = animal_names
      self.exhibit_names = exhibit_names
      self.closed_exhibit_names = closed_exhibit_names
      self.calls: list[ tuple[ str, dict[ str, Any ] ] ] = []
      self.closed = False
      StubExhibitCoordinator.instances.append( self )


   def close( self ) -> None:
      self.closed = True


   def get_exhibits_in_region( self, region: str ) -> list[ str ]:
      self.calls.append( ( 'get_exhibits_in_region', { 'region': region } ) )
      return [ self.exhibit_name ]


   def get_regions( self ) -> list[ Region ]:
      self.calls.append( ( 'get_regions', {} ) )
      return [ Region( name=self.region_name, has_exhibits=True ) ]


   def get_names_of_animals_in_exhibit( self, exhibit: str ) -> list[ str ]:
      self.calls.append( ( 'get_names_of_animals_in_exhibit', { 'exhibit': exhibit } ) )
      return list( self.animal_names )


   def get_closed_exhibits_for_visit_date(
         self,
         month: str,
         day: int,
         year: int ) -> list[ str ]:
      self.calls.append(
         (
            'get_closed_exhibits_for_visit_date',
            {
               'month': month,
               'day': day,
               'year': year,
            }
         )
      )
      return list( self.closed_exhibit_names )


   def get_regions_with_exhibits( self ) -> list[ RegionWithExhibits ]:
      self.calls.append( ( 'get_regions_with_exhibits', {} ) )
      return [
         RegionWithExhibits(
            name=self.region_name,
            exhibits=[ self.exhibit_name ] )
      ]


   def get_exhibits( self ) -> list[ str ]:
      self.calls.append( ( 'get_exhibits', {} ) )
      return list( self.exhibit_names )


   def set_exhibit_as_closed( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'set_exhibit_as_closed', kwargs ) )
      return StubExhibitCoordinator.default_success


   def set_exhibit_as_open( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'set_exhibit_as_open', kwargs ) )
      return StubExhibitCoordinator.default_success

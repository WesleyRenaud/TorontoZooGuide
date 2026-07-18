from __future__ import annotations

from collections.abc import Callable
from typing import Any

from http_stub_amenities import AmenitiesStubMixin
from http_stub_animals import AnimalsExhibitsStubMixin
from http_stub_events import EventsStubMixin
from http_stub_itinerary import ItineraryStubMixin
from http_stub_locations import LocationsStubMixin
from http_stub_updates import UpdatesStubMixin
from http_stub_zoo_hours import ZooHoursStubMixin
from http_stub_zoomobile import ZoomobileStubMixin

from api.types import Connection


class StubControllerNamespace:
   def __init__( self, root: StubZooControllers ) -> None:
      self._root = root


   def __getattr__( self, name: str ) -> Any:
      return getattr( self._root, name )


class StubZooControllers( AnimalsExhibitsStubMixin, AmenitiesStubMixin, ZoomobileStubMixin, EventsStubMixin, LocationsStubMixin, UpdatesStubMixin, ItineraryStubMixin, ZooHoursStubMixin ):
   instances: list[ StubZooControllers ] = []
   default_success: bool = True
   controller_attributes: list[ str ] = [
      'animals',
      'exhibits',
      'pavilions',
      'restaurants',
      'restrooms',
      'giftshops',
      'attractions',
      'zoomobile',
      'guardians',
      'wild_encounters',
      'drinking_fountains',
      'defibrillators',
      'emergency_intercoms',
      'guest_services',
      'picnic_sites',
      'event_sites',
      'updates',
      'itinerary',
      'zoo_hours',
   ]


   def __init__( self, conn: Connection | None = None ) -> None:
         self.conn: Connection | None = conn
         self.calls: list[ tuple[ str, dict[ str, Any ] ] ] = []
         self.closed = False
         StubZooControllers.instances.append( self )

         for attribute in self.controller_attributes:
            setattr( self, attribute, StubControllerNamespace( self ) )


   def close( self ) -> None:
         self.closed = True
         self.conn = None


   def __getattr__( self, name: str ) -> Callable[ ..., bool ]:
         mutation_prefixes = (
            'create_',
            'set_',
            'remove_',
            'end_',
            'edit_',
            'cancel_',
            'replace_',
            'trim_'
         )

         if not name.startswith( mutation_prefixes ):
            raise AttributeError( name )

         def mutation_stub( **kwargs: Any ) -> bool:
            self.calls.append( ( name, kwargs ) )
            return StubZooControllers.default_success

         return mutation_stub

from __future__ import annotations

from typing import Any

from http_support_constants import DRINKING_FOUNTAIN_X_COORD
from http_support_constants import DRINKING_FOUNTAIN_Y_COORD

from api.models import Defibrillator
from api.models import DrinkingFountain
from api.models import EmergencyIntercom
from api.models import EventSite
from api.models import GuestService
from api.models import PicnicSite

class LocationsStubMixin:
   def get_drinking_fountains( self, **kwargs: Any ) -> list[ DrinkingFountain ]:
         self.calls.append( ( 'get_drinking_fountains', kwargs ) )
         return [
            DrinkingFountain(
               x_coord=DRINKING_FOUNTAIN_X_COORD,
               y_coord=DRINKING_FOUNTAIN_Y_COORD )
         ]


   def get_defibrillators( self ) -> list[ Defibrillator ]:
         self.calls.append( ( 'get_defibrillators', {} ) )
         return [ Defibrillator( x_coord=12.345, y_coord=67.890 ) ]


   def get_emergency_intercoms( self ) -> list[ EmergencyIntercom ]:
         self.calls.append( ( 'get_emergency_intercoms', {} ) )
         return [ EmergencyIntercom( x_coord=23.456, y_coord=78.901 ) ]


   def get_guest_services( self ) -> list[ GuestService ]:
         self.calls.append( ( 'get_guest_services', {} ) )
         return [
            GuestService(
               service_type='Information',
               x_coord=34.567,
               y_coord=89.012 )
         ]


   def get_picnic_sites( self ) -> list[ PicnicSite ]:
         self.calls.append( ( 'get_picnic_sites', {} ) )
         return [
            PicnicSite(
               x_coord=45.678,
               y_coord=90.123 )
         ]


   def get_event_sites( self ) -> list[ EventSite ]:
         self.calls.append( ( 'get_event_sites', {} ) )
         return [
            EventSite(
               name='Special Events Center',
               x_coord=56.789,
               y_coord=12.345 )
         ]

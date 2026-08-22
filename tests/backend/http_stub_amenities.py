from __future__ import annotations

from typing import Any

from http_support_constants import ATTRACTION_NAME
from http_support_constants import GIFT_SHOP_NAME
from http_support_constants import PAVILION_NAME
from http_support_constants import RESTAURANT_NAME
from http_support_constants import RESTROOM_NAME
from http_support_constants import TRANSPORTATION_NAME

from api.models import Attraction
from api.models import GiftShop
from api.models import Pavilion
from api.models import Restaurant
from api.models import Restroom
from api.models import Transportation

class AmenitiesStubMixin:
   def get_pavilions( self ) -> list[ Pavilion ]:
         self.calls.append( ( 'get_pavilions', {} ) )
         return [ Pavilion( name=PAVILION_NAME, region='Africa' ) ]


   def get_restaurants( self, **kwargs: Any ) -> list[ Restaurant ]:
         self.calls.append( ( 'get_restaurants', kwargs ) )
         return [ Restaurant( name=RESTAURANT_NAME, location='Africa', sub_location=None ) ]


   def get_restrooms( self, **kwargs: Any ) -> list[ Restroom ]:
         self.calls.append( ( 'get_restrooms', kwargs ) )
         return [ Restroom( title=RESTROOM_NAME ) ]


   def get_gift_shops( self, **kwargs: Any ) -> list[ GiftShop ]:
         self.calls.append( ( 'get_gift_shops', kwargs ) )
         return [ GiftShop( name=GIFT_SHOP_NAME, location='Learning & Engagement Centre' ) ]


   def get_attractions( self, **kwargs: Any ) -> list[ Attraction ]:
         self.calls.append( ( 'get_attractions', kwargs ) )
         return [ Attraction( name=ATTRACTION_NAME, free_with_admission=0 ) ]


   def get_pavilions_matching_query( self, query: str ) -> list[ Pavilion ]:
         self.calls.append( ( 'get_pavilions_matching_query', { 'query': query } ) )
         return [ Pavilion( name=PAVILION_NAME, region='Africa' ) ]


   def get_restaurants_matching_query( self, **kwargs: Any ) -> list[ Restaurant ]:
         self.calls.append( ( 'get_restaurants_matching_query', kwargs ) )
         return [ Restaurant( name=RESTAURANT_NAME, location='Africa', sub_location=None ) ]


   def get_restrooms_matching_query( self, **kwargs: Any ) -> list[ Restroom ]:
         self.calls.append( ( 'get_restrooms_matching_query', kwargs ) )
         return [ Restroom( title=RESTROOM_NAME ) ]


   def get_gift_shops_matching_query( self, **kwargs: Any ) -> list[ GiftShop ]:
         self.calls.append( ( 'get_gift_shops_matching_query', kwargs ) )
         return [ GiftShop( name=GIFT_SHOP_NAME, location='Learning & Engagement Centre' ) ]


   def get_attractions_matching_query( self, **kwargs: Any ) -> list[ Attraction ]:
         self.calls.append( ( 'get_attractions_matching_query', kwargs ) )
         return [ Attraction( name=ATTRACTION_NAME, free_with_admission=0 ) ]


   def get_transportations( self, **kwargs: Any ) -> list[ Transportation ]:
         self.calls.append( ( 'get_transportations', kwargs ) )
         return [ Transportation( name=TRANSPORTATION_NAME, is_also_attraction=True ) ]


   def get_transportations_matching_query( self, **kwargs: Any ) -> list[ Transportation ]:
         self.calls.append( ( 'get_transportations_matching_query', kwargs ) )
         return [ Transportation( name=TRANSPORTATION_NAME, is_also_attraction=True ) ]


   def get_restaurant_names( self ) -> list[ str ]:
         self.calls.append( ( 'get_restaurant_names', {} ) )
         return [ RESTAURANT_NAME ]


   def get_restroom_names( self ) -> list[ str ]:
         self.calls.append( ( 'get_restroom_names', {} ) )
         return [ RESTROOM_NAME ]


   def get_gift_shop_names( self ) -> list[ str ]:
         self.calls.append( ( 'get_gift_shop_names', {} ) )
         return [ GIFT_SHOP_NAME ]


   def get_attraction_names( self ) -> list[ str ]:
         self.calls.append( ( 'get_attraction_names', {} ) )
         return [ ATTRACTION_NAME ]

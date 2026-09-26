from __future__ import annotations

from api.models.transportation import Transportation
from api.transportation.search.transportations_matching_query_builder import TransportationsMatchingQueryBuilder


def Test_Build_TestMatchingQuery_ExpectMatchingTransportationOnly() -> None:
   zoomobile = Transportation( name='Zoomobile' )
   gondola = Transportation( name='Gondola' )
   transportations = [ zoomobile, gondola ]
   query = 'zoomobile'

   matches = TransportationsMatchingQueryBuilder.build( transportations, query )

   assert [ transportation.name for transportation in matches ] == [ zoomobile.name ]

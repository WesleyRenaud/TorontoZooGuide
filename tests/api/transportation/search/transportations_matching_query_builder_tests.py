from __future__ import annotations

from api.models.transportation import Transportation
from api.transportation.search.transportations_matching_query_builder import TransportationsMatchingQueryBuilder


def Test_Build_TestMatchingQuery_ExpectMatchingTransportationOnly() -> None:
   transportations = [
      Transportation( name='Zoomobile' ),
      Transportation( name='Gondola' ),
   ]

   matches = TransportationsMatchingQueryBuilder.build( transportations, 'zoomobile' )

   assert [ transportation.name for transportation in matches ] == [ 'Zoomobile' ]

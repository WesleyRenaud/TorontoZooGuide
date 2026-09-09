from enum import Enum

from .shared_enum_values import SharedEnumValues


TransportationRouteId = Enum(
   'TransportationRouteId',
   SharedEnumValues.load( 'transportationRouteId.json' ),
   type=str,
)

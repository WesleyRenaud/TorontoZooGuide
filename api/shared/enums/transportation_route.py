from enum import Enum


class TransportationRouteSource( str, Enum ):
   FALLBACK = 'fallback'
   MANUAL = 'manual'
   OVERRIDE = 'override'


class TransportationRouteId( str, Enum ):
   SUMMER = 'summer'
   WINTER = 'winter'

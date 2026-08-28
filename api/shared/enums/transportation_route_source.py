from enum import Enum


class TransportationRouteSource( str, Enum ):
   FALLBACK = 'fallback'
   MANUAL = 'manual'
   OVERRIDE = 'override'

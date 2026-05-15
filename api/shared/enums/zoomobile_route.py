from enum import Enum


class ZoomobileRouteSource( str, Enum ):
   FALLBACK = 'fallback'
   MANUAL = 'manual'
   OVERRIDE = 'override'


class ZoomobileRouteId( str, Enum ):
   SUMMER = 'summer'
   WINTER = 'winter'

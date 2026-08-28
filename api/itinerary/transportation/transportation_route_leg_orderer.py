from __future__ import annotations

from .transportation_route_leg_segment import TransportationRouteLegSegment


class TransportationRouteLegOrderer():
   @classmethod
   def order_from_station(
         cls,
         legs: list[ TransportationRouteLegSegment ],
         *,
         start_station: str ) -> list[ TransportationRouteLegSegment ]:
      if not legs:
         return []

      outgoing_by_from: dict[ str, TransportationRouteLegSegment ] = {}

      for leg in legs:
         if leg.from_station in outgoing_by_from:
            raise ValueError(
               f'Duplicate outgoing leg from station { repr( leg.from_station ) }' )

         outgoing_by_from[ leg.from_station ] = leg

      ordered: list[ TransportationRouteLegSegment ] = []
      current_station = start_station

      for _ in range( len( outgoing_by_from ) ):
         next_leg = outgoing_by_from.get( current_station )

         if next_leg is None:
            raise ValueError(
               f'No outgoing leg from station { repr( current_station ) }' )

         ordered.append( next_leg )
         current_station = next_leg.to_station

      if current_station != start_station:
         raise ValueError(
            f'Route legs from { repr( start_station ) } do not form a closed loop' )

      return ordered

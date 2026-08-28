from __future__ import annotations

from ..data_access.guardians_talk_animal_record import GuardiansTalkAnimalRecord
from ...walk_graph.domain.master_route_loop import MasterRouteLoop
from ...walk_graph.domain.master_route_stop_checker import MasterRouteStopChecker


class GuardiansTalkLoopViewingSpotIndexResolver():
   @classmethod
   def resolve(
         cls,
         master_route_loop: MasterRouteLoop,
         *,
         talk_name: str,
         talk_location: str,
         linked_animals: list[ GuardiansTalkAnimalRecord ] | None = None ) -> int | None:
      for linked_animal in linked_animals or []:
         index = cls._index_for_enclosure(
            master_route_loop,
            species=linked_animal.species,
            exhibit=linked_animal.exhibit,
            enclosure_name=linked_animal.enclosure_name )

         if index is not None:
            return index

      for index, viewing_spot in enumerate( master_route_loop.viewing_spots ):
         # Guardians-talk pins resolve against animal stops only.
         if not MasterRouteStopChecker.is_animal( viewing_spot ):
            continue

         if (
               viewing_spot.species == talk_name
               and viewing_spot.exhibit == talk_location ):
            return index

      return None


   @classmethod
   def _index_for_enclosure(
         cls,
         master_route_loop: MasterRouteLoop,
         *,
         species: str,
         exhibit: str,
         enclosure_name: str | None ) -> int | None:
      return next(
         (
            index
            for index, viewing_spot in enumerate( master_route_loop.viewing_spots )
            if (
               # Guardians-talk enclosure pins resolve against animal stops only.
               MasterRouteStopChecker.is_animal( viewing_spot )
               and viewing_spot.species == species
               and viewing_spot.exhibit == exhibit
               and viewing_spot.name == enclosure_name )
         ),
         None )

from __future__ import annotations

from ...guardians.data_access.guardians_talk_animal_provider import GuardiansTalkAnimalProvider
from ...guardians.data_access.guardians_talk_animal_record import GuardiansTalkAnimalRecord
from ...itinerary.routing.itinerary_stop import ItineraryStop
from ...itinerary.routing.loop_schedule_pin import LoopSchedulePin
from ...models import GuardiansTalk
from ...shared.calendar_dates import DateValues
from ...types import Connection
from ...walk_graph.domain.master_route_loop import MasterRouteLoop
from ...walk_graph.domain.master_route_stop import is_animal_route_stop
from ...walk_graph.master_route_provider import MasterRouteProvider


def resolve_guardians_talk_loop_pin(
      conn: Connection,
      guardians_talk: GuardiansTalk,
      itinerary_stop: ItineraryStop ) -> LoopSchedulePin | None:
   start_seconds = DateValues.time_value_in_seconds( itinerary_stop.start_time )
   end_seconds = DateValues.time_value_in_seconds( itinerary_stop.end_time )

   if start_seconds is None or end_seconds is None:
      return None

   linked_animals = GuardiansTalkAnimalProvider.fetch_animal_links(
      conn,
      guardians_talk.name )
   loops_by_id = MasterRouteProvider.loops_by_id()

   for loop_id, master_route_loop in loops_by_id.items():
      viewing_spot_index = viewing_spot_index_for_talk_in_loop(
         master_route_loop,
         talk_name=guardians_talk.name,
         talk_location=guardians_talk.location,
         linked_animals=linked_animals )

      if viewing_spot_index is not None:
         return LoopSchedulePin(
            loop_id=loop_id,
            viewing_spot_index=viewing_spot_index,
            stop=itinerary_stop,
            start_seconds=start_seconds,
            end_seconds=end_seconds )

   return None


def viewing_spot_index_for_talk_in_loop(
      master_route_loop: MasterRouteLoop,
      *,
      talk_name: str,
      talk_location: str,
      linked_animals: list[ GuardiansTalkAnimalRecord ] | None = None ) -> int | None:
   for linked_animal in linked_animals or []:
      index = _viewing_spot_index_for_enclosure(
         master_route_loop,
         species=linked_animal.species,
         exhibit=linked_animal.exhibit,
         enclosure_name=linked_animal.enclosure_name )

      if index is not None:
         return index

   for index, viewing_spot in enumerate( master_route_loop.viewing_spots ):
      # Guardians-talk pins resolve against animal stops only.
      if not is_animal_route_stop( viewing_spot ):
         continue

      if (
            viewing_spot.species == talk_name
            and viewing_spot.exhibit == talk_location ):
         return index

   return None


def _viewing_spot_index_for_enclosure(
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
            is_animal_route_stop( viewing_spot )
            and viewing_spot.species == species
            and viewing_spot.exhibit == exhibit
            and viewing_spot.name == enclosure_name )
      ),
      None )

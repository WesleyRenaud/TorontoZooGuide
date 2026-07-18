from __future__ import annotations

from ...shared.enums import ScheduleItemKind


AnimalMasterRouteStopKey = tuple[ ScheduleItemKind, str, str, str | None ]
AttractionMasterRouteStopKey = tuple[ ScheduleItemKind, str ]
MasterRouteStopKey = AnimalMasterRouteStopKey | AttractionMasterRouteStopKey


def animal_master_route_stop_key(
      species: str,
      exhibit: str,
      name: str | None ) -> AnimalMasterRouteStopKey:
   return ( ScheduleItemKind.ANIMAL, species, exhibit, name )


def attraction_master_route_stop_key(
      name: str ) -> AttractionMasterRouteStopKey:
   return ( ScheduleItemKind.ATTRACTION, name )

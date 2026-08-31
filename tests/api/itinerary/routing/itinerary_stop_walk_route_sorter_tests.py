from __future__ import annotations

from api.itinerary.routing.itinerary_stop import ENTRANCE_ITEM_KEY
from api.itinerary.routing.itinerary_stop import ItineraryStop
from api.itinerary.routing.itinerary_stop_walk_route_sorter import ItineraryStopWalkRouteSorter
from api.shared.enums import ScheduleItemKind


ENTRANCE_STOP = ItineraryStop(
   schedule_item_kind=ScheduleItemKind.ENTRANCE,
   item_key=ENTRANCE_ITEM_KEY,
   walk_node_ids=[ 'n-1' ],
)

UNSCHEDULED_LION_STOP = ItineraryStop(
   schedule_item_kind=ScheduleItemKind.ANIMAL,
   item_key='African Lion||Africa Savanna',
   walk_node_ids=[ 'n-2' ],
)

SCHEDULED_LION_STOP = ItineraryStop(
   schedule_item_kind=ScheduleItemKind.ANIMAL,
   item_key='African Lion||Africa Savanna',
   walk_node_ids=[ 'n-2' ],
   is_fixed_time=True,
   start_time='2:00 PM',
   end_time='2:30 PM',
)

SCHEDULED_ENCOUNTER_STOP = ItineraryStop(
   schedule_item_kind=ScheduleItemKind.WILD_ENCOUNTER,
   item_key='Guardians of White Rhinos',
   walk_node_ids=[ 'n-3' ],
   meeting_spot='Wild Encounter - Penguin Meeting Spot',
   is_fixed_time=True,
   start_time='11:00 AM',
   end_time='11:45 AM',
)


def Test_Sort_TestUnscheduledStopsOnly_ExpectEmptyList() -> None:
   assert ItineraryStopWalkRouteSorter.sort(
      [ ENTRANCE_STOP, UNSCHEDULED_LION_STOP ] ) == []


def Test_Sort_TestScheduledStops_ExpectEntranceFirstThenStartTimeOrder() -> None:
   ordered_stops = ItineraryStopWalkRouteSorter.sort(
      [ ENTRANCE_STOP, SCHEDULED_LION_STOP, SCHEDULED_ENCOUNTER_STOP ] )

   assert [ stop.item_key for stop in ordered_stops ] == [
      ENTRANCE_ITEM_KEY,
      'Guardians of White Rhinos',
      'African Lion||Africa Savanna',
   ]

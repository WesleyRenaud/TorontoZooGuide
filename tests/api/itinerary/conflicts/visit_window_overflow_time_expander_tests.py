from __future__ import annotations

import pytest

from api.itinerary.conflicts.visit_window_overflow_time_expander import VisitWindowOverflowTimeExpander
from api.itinerary.results.itinerary_save_issue_item import ItinerarySaveIssueItem
from api.itinerary.scheduling.items.schedule_item_travel_time_calculator import ScheduleItemTravelTimeCalculator
from api.shared.calendar_dates import DateValues
from api.shared.enums import ItinerarySaveIssueItemType
from api.shared.enums import ItineraryVisitWindowOverflowEnd


ARRIVAL_TIME = '11:00 AM'
DEPARTURE_TIME = '1:00 PM'
TRAVEL_SECONDS = 600


@pytest.fixture
def stub_overflow_travel( monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      ScheduleItemTravelTimeCalculator,
      'walk_node_id_for_attraction',
      lambda name: 'n-attraction' )
   monkeypatch.setattr(
      ScheduleItemTravelTimeCalculator,
      'walk_node_id_for_guardians_talk',
      lambda name, location='': 'n-talk' )
   monkeypatch.setattr(
      ScheduleItemTravelTimeCalculator,
      'walk_node_id_for_wild_encounter',
      lambda meeting_spot: 'n-encounter' )
   monkeypatch.setattr(
      ScheduleItemTravelTimeCalculator,
      'entrance_travel_seconds_to_walk_node',
      lambda walk_node_id: TRAVEL_SECONDS )
   monkeypatch.setattr(
      ScheduleItemTravelTimeCalculator,
      'entrance_travel_seconds_from_walk_node',
      lambda walk_node_id: TRAVEL_SECONDS )


def _issue_item(
      *,
      name: str,
      start_time: str,
      end_time: str,
      overflow_end: ItineraryVisitWindowOverflowEnd,
      item_type: str = ItinerarySaveIssueItemType.ATTRACTION ) -> ItinerarySaveIssueItem:
   return ItinerarySaveIssueItem(
      name=name,
      start_time=start_time,
      end_time=end_time,
      item_type=item_type,
      overflow_end=overflow_end )


def Test_Expand_TestDropAll_ExpectUnchangedTimes(
      stub_overflow_travel: None ) -> None:
   arrival_time, departure_time = VisitWindowOverflowTimeExpander.expand(
      ARRIVAL_TIME,
      DEPARTURE_TIME,
      [] )

   assert arrival_time == ARRIVAL_TIME
   assert departure_time == DEPARTURE_TIME


def Test_Expand_TestKeepArrivalOnly_ExpectArrivalMoved(
      stub_overflow_travel: None ) -> None:
   kept_item = _issue_item(
      name='Splash Island',
      start_time='10:00 AM',
      end_time='10:30 AM',
      overflow_end=ItineraryVisitWindowOverflowEnd.ARRIVAL )

   arrival_time, departure_time = VisitWindowOverflowTimeExpander.expand(
      ARRIVAL_TIME,
      DEPARTURE_TIME,
      [ kept_item ] )

   assert arrival_time == DateValues.schedule_time_key_from_seconds(
      ( DateValues.time_value_in_seconds( kept_item.start_time ) or 0 )
      - TRAVEL_SECONDS )
   assert departure_time == DEPARTURE_TIME


def Test_Expand_TestKeepDepartureOnly_ExpectDepartureMoved(
      stub_overflow_travel: None ) -> None:
   kept_item = _issue_item(
      name='Splash Island',
      start_time='12:30 PM',
      end_time='2:00 PM',
      overflow_end=ItineraryVisitWindowOverflowEnd.DEPARTURE )

   arrival_time, departure_time = VisitWindowOverflowTimeExpander.expand(
      ARRIVAL_TIME,
      DEPARTURE_TIME,
      [ kept_item ] )

   assert arrival_time == ARRIVAL_TIME
   assert departure_time == DateValues.schedule_time_key_from_seconds(
      ( DateValues.time_value_in_seconds( kept_item.end_time ) or 0 )
      + TRAVEL_SECONDS )


def Test_Expand_TestKeepBothEnds_ExpectBothMoved(
      stub_overflow_travel: None ) -> None:
   kept_item = _issue_item(
      name='African Lion',
      start_time='10:00 AM',
      end_time='2:00 PM',
      overflow_end=ItineraryVisitWindowOverflowEnd.BOTH,
      item_type=ItinerarySaveIssueItemType.GUARDIANS_TALK )

   arrival_time, departure_time = VisitWindowOverflowTimeExpander.expand(
      ARRIVAL_TIME,
      DEPARTURE_TIME,
      [ kept_item ] )

   assert arrival_time == DateValues.schedule_time_key_from_seconds(
      ( DateValues.time_value_in_seconds( kept_item.start_time ) or 0 )
      - TRAVEL_SECONDS )
   assert departure_time == DateValues.schedule_time_key_from_seconds(
      ( DateValues.time_value_in_seconds( kept_item.end_time ) or 0 )
      + TRAVEL_SECONDS )


def Test_Expand_TestKeepOneOfTwoPinching_ExpectOnlyThatEndMoved(
      stub_overflow_travel: None ) -> None:
   arrival_item = _issue_item(
      name='Morning Ride',
      start_time='10:00 AM',
      end_time='10:20 AM',
      overflow_end=ItineraryVisitWindowOverflowEnd.ARRIVAL )

   arrival_time, departure_time = VisitWindowOverflowTimeExpander.expand(
      ARRIVAL_TIME,
      DEPARTURE_TIME,
      [ arrival_item ] )

   assert arrival_time == DateValues.schedule_time_key_from_seconds(
      ( DateValues.time_value_in_seconds( arrival_item.start_time ) or 0 )
      - TRAVEL_SECONDS )
   assert departure_time == DEPARTURE_TIME


def Test_Expand_TestKeepEncounter_ExpectDepartureMoved(
      stub_overflow_travel: None ) -> None:
   kept_item = _issue_item(
      name='African Rainforest',
      start_time='12:30 PM',
      end_time='2:00 PM',
      overflow_end=ItineraryVisitWindowOverflowEnd.DEPARTURE,
      item_type=ItinerarySaveIssueItemType.WILD_ENCOUNTER )

   arrival_time, departure_time = VisitWindowOverflowTimeExpander.expand(
      ARRIVAL_TIME,
      DEPARTURE_TIME,
      [ kept_item ] )

   assert arrival_time == ARRIVAL_TIME
   assert departure_time == DateValues.schedule_time_key_from_seconds(
      ( DateValues.time_value_in_seconds( kept_item.end_time ) or 0 )
      + TRAVEL_SECONDS )


def Test_Expand_TestUnknownItemType_ExpectWalkNodeNone(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   walked_nodes: list[ str | None ] = []
   kept_item = _issue_item(
      name='African Lion',
      start_time='10:00 AM',
      end_time='10:30 AM',
      overflow_end=ItineraryVisitWindowOverflowEnd.ARRIVAL,
      item_type=ItinerarySaveIssueItemType.ANIMAL )
   monkeypatch.setattr(
      ScheduleItemTravelTimeCalculator,
      'entrance_travel_seconds_to_walk_node',
      lambda walk_node_id: walked_nodes.append( walk_node_id ) or 0 )

   arrival_time, departure_time = VisitWindowOverflowTimeExpander.expand(
      ARRIVAL_TIME,
      DEPARTURE_TIME,
      [ kept_item ] )

   assert walked_nodes == [ None ]
   assert arrival_time == kept_item.start_time
   assert departure_time == DEPARTURE_TIME

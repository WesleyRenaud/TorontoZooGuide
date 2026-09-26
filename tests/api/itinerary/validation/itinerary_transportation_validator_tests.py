from __future__ import annotations

from datetime import date

import pytest

from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.itinerary.data_access.itinerary_transportation_input import ItineraryTransportationInput
from api.itinerary.data_access.itinerary_transportation_record import ItineraryTransportationRecord
from api.itinerary.transportation.transportation_day_loop import TransportationDayLoop
from api.itinerary.transportation.transportation_route_leg_segment import TransportationRouteLegSegment
from api.itinerary.validation.itinerary_transportation_validator import ItineraryTransportationValidator
from api.models.itinerary_transportation_leg import ItineraryTransportationLeg
from api.shared.calendar_dates import DateValues
from api.shared.enums.position import Position
from api.shared.enums.transportation_name import TransportationName


VISIT_DATE = date( 2026, 6, 15 )
PREVIOUS_VISIT_DATE = date( 2026, 6, 14 )
MAIN = 'Main Zoomobile Station'
CANADA = 'Canadian Domain Zoomobile Station'
AFRICA = 'Africa Zoomobile Station'
ROUTE = 'summer'
ATTRACTION_LIKELIHOOD = 80
ARRIVAL_TIME = '9:00 AM'
DEPARTURE_TIME = '5:00 PM'
ROUTE_MARKER_SEQUENCES = [ [ 'm-a' ] ]
FIRST_LEG_DURATION_MINUTES = 20
SECOND_LEG_DURATION_MINUTES = 10
CARRYOVER_START_TIME = '10:00 AM'
CARRYOVER_END_TIME = DateValues.add_minutes_to_time(
   CARRYOVER_START_TIME,
   FIRST_LEG_DURATION_MINUTES )

CARRYOVER_LEG = ItineraryTransportationLeg(
   transportation=TransportationName.ZOOMOBILE,
   from_station=MAIN,
   to_station=CANADA,
   start_time=CARRYOVER_START_TIME,
   end_time=CARRYOVER_END_TIME,
   added_as_attraction=True )

SAVED_ROW = ItineraryTransportationRecord(
   transportation=TransportationName.ZOOMOBILE,
   old_likelihood=None,
   new_likelihood=100,
   added_as_attraction=True,
   start_time=CARRYOVER_START_TIME,
   end_time=CARRYOVER_END_TIME,
   bulk_transit_evaluated=True,
   legs=[ CARRYOVER_LEG ],
)

DAY_LOOP = TransportationDayLoop(
   transportation=TransportationName.ZOOMOBILE,
   route=ROUTE,
   main_station=MAIN,
   legs=[
      TransportationRouteLegSegment( MAIN, CANADA, FIRST_LEG_DURATION_MINUTES ),
      TransportationRouteLegSegment( CANADA, AFRICA, SECOND_LEG_DURATION_MINUTES ),
   ],
)


@pytest.fixture
def stub_transportation_validator( monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      AttractionCoordinator,
      'get_attraction_likelihood_for_visit_date',
      lambda **kwargs: ATTRACTION_LIKELIHOOD )


def Test_Validate_TestVisitDateChangingWithDayLoop_ExpectExpandedLegsAndRoute(
      stub_transportation_validator: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   transportation = ItineraryTransportationInput(
      name=TransportationName.ZOOMOBILE,
      added_as_attraction=True )
   first_leg_end = DateValues.add_minutes_to_time(
      SAVED_ROW.start_time,
      DAY_LOOP.legs[ Position.FIRST ].duration_minutes )
   expanded_end_time = DateValues.add_minutes_to_time(
      first_leg_end,
      DAY_LOOP.legs[ Position.SECOND ].duration_minutes )
   monkeypatch.setattr(
      'api.itinerary.validation.itinerary_transportation_validator.TransportationDayLoopFetcher.fetch',
      lambda conn, *, transportation, target_date: DAY_LOOP )
   monkeypatch.setattr(
      'api.itinerary.validation.itinerary_transportation_validator.TransportationRouteResolver.resolve_for_date',
      lambda conn, *, transportation, target_date: DAY_LOOP.route )
   monkeypatch.setattr(
      'api.itinerary.validation.itinerary_transportation_validator.TransportationRouteMarkerSequencesBuilder.build',
      lambda conn, *, transportation, route, legs: ROUTE_MARKER_SEQUENCES )

   diffs = ItineraryTransportationValidator.validate(
      AttractionCoordinator,
      None,
      [ transportation ],
      VISIT_DATE,
      arrival_time=ARRIVAL_TIME,
      departure_time=DEPARTURE_TIME,
      old_visit_date=PREVIOUS_VISIT_DATE.isoformat(),
      saved_transportation_rows=[ SAVED_ROW ],
      visit_date_is_changing=True )

   diff = diffs[ Position.FIRST ]
   assert len( diffs ) == 1
   assert diff.name == transportation.name
   assert diff.new_likelihood == ATTRACTION_LIKELIHOOD
   assert diff.start_time == SAVED_ROW.start_time
   assert diff.end_time == expanded_end_time
   assert diff.route == DAY_LOOP.route
   assert len( diff.legs ) == len( DAY_LOOP.legs )
   assert diff.route_marker_sequences == ROUTE_MARKER_SEQUENCES
   assert diff.bulk_transit_evaluated is False


def Test_Validate_TestVisitDateChangingWithoutDayLoop_ExpectEmptyLegs(
      stub_transportation_validator: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   transportation = ItineraryTransportationInput(
      name=TransportationName.ZOOMOBILE,
      added_as_attraction=True )
   monkeypatch.setattr(
      'api.itinerary.validation.itinerary_transportation_validator.TransportationDayLoopFetcher.fetch',
      lambda conn, *, transportation, target_date: None )

   diffs = ItineraryTransportationValidator.validate(
      AttractionCoordinator,
      None,
      [ transportation ],
      VISIT_DATE,
      arrival_time=ARRIVAL_TIME,
      departure_time=DEPARTURE_TIME,
      old_visit_date=PREVIOUS_VISIT_DATE.isoformat(),
      saved_transportation_rows=[ SAVED_ROW ],
      visit_date_is_changing=True )

   diff = diffs[ Position.FIRST ]
   assert len( diffs ) == 1
   assert diff.legs == []
   assert diff.route is None


def Test_Validate_TestSameVisitDateWithCarryoverLegs_ExpectLegsPreserved(
      stub_transportation_validator: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   transportation = ItineraryTransportationInput(
      name=TransportationName.ZOOMOBILE,
      added_as_attraction=True )
   monkeypatch.setattr(
      'api.itinerary.validation.itinerary_transportation_validator.TransportationRouteResolver.resolve_for_date',
      lambda conn, *, transportation, target_date: DAY_LOOP.route )
   monkeypatch.setattr(
      'api.itinerary.validation.itinerary_transportation_validator.TransportationRouteMarkerSequencesBuilder.build',
      lambda conn, *, transportation, route, legs: ROUTE_MARKER_SEQUENCES )

   diffs = ItineraryTransportationValidator.validate(
      AttractionCoordinator,
      None,
      [ transportation ],
      VISIT_DATE,
      arrival_time=ARRIVAL_TIME,
      departure_time=DEPARTURE_TIME,
      old_visit_date=VISIT_DATE.isoformat(),
      saved_transportation_rows=[ SAVED_ROW ],
      visit_date_is_changing=False )

   diff = diffs[ Position.FIRST ]
   assert len( diffs ) == 1
   assert diff.legs == [ CARRYOVER_LEG ]
   assert diff.bulk_transit_evaluated is SAVED_ROW.bulk_transit_evaluated
   assert diff.route == DAY_LOOP.route


def Test_Validate_TestScheduleOutsideVisitWindow_ExpectClearedLegs(
      stub_transportation_validator: None ) -> None:
   transportation = ItineraryTransportationInput(
      name=TransportationName.ZOOMOBILE,
      added_as_attraction=True )
   arrival_after_ride = DateValues.add_minutes_to_time(
      SAVED_ROW.start_time,
      DateValues.time_value_in_minutes( '01:00' ) )

   diffs = ItineraryTransportationValidator.validate(
      AttractionCoordinator,
      None,
      [ transportation ],
      VISIT_DATE,
      arrival_time=arrival_after_ride,
      departure_time=DEPARTURE_TIME,
      old_visit_date=VISIT_DATE.isoformat(),
      saved_transportation_rows=[ SAVED_ROW ],
      visit_date_is_changing=False )

   diff = diffs[ Position.FIRST ]
   assert len( diffs ) == 1
   assert diff.start_time is None
   assert diff.end_time is None
   assert diff.legs == []

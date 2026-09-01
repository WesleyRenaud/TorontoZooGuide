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


VISIT_DATE = date( 2026, 6, 15 )
ZOOMOBILE = 'Zoomobile'
MAIN = 'Main Zoomobile Station'
CANADA = 'Canadian Domain Zoomobile Station'
AFRICA = 'Africa Zoomobile Station'

CARRYOVER_LEG = ItineraryTransportationLeg(
   transportation=ZOOMOBILE,
   from_station=MAIN,
   to_station=CANADA,
   start_time='10:00 AM',
   end_time='10:20 AM',
   added_as_attraction=True )

SAVED_ROW = ItineraryTransportationRecord(
   transportation=ZOOMOBILE,
   old_likelihood=None,
   new_likelihood=100,
   added_as_attraction=True,
   start_time='10:00 AM',
   end_time='10:20 AM',
   bulk_transit_evaluated=True,
   legs=[ CARRYOVER_LEG ],
)

DAY_LOOP = TransportationDayLoop(
   transportation=ZOOMOBILE,
   route='summer',
   main_station=MAIN,
   legs=[
      TransportationRouteLegSegment( MAIN, CANADA, 20 ),
      TransportationRouteLegSegment( CANADA, AFRICA, 10 ),
   ],
)


@pytest.fixture
def stub_transportation_validator( monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      AttractionCoordinator,
      'get_attraction_likelihood_for_visit_date',
      lambda **kwargs: 80 )


def Test_Validate_TestVisitDateChangingWithDayLoop_ExpectExpandedLegsAndRoute(
      stub_transportation_validator: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.validation.itinerary_transportation_validator.TransportationDayLoopFetcher.fetch',
      lambda conn, *, transportation, target_date: DAY_LOOP )
   monkeypatch.setattr(
      'api.itinerary.validation.itinerary_transportation_validator.TransportationRouteResolver.resolve_for_date',
      lambda conn, *, transportation, target_date: 'summer' )
   monkeypatch.setattr(
      'api.itinerary.validation.itinerary_transportation_validator.TransportationRouteMarkerSequencesBuilder.build',
      lambda conn, *, transportation, route, legs: [ [ 'm-a' ] ] )

   diffs = ItineraryTransportationValidator.validate(
      AttractionCoordinator,
      None,
      [ ItineraryTransportationInput( name=ZOOMOBILE, added_as_attraction=True ) ],
      VISIT_DATE,
      arrival_time='9:00 AM',
      departure_time='5:00 PM',
      old_visit_date='2026-06-14',
      saved_transportation_rows=[ SAVED_ROW ],
      visit_date_is_changing=True )

   assert len( diffs ) == 1
   assert diffs[ 0 ].name == ZOOMOBILE
   assert diffs[ 0 ].new_likelihood == 80
   assert diffs[ 0 ].start_time == '10:00 AM'
   assert diffs[ 0 ].end_time == '10:30 AM'
   assert diffs[ 0 ].route == 'summer'
   assert len( diffs[ 0 ].legs ) == 2
   assert diffs[ 0 ].route_marker_sequences == [ [ 'm-a' ] ]
   assert diffs[ 0 ].bulk_transit_evaluated is False


def Test_Validate_TestVisitDateChangingWithoutDayLoop_ExpectEmptyLegs(
      stub_transportation_validator: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.validation.itinerary_transportation_validator.TransportationDayLoopFetcher.fetch',
      lambda conn, *, transportation, target_date: None )

   diffs = ItineraryTransportationValidator.validate(
      AttractionCoordinator,
      None,
      [ ItineraryTransportationInput( name=ZOOMOBILE, added_as_attraction=True ) ],
      VISIT_DATE,
      arrival_time='9:00 AM',
      departure_time='5:00 PM',
      old_visit_date='2026-06-14',
      saved_transportation_rows=[ SAVED_ROW ],
      visit_date_is_changing=True )

   assert len( diffs ) == 1
   assert diffs[ 0 ].legs == []
   assert diffs[ 0 ].route is None


def Test_Validate_TestSameVisitDateWithCarryoverLegs_ExpectLegsPreserved(
      stub_transportation_validator: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.validation.itinerary_transportation_validator.TransportationRouteResolver.resolve_for_date',
      lambda conn, *, transportation, target_date: 'summer' )
   monkeypatch.setattr(
      'api.itinerary.validation.itinerary_transportation_validator.TransportationRouteMarkerSequencesBuilder.build',
      lambda conn, *, transportation, route, legs: [ [ 'm-a' ] ] )

   diffs = ItineraryTransportationValidator.validate(
      AttractionCoordinator,
      None,
      [ ItineraryTransportationInput( name=ZOOMOBILE, added_as_attraction=True ) ],
      VISIT_DATE,
      arrival_time='9:00 AM',
      departure_time='5:00 PM',
      old_visit_date='2026-06-15',
      saved_transportation_rows=[ SAVED_ROW ],
      visit_date_is_changing=False )

   assert len( diffs ) == 1
   assert diffs[ 0 ].legs == [ CARRYOVER_LEG ]
   assert diffs[ 0 ].bulk_transit_evaluated is True
   assert diffs[ 0 ].route == 'summer'


def Test_Validate_TestScheduleOutsideVisitWindow_ExpectClearedLegs(
      stub_transportation_validator: None ) -> None:
   diffs = ItineraryTransportationValidator.validate(
      AttractionCoordinator,
      None,
      [ ItineraryTransportationInput( name=ZOOMOBILE, added_as_attraction=True ) ],
      VISIT_DATE,
      arrival_time='11:00 AM',
      departure_time='5:00 PM',
      old_visit_date='2026-06-15',
      saved_transportation_rows=[ SAVED_ROW ],
      visit_date_is_changing=False )

   assert len( diffs ) == 1
   assert diffs[ 0 ].start_time is None
   assert diffs[ 0 ].end_time is None
   assert diffs[ 0 ].legs == []

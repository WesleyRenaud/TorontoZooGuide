from __future__ import annotations

from datetime import date

import pytest

from api.itinerary.transportation.transportation_day_loop import TransportationDayLoop
from api.itinerary.transportation.transportation_day_loop_fetcher import TransportationDayLoopFetcher
from api.itinerary.transportation.transportation_route_duration_resolver import TransportationRouteDurationResolver
from api.itinerary.transportation.transportation_route_leg_segment import TransportationRouteLegSegment


VISIT_DATE = date( 2026, 6, 15 )
ZOOMOBILE = 'Zoomobile'
MAIN = 'Main Zoomobile Station'
CANADA = 'Canadian Domain Zoomobile Station'
AFRICA = 'Africa Zoomobile Station'

SUMMER_LOOP = TransportationDayLoop(
   transportation=ZOOMOBILE,
   route='summer',
   main_station=MAIN,
   legs=[
      TransportationRouteLegSegment( MAIN, CANADA, 20 ),
      TransportationRouteLegSegment( CANADA, AFRICA, 10 ),
      TransportationRouteLegSegment( AFRICA, MAIN, 45 ),
   ],
)


def Test_Minutes_TestSummerLoop_ExpectDurationSum(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      TransportationDayLoopFetcher,
      'fetch',
      lambda conn, *, transportation, target_date: SUMMER_LOOP )

   assert TransportationRouteDurationResolver.minutes(
      None,
      transportation=ZOOMOBILE,
      target_date=VISIT_DATE ) == 75


def Test_Minutes_TestMissingLoop_ExpectNone(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      TransportationDayLoopFetcher,
      'fetch',
      lambda conn, *, transportation, target_date: None )

   assert TransportationRouteDurationResolver.minutes(
      None,
      transportation=ZOOMOBILE,
      target_date=VISIT_DATE ) is None

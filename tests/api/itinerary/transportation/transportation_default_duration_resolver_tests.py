from __future__ import annotations

import pytest

from api.itinerary.data_access.itinerary_provider import ItineraryProvider
from api.itinerary.transportation.transportation_day_loop import TransportationDayLoop
from api.itinerary.transportation.transportation_day_loop_fetcher import TransportationDayLoopFetcher
from api.itinerary.transportation.transportation_default_duration_resolver import TransportationDefaultDurationResolver
from api.itinerary.transportation.transportation_route_leg_segment import TransportationRouteLegSegment
from api.shared.enums.transportation_name import TransportationName


MAIN = 'Main Zoomobile Station'
CANADA = 'Canadian Domain Zoomobile Station'
SUMMER_LOOP = TransportationDayLoop(
   transportation=TransportationName.ZOOMOBILE,
   route='summer',
   main_station=MAIN,
   legs=[
      TransportationRouteLegSegment( MAIN, CANADA, 20 ),
   ],
)


def Test_Resolve_TestVisitDateAndLoop_ExpectDurationSeconds(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_date',
      lambda conn: '2026-06-15' )
   monkeypatch.setattr(
      TransportationDayLoopFetcher,
      'fetch',
      lambda conn, *, transportation, target_date: SUMMER_LOOP )

   assert TransportationDefaultDurationResolver.resolve(
      None,
      TransportationName.ZOOMOBILE ) == 20 * 60


def Test_Resolve_TestMissingVisitDate_ExpectNone(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_date',
      lambda conn: None )

   assert TransportationDefaultDurationResolver.resolve(
      None,
      TransportationName.ZOOMOBILE ) is None


def Test_Resolve_TestMissingLoop_ExpectNone(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_date',
      lambda conn: '2026-06-15' )
   monkeypatch.setattr(
      TransportationDayLoopFetcher,
      'fetch',
      lambda conn, *, transportation, target_date: None )

   assert TransportationDefaultDurationResolver.resolve(
      None,
      TransportationName.ZOOMOBILE ) is None

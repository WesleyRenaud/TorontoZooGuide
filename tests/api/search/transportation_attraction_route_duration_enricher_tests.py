from __future__ import annotations

from datetime import date
from typing import cast

import pytest

from api.models.attraction import Attraction
from api.request_connection_provider import RequestConnectionProvider
from api.search.transportation_attraction_route_duration_enricher import TransportationAttractionRouteDurationEnricher
from api.types import Types


VISIT_DATE = date( 2026, 6, 15 )
ROUTE_DURATION_MINUTES = 75
STUB_CONNECTION = cast( Types.Connection, None )


@pytest.fixture
def stub_request_connection( monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr( RequestConnectionProvider, 'get', lambda: STUB_CONNECTION )


def Test_Enrich_TestTransportationAttraction_ExpectRouteDurationMinutes(
      monkeypatch: pytest.MonkeyPatch,
      stub_request_connection: None,
) -> None:
   def minutes(
         _conn: Types.Connection,
         *,
         transportation: str,
         target_date: date,
   ) -> int | None:
      assert transportation == 'Zoomobile'
      assert target_date == VISIT_DATE
      return ROUTE_DURATION_MINUTES

   monkeypatch.setattr(
      'api.search.transportation_attraction_route_duration_enricher.TransportationRouteDurationResolver.minutes',
      minutes )

   zoomobile = Attraction(
      name='Zoomobile',
      free_with_admission=True,
      description='Zoomobile',
      info_link='https://example.com',
      hyperlink_text='Learn more',
      x_coord=1.0,
      y_coord=2.0,
      region='Africa',
      is_also_transportation=True )
   carousel = Attraction(
      name='Conservation Carousel',
      free_with_admission=True,
      description='Carousel',
      info_link='https://example.com',
      hyperlink_text='Learn more',
      x_coord=1.0,
      y_coord=2.0,
      region='Americas',
      is_also_transportation=False )

   TransportationAttractionRouteDurationEnricher.enrich(
      [ zoomobile, carousel ],
      target_date=VISIT_DATE )

   assert zoomobile.route_duration_minutes == ROUTE_DURATION_MINUTES
   assert carousel.route_duration_minutes is None

from __future__ import annotations

from datetime import date

import pytest

from api.models.attraction import Attraction
from api.search.transportation_attraction_route_duration_enricher import TransportationAttractionRouteDurationEnricher
from api.types import Types


VISIT_DATE = date( 2026, 6, 15 )
ROUTE_DURATION_MINUTES = 75


def Test_EnrichForVisit_TestTransportationAttraction_ExpectRouteDurationMinutes(
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

   TransportationAttractionRouteDurationEnricher.enrich_for_visit(
      [ zoomobile ],
      month=VISIT_DATE.month,
      day=VISIT_DATE.day,
      year=VISIT_DATE.year )

   assert zoomobile.route_duration_minutes == ROUTE_DURATION_MINUTES


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

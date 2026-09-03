from __future__ import annotations

import pytest

from api.models.pavilion import Pavilion
from api.pavilions.coordinators.pavilion_coordinator import PavilionCoordinator
from api.pavilions.data_access.pavilion_provider import PavilionProvider
from api.pavilions.search.pavilions_matching_query_builder import PavilionsMatchingQueryBuilder
from api.types import Types

QUERY = 'americas'
PAVILION = Pavilion( 'Americas Pavilion', 'Americas' )

def Test_GetPavilions_TestProviderRecords_ExpectReturned(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      PavilionProvider,
      'fetch_pavilions',
      lambda _conn: [ PAVILION ] )

   assert PavilionCoordinator.get_pavilions() == [ PAVILION ]

def Test_GetPavilionsMatchingQuery_TestBuilder_ExpectMatches(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   pavilions = [ PAVILION ]

   monkeypatch.setattr(
      PavilionCoordinator,
      'get_pavilions',
      lambda: pavilions )
   monkeypatch.setattr(
      PavilionsMatchingQueryBuilder,
      'build',
      lambda rows, query: rows if query == QUERY else [] )

   assert PavilionCoordinator.get_pavilions_matching_query( QUERY ) == pavilions

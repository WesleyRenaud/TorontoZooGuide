from __future__ import annotations

from collections.abc import Generator
from pathlib import Path
import shutil

from api_test_support.request_connection_test_support import STUB_REQUEST_CONNECTION
from api_test_support.seeded_database import SeededDatabase
import pytest

from api.database_connection_provider import DatabaseConnectionProvider
from api.request_connection_provider import RequestConnectionProvider
from api.seed.seed_runner import SeedRunner

@pytest.fixture
def stub_request_connection( monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      RequestConnectionProvider,
      'get',
      lambda: STUB_REQUEST_CONNECTION )


@pytest.fixture( scope='session' )
def seeded_template_db_path( tmp_path_factory: pytest.TempPathFactory ) -> Path:
   path = tmp_path_factory.mktemp( 'seeded-db' ) / 'animals.db'
   SeedRunner.apply_schema( db_path=str( path ) )
   SeedRunner.apply_seed_data( db_path=str( path ) )
   return path


@pytest.fixture
def db_path( tmp_path: Path, seeded_template_db_path: Path ) -> Path:
   path = tmp_path / 'animals.db'
   shutil.copy2( seeded_template_db_path, path )
   return path


@pytest.fixture
def seeded_database( db_path: Path ) -> Generator[ SeededDatabase, None, None ]:
   conn = DatabaseConnectionProvider.open( db_path=str( db_path ) )
   RequestConnectionProvider.set( conn )

   fixture = SeededDatabase( conn )

   try:
      yield fixture
   finally:
      fixture.close()


@pytest.fixture
def db( seeded_database: SeededDatabase ) -> SeededDatabase:
   return seeded_database

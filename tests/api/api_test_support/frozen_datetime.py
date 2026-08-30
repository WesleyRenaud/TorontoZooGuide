from __future__ import annotations

from datetime import date
from datetime import datetime
from datetime import tzinfo

import pytest


class FrozenDateTime( datetime ):
   frozen_now: datetime | None = None


   @classmethod
   def now( cls, tz: tzinfo | None = None ) -> datetime:
      if cls.frozen_now is None:
         raise RuntimeError(
            'FrozenDateTime.now was called before a test froze the database today.' )

      return cls.frozen_now


def patch_database_today( monkeypatch: pytest.MonkeyPatch, value: date ) -> None:
   FrozenDateTime.frozen_now = datetime.combine( value, datetime.min.time() )
   monkeypatch.setattr( 'api.shared.date_values.datetime', FrozenDateTime )

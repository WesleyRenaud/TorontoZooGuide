from __future__ import annotations

from ..data_access.defibrillator_provider import DefibrillatorProvider
from ...models import Defibrillator
from ...request_connection import get_connection


class DefibrillatorCoordinator():
   @classmethod
   def get_defibrillators( cls ) -> list[ Defibrillator ]:
      return DefibrillatorProvider.fetch_defibrillators( get_connection() )

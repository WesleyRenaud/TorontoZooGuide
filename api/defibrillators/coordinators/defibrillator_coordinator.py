from __future__ import annotations

from ..data_access.defibrillator_provider import DefibrillatorProvider
from ...models import Defibrillator
from ...request_connection_provider import RequestConnectionProvider


class DefibrillatorCoordinator():
   @classmethod
   def get_defibrillators( cls ) -> list[ Defibrillator ]:
      return DefibrillatorProvider.fetch_defibrillators( RequestConnectionProvider.get() )

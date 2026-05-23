from __future__ import annotations

from ..data_access.defibrillator import fetch_defibrillators
from ...models import Defibrillator
from ...request_connection import get_connection


class DefibrillatorController():


   @classmethod
   def get_defibrillators( cls ) -> list[ Defibrillator ]:
      return fetch_defibrillators( get_connection() )

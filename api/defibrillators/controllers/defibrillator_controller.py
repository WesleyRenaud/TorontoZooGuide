from __future__ import annotations

from ... import zoo
from ..data_access.defibrillator import fetch_defibrillators
from ...request_connection import get_connection


class DefibrillatorController():


   @classmethod
   def get_defibrillators( cls ) -> list[ zoo.Defibrillator ]:
      return fetch_defibrillators( get_connection() )

from ..data_access.defibrillator import fetch_defibrillators
from ...request_connection import get_connection


class DefibrillatorController():


   @classmethod
   def get_defibrillators( cls ):
      return fetch_defibrillators( get_connection() )

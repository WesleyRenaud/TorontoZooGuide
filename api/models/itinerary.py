from __future__ import annotations

from .animal import Animal
from .attraction import Attraction
from .guardians_talk import GuardiansTalk
from .itinerary_event import ItineraryEvent
from ..types import ScheduleTimeKey
from .wild_encounter import WildEncounter


class Itinerary:
   def __init__(
         self,
         date: str,
         animals: list[ Animal ] | None = None,
         attractions: list[ Attraction ] | None = None,
         guardians_talks: list[ GuardiansTalk ] | None = None,
         wild_encounters: list[ WildEncounter ] | None = None,
         events: list[ ItineraryEvent ] | None = None,
         arrival_time: ScheduleTimeKey = None,
         departure_time: ScheduleTimeKey = None ) -> None:
      self.date = date
      self.animals = animals or []
      self.attractions = attractions or []
      self.guardians_talks = guardians_talks or []
      self.wild_encounters = wild_encounters or []
      self.events = events or []
      self.arrival_time = arrival_time
      self.departure_time = departure_time


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'date': self.date,
         'arrival_time': self.arrival_time,
         'departure_time': self.departure_time,
         'animals': [
            self._to_dict_with_type( a, 'animal' ) for a in self.animals
         ],
         'attractions': [
            self._to_dict_with_type( a, 'attraction' ) for a in self.attractions
         ],
         'guardians_talks': [
            self._to_dict_with_type( g, 'guardiansTalk' ) for g in self.guardians_talks
         ],
         'wild_encounters': [
            self._to_dict_with_type( w, 'wildEncounter' ) for w in self.wild_encounters
         ],
         'events': [
            self._to_dict_with_type( event, 'itineraryEvent' ) for event in self.events
         ]
      }


   def _to_dict_with_type(
         self,
         obj: Animal | Attraction | GuardiansTalk | WildEncounter | ItineraryEvent | dict[ str, object ],
         fallback_type: str ) -> dict[ str, object ]:
      if hasattr( obj, 'to_dict' ):
         d = obj.to_dict()
      else:
         d = dict( obj ) if isinstance( obj, dict ) else {}

      d[ 'type' ] = d.get( 'type', fallback_type )
      return d

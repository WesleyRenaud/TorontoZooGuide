from __future__ import annotations

from .animal import Animal
from .attraction import Attraction
from .guardians_talk import GuardiansTalk
from .itinerary_event import ItineraryEvent
from .itinerary_transportation import ItineraryTransportation
from .itinerary_transportation_station import ItineraryTransportationStation
from ..shared.typed_dict_mapper import TypedDictMapper
from ..types import Types
from .wild_encounter import WildEncounter


class Itinerary:
   def __init__(
         self,
         date: str,
         selected_exhibits: list[ str ] | None = None,
         animals: list[ Animal ] | None = None,
         attractions: list[ Attraction ] | None = None,
         transportations: list[ ItineraryTransportation ] | None = None,
         transportation_stations: list[ ItineraryTransportationStation ] | None = None,
         guardians_talks: list[ GuardiansTalk ] | None = None,
         wild_encounters: list[ WildEncounter ] | None = None,
         events: list[ ItineraryEvent ] | None = None,
         arrival_time: Types.ScheduleTimeKey = None,
         departure_time: Types.ScheduleTimeKey = None ) -> None:
      self.date = date
      self.selected_exhibits = selected_exhibits or []
      self.animals = animals or []
      self.attractions = attractions or []
      self.transportations = transportations or []
      self.transportation_stations = transportation_stations or []
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
         'selected_exhibits': list( self.selected_exhibits ),
         'animals': [
            TypedDictMapper.to_dict_with_type( a, 'animal' ) for a in self.animals
         ],
         'attractions': [
            TypedDictMapper.to_dict_with_type( a, 'attraction' ) for a in self.attractions
         ],
         'transportations': [
            TypedDictMapper.to_dict_with_type( t, 'transportation' )
            for t in self.transportations
         ],
         'transportation_stations': [
            station.to_dict()
            for station in self.transportation_stations
         ],
         'guardians_talks': [
            TypedDictMapper.to_dict_with_type( g, 'guardiansTalk' ) for g in self.guardians_talks
         ],
         'wild_encounters': [
            TypedDictMapper.to_dict_with_type( w, 'wildEncounter' ) for w in self.wild_encounters
         ],
         'events': [
            TypedDictMapper.to_dict_with_type( event, 'itineraryEvent' ) for event in self.events
         ],
      }

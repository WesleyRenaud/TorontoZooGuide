from __future__ import annotations

from ...models import Animal
from ...models import Attraction
from ...models import GuardiansTalk
from ...models import Itinerary
from ...models import ItineraryEvent
from ...models import WildEncounter
from ...shared.date_values import DateValues
from ...shared.enums import ItineraryEventType
from ...types import ScheduleTimeKey


class ItineraryActivityScheduler:
   def __init__( self, itinerary: Itinerary ) -> None:
      self.itinerary = itinerary


   def schedule_animal(
         self,
         species: str,
         exhibit: str,
         start_time: ScheduleTimeKey,
         end_time: ScheduleTimeKey ) -> bool:
      animal = next(
         (
            item for item in self.itinerary.animals
            if item.species == species and item.exhibit == exhibit
         ),
         None )

      if animal == None:
         return False

      self.schedule_item( animal, start_time, end_time )
      return True


   def schedule_attraction(
         self,
         name: str,
         start_time: ScheduleTimeKey,
         end_time: ScheduleTimeKey ) -> bool:
      attraction = next(
         (
            item for item in self.itinerary.attractions
            if item.name == name
         ),
         None )

      if attraction == None:
         return False

      self.schedule_item( attraction, start_time, end_time )
      return True


   def schedule_guardians_talk(
         self,
         name: str,
         start_time: ScheduleTimeKey,
         end_time: ScheduleTimeKey ) -> bool:
      guardians_talk = next(
         (
            item for item in self.itinerary.guardians_talks
            if item.name == name
         ),
         None )

      if guardians_talk == None:
         return False

      self.schedule_item( guardians_talk, start_time, end_time )
      return True


   def schedule_wild_encounter(
         self,
         name: str,
         start_time: ScheduleTimeKey,
         end_time: ScheduleTimeKey ) -> bool:
      wild_encounter = next(
         (
            item for item in self.itinerary.wild_encounters
            if item.name == name
         ),
         None )

      if wild_encounter == None:
         return False

      self.schedule_item( wild_encounter, start_time, end_time )
      return True


   def schedule_event(
         self,
         event_type: ItineraryEventType,
         start_time: ScheduleTimeKey,
         end_time: ScheduleTimeKey ) -> ItineraryEvent:
      event = ItineraryEvent(
         event_type=event_type,
         start_time=DateValues.normalize_itinerary_schedule_time( start_time ),
         end_time=DateValues.normalize_itinerary_schedule_time( end_time ) )

      self.itinerary.events.append( event )
      return event


   def schedule_item(
         self,
         item: Animal | Attraction | GuardiansTalk | WildEncounter,
         start_time: ScheduleTimeKey,
         end_time: ScheduleTimeKey ) -> None:
      item.start_time = DateValues.normalize_itinerary_schedule_time( start_time )
      item.end_time = DateValues.normalize_itinerary_schedule_time( end_time )

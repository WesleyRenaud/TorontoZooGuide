from __future__ import annotations

from ...animals.coordinators.animal_coordinator import AnimalCoordinator
from ...attractions.coordinators.attraction_coordinator import AttractionCoordinator
from ..data_access.saved_itinerary import SavedItinerary
from ...guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from .itinerary_transportations import build_itinerary_transportations
from ...models import Animal
from ...models import Attraction
from ...models import GuardiansTalk
from ...models import Itinerary
from ...models import ItineraryEvent
from ...models import ItineraryTransportation
from ...models import WildEncounter
from ...types import DateInput, ScheduleTimeKey
from ...wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


def empty_itinerary() -> Itinerary:
   return Itinerary(
      date='',
      selected_exhibits=[],
      animals=[],
      attractions=[],
      transportations=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
      arrival_time=None,
      departure_time=None )


def build_itinerary(
      date: DateInput,
      selected_exhibits: list[ str ],
      animals: list[ Animal ],
      attractions: list[ Attraction ],
      transportations: list[ ItineraryTransportation ],
      guardians_talks: list[ GuardiansTalk ],
      wild_encounters: list[ WildEncounter ],
      events: list[ ItineraryEvent ],
      arrival_time: ScheduleTimeKey,
      departure_time: ScheduleTimeKey ) -> Itinerary:

   return Itinerary(
      date=date,
      selected_exhibits=selected_exhibits,
      animals=animals,
      attractions=attractions,
      transportations=transportations,
      guardians_talks=guardians_talks,
      wild_encounters=wild_encounters,
      events=events,
      arrival_time=arrival_time,
      departure_time=departure_time )


def build_current_itinerary(
      saved_itinerary: SavedItinerary,
      animal_coordinator: type[ AnimalCoordinator ],
      attraction_coordinator: type[ AttractionCoordinator ],
      guardians_coordinator: type[ GuardiansCoordinator ],
      wild_encounter_coordinator: type[ WildEncounterCoordinator ],
      visit_date_temp: float | None = None ) -> Itinerary:

   if saved_itinerary.is_empty():
      return empty_itinerary()

   day = saved_itinerary.day()
   month = saved_itinerary.month()
   year = saved_itinerary.year()

   animals = animal_coordinator.get_animals_for_saved_itinerary(
      day=day,
      month=month,
      year=year,
      saved_animals=list( saved_itinerary.animal_rows ),
      temp=visit_date_temp )

   attractions = attraction_coordinator.get_attractions_for_saved_itinerary(
      day=day,
      month=month,
      year=year,
      saved_attractions=list( saved_itinerary.attraction_rows ) )

   guardians_talks = guardians_coordinator.get_guardians_talks_for_saved_itinerary(
      list( saved_itinerary.guardians_talk_rows ) )

   wild_encounters = wild_encounter_coordinator.get_wild_encounters_for_saved_itinerary(
      list( saved_itinerary.wild_encounter_rows ) )

   events = [
      ItineraryEvent(
         event_type=event.event_type,
         start_time=event.start_time,
         end_time=event.end_time )
      for event in saved_itinerary.event_rows
   ]

   return build_itinerary(
      date=saved_itinerary.date_value,
      selected_exhibits=saved_itinerary.selected_exhibits,
      animals=animals,
      attractions=attractions,
      transportations=build_itinerary_transportations(
         saved_itinerary.transportation_rows ),
      guardians_talks=guardians_talks,
      wild_encounters=wild_encounters,
      events=events,
      arrival_time=saved_itinerary.arrival_time,
      departure_time=saved_itinerary.departure_time )

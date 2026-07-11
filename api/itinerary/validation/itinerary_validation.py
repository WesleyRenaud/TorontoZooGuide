from __future__ import annotations

from dataclasses import replace
from datetime import date

from ...animals.coordinators.animal_coordinator import AnimalCoordinator
from ...attractions.coordinators.attraction_coordinator import AttractionCoordinator
from ..data_access.itinerary import fetch_saved_itinerary
from ..data_access.itinerary_animal_input import ItineraryAnimalInput
from ..data_access.itinerary_animal_record import ItineraryAnimalRecord
from ..data_access.itinerary_animal_save_carryover import itinerary_animal_save_carryover
from ..data_access.itinerary_attraction_record import ItineraryAttractionRecord
from ..data_access.itinerary_attraction_save_carryover import itinerary_attraction_save_carryover
from ..data_access.itinerary_event_record import ItineraryEventRecord
from ..data_access.itinerary_save_input import ItinerarySaveInput
from ..data_access.saved_itinerary import SavedItinerary
from ..data_access.validated_itinerary import ValidatedItinerary
from ..domain.itinerary_visit_window import cleared_schedule_times_for_visit_window
from ..domain.itinerary_visit_window import schedule_time_occurs_outside_visit_window
from ...guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from ...guardians.itinerary.guardians_talk_itinerary_validation import validate_guardians_talks_for_itinerary
from ...models import AnimalDiff
from ...models import AttractionDiff
from ...models import GuardiansTalkDiff
from ...models import WildEncounterDiff
from ...models.itinerary_event import ItineraryEvent
from ..scheduling.extend_departure_for_activity import departure_time_covering_schedule_ends
from ...shared.enums import ItineraryEventType
from ...types import Connection, DateKey, ScheduleTimeKey
from ..warnings.guardians_talk_unschedule_warning import new_guardians_talks_overlapping_saved_schedule
from ..warnings.wild_encounter_unschedule_warning import new_wild_encounters_overlapping_saved_schedule
from ...wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from ...wild_encounters.itinerary.wild_encounter_itinerary_validation import validate_wild_encounters_for_itinerary


def validate_itinerary_animals(
      animal_coordinator: type[ AnimalCoordinator ],
      animals: list[ ItineraryAnimalInput ],
      new_visit_date: date,
      *,
      arrival_time: ScheduleTimeKey,
      departure_time: ScheduleTimeKey,
      new_visit_date_temp: float | None = None,
      old_visit_date: DateKey | None = None,
      saved_animal_rows: list[ ItineraryAnimalRecord ] | None = None,
      visit_date_is_changing: bool = False ) -> list[ AnimalDiff ]:
   diffs: list[ AnimalDiff ] = []

   for animal in animals:
      carryover = itinerary_animal_save_carryover(
         saved_animal_rows,
         animal,
         old_visit_date=old_visit_date )

      saved_animals = animal_coordinator.get_animals_for_saved_itinerary(
         day=new_visit_date.day,
         month=new_visit_date.month,
         year=new_visit_date.year,
         temp=new_visit_date_temp,
         saved_animals=[
            ItineraryAnimalRecord(
               species=carryover.species,
               exhibit=carryover.exhibit,
               enclosure_name=carryover.enclosure_name,
               old_likelihood=None,
               new_likelihood=None ) ],
      )

      new_likelihood = (
         None
         if not saved_animals
         else max( ( a.likelihood or 0 ) for a in saved_animals ) )
      start_time, end_time = (
         ( carryover.start_time, carryover.end_time )
         if visit_date_is_changing
         else cleared_schedule_times_for_visit_window(
            carryover.start_time,
            carryover.end_time,
            arrival_time=arrival_time,
            departure_time=departure_time ) )

      diffs.append(
         AnimalDiff(
            species=carryover.species,
            exhibit=carryover.exhibit,
            enclosure_name=carryover.enclosure_name,
            old_likelihood=carryover.old_likelihood,
            new_likelihood=new_likelihood,
            is_added=carryover.is_added,
            start_time=start_time,
            end_time=end_time,
         )
      )

   return diffs



def validate_itinerary_attractions(
      attraction_coordinator: type[ AttractionCoordinator ],
      attractions: tuple[ str, ... ],
      new_visit_date: date,
      *,
      arrival_time: ScheduleTimeKey,
      departure_time: ScheduleTimeKey,
      old_visit_date: DateKey | None = None,
      saved_attraction_rows: list[ ItineraryAttractionRecord ] | None = None,
      visit_date_is_changing: bool = False ) -> list[ AttractionDiff ]:
   diffs: list[ AttractionDiff ] = []

   for attraction_name in attractions:
      carryover = itinerary_attraction_save_carryover(
         saved_attraction_rows,
         attraction_name,
         old_visit_date=old_visit_date )

      new_likelihood = attraction_coordinator.get_attraction_likelihood_for_visit_date(
         visit_date=new_visit_date,
         attraction_name=attraction_name )
      start_time, end_time = (
         ( carryover.start_time, carryover.end_time )
         if visit_date_is_changing
         else cleared_schedule_times_for_visit_window(
            carryover.start_time,
            carryover.end_time,
            arrival_time=arrival_time,
            departure_time=departure_time ) )

      diffs.append(
         AttractionDiff(
            name=carryover.name,
            old_likelihood=carryover.old_likelihood,
            new_likelihood=new_likelihood,
            start_time=start_time,
            end_time=end_time,
         )
      )

   return diffs



def guardians_talk_diffs_within_visit_window(
      guardians_talks: list[ GuardiansTalkDiff ],
      *,
      arrival_time: ScheduleTimeKey,
      departure_time: ScheduleTimeKey ) -> list[ GuardiansTalkDiff ]:
   return [
      talk
      for talk in guardians_talks
      if not schedule_time_occurs_outside_visit_window(
            talk.start_time,
            talk.end_time,
            arrival_time=arrival_time,
            departure_time=departure_time )
   ]



def wild_encounter_diffs_within_visit_window(
      wild_encounters: list[ WildEncounterDiff ],
      *,
      arrival_time: ScheduleTimeKey,
      departure_time: ScheduleTimeKey ) -> list[ WildEncounterDiff ]:
   return [
      encounter
      for encounter in wild_encounters
      if not schedule_time_occurs_outside_visit_window(
            encounter.start_time,
            encounter.end_time,
            arrival_time=arrival_time,
            departure_time=departure_time )
   ]



def itinerary_events_from_saved_rows(
      event_rows: list[ ItineraryEventRecord ],
      *,
      arrival_time: ScheduleTimeKey,
      departure_time: ScheduleTimeKey ) -> list[ ItineraryEvent ]:
   events: list[ ItineraryEvent ] = []

   for event in event_rows:
      if event.event_type in (
            ItineraryEventType.ARRIVAL,
            ItineraryEventType.DEPARTURE ):
         continue

      if schedule_time_occurs_outside_visit_window(
            event.start_time,
            event.end_time,
            arrival_time=arrival_time,
            departure_time=departure_time ):
         continue

      events.append(
         ItineraryEvent(
            event_type=event.event_type,
            start_time=event.start_time,
            end_time=event.end_time,
         )
      )

   return events



def validate_itinerary_for_save(
      conn: Connection,
      save_input: ItinerarySaveInput,
      animal_coordinator: type[ AnimalCoordinator ],
      attraction_coordinator: type[ AttractionCoordinator ],
      guardians_coordinator: type[ GuardiansCoordinator ],
      wild_encounter_coordinator: type[ WildEncounterCoordinator ],
      *,
      new_visit_date_temp: float | None = None,
      old_visit_date: DateKey | None = None ) -> ValidatedItinerary:
   arrival_time = save_input.arrival_time
   saved_itinerary = fetch_saved_itinerary( conn )
   has_saved_itinerary = old_visit_date is not None
   visit_date_is_changing = (
      has_saved_itinerary
      and old_visit_date != save_input.date.isoformat() )
   guardians_talk_diffs = validate_guardians_talks_for_itinerary(
      save_input.guardians_talks,
      guardians_coordinator.get_guardians_talk_schedule(
         month=save_input.month(),
         day=save_input.day(),
         year=save_input.year() ) )
   wild_encounter_diffs = validate_wild_encounters_for_itinerary(
      save_input.wild_encounters,
      wild_encounter_coordinator.get_wild_encounter_schedule(
         month=save_input.month(),
         day=save_input.day(),
         year=save_input.year() ) )
   departure_time = save_input.departure_time

   if not visit_date_is_changing:
      departure_time = departure_time_covering_schedule_ends(
         departure_time,
         [
            *(
               talk.end_time
               for talk in guardians_talk_diffs
               if not talk.is_deleted
            ),
            *(
               encounter.end_time
               for encounter in wild_encounter_diffs
               if not encounter.is_deleted
            ),
         ] )

   validated_itinerary = ValidatedItinerary(
      arrival_time=arrival_time,
      departure_time=departure_time,
      animals=(
         validate_itinerary_animals(
            animal_coordinator,
            animals=save_input.animals,
            new_visit_date=save_input.date,
            arrival_time=arrival_time,
            departure_time=departure_time,
            new_visit_date_temp=new_visit_date_temp,
            old_visit_date=old_visit_date,
            saved_animal_rows=saved_itinerary.animal_rows,
            visit_date_is_changing=visit_date_is_changing )
         if save_input.animals
         else [] ),
      attractions=(
         validate_itinerary_attractions(
            attraction_coordinator,
            attractions=save_input.attractions,
            new_visit_date=save_input.date,
            arrival_time=arrival_time,
            departure_time=departure_time,
            old_visit_date=old_visit_date,
            saved_attraction_rows=saved_itinerary.attraction_rows,
            visit_date_is_changing=visit_date_is_changing )
         if save_input.attractions
         else [] ),
      guardians_talks=guardians_talk_diffs_within_visit_window(
         guardians_talk_diffs,
         arrival_time=arrival_time,
         departure_time=departure_time ),
      wild_encounters=wild_encounter_diffs_within_visit_window(
         wild_encounter_diffs,
         arrival_time=arrival_time,
         departure_time=departure_time ),
      events=itinerary_events_from_saved_rows(
         saved_itinerary.event_rows,
         arrival_time=arrival_time,
         departure_time=departure_time ),
   )

   return replace(
      validated_itinerary,
      needs_schedule_reschedule=(
         itinerary_needs_schedule_reschedule(
            saved_itinerary,
            validated_itinerary )
         if has_saved_itinerary
         else False ) )


def itinerary_needs_schedule_reschedule(
      saved_itinerary: SavedItinerary,
      validated_itinerary: ValidatedItinerary ) -> bool:
   if new_guardians_talks_overlapping_saved_schedule(
         saved_itinerary,
         validated_itinerary ):
      return True

   if new_wild_encounters_overlapping_saved_schedule(
         saved_itinerary,
         validated_itinerary ):
      return True

   if (
         saved_itinerary.arrival_time != validated_itinerary.arrival_time
         or saved_itinerary.departure_time != validated_itinerary.departure_time ):
      return True

   saved_talk_names = {
      talk.talk_name
      for talk in saved_itinerary.guardians_talk_rows
      if not talk.is_deleted
   }
   validated_talk_names = {
      talk.name
      for talk in validated_itinerary.guardians_talks
      if not talk.is_deleted
   }

   if saved_talk_names - validated_talk_names:
      return True

   saved_encounter_names = {
      encounter.wild_encounter
      for encounter in saved_itinerary.wild_encounter_rows
      if not encounter.is_deleted
   }
   validated_encounter_names = {
      encounter.name
      for encounter in validated_itinerary.wild_encounters
      if not encounter.is_deleted
   }

   return bool( saved_encounter_names - validated_encounter_names )
